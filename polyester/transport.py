from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import httpx
import pyqwest
from connectrpc.code import Code
from connectrpc.codec import proto_binary_codec
from connectrpc.errors import ConnectError
from connectrpc.interceptor import UnaryInterceptor
from google.protobuf.json_format import MessageToJson, Parse
from google.protobuf.message import Message

from polyester.auth import ApiKeyCredentials
from polyester.auth_interceptor import ApiKeyAuthUnaryInterceptor, UserAgentUnaryInterceptor
from polyester.errors import TIMESTAMP_SKEW, PolyesterAuthError, PolyesterTransportError
from polyester.user_agent import USER_AGENT, USER_AGENT_HEADER

WireFormat = Literal["binary", "json"]
MAX_CONNECT_RESPONSE_BYTES = 4 * 1024 * 1024


class _ProtoJSONCodec:
    """Protobuf JSON codec that ignores fields and enum names this SDK does not
    know yet (the server adds them ahead of SDK releases); unknown enum names
    read as the unspecified value, unknown enum numbers stay numbers."""

    def name(self) -> str:
        return "json"

    def encode(self, message: Message) -> bytes:
        return MessageToJson(message).encode()

    def decode(self, data: bytes | bytearray, message: Message) -> Message:
        Parse(bytes(data), message, ignore_unknown_fields=True)
        return message


_PROTO_JSON_CODEC = _ProtoJSONCodec()


_CONNECT_CODES = frozenset(code.value for code in Code)
# HTTP status -> Connect code for a non-Connect error body (Connect protocol table).
_HTTP_STATUS_TO_CODE = {
    400: Code.INTERNAL,
    401: Code.UNAUTHENTICATED,
    403: Code.PERMISSION_DENIED,
    404: Code.UNIMPLEMENTED,
    429: Code.UNAVAILABLE,
    502: Code.UNAVAILABLE,
    503: Code.UNAVAILABLE,
    504: Code.UNAVAILABLE,
}


def _raise_for_gateway_rejection(response: pyqwest.FullResponse) -> pyqwest.FullResponse:
    """Map an API-gateway rejection that is not a Connect error.

    The gateway answers API-key failures with a JSON body such as
    ``{"code": "TIMESTAMP_SKEW"}`` (``application/json`` or
    ``application/problem+json``). connectrpc would read that ``code`` as an
    unknown Connect code and report ``unavailable``, a retryable server error.
    Map it by HTTP status instead, keeping the gateway code as the message, so
    ``TIMESTAMP_SKEW`` and ``SIGNATURE_INVALID`` reach the error mapping.
    """
    if response.status == 200:
        return response
    content_type = response.headers.get("content-type", "").lower()
    if "json" not in content_type:
        return response
    try:
        body = response.json()
    except Exception:
        return response
    if not isinstance(body, dict):
        return response
    code = body.get("code")
    if not isinstance(code, str) or not code or code in _CONNECT_CODES:
        return response
    if code == TIMESTAMP_SKEW:
        raise ConnectError(Code.UNAUTHENTICATED, TIMESTAMP_SKEW)
    raise ConnectError(_HTTP_STATUS_TO_CODE.get(response.status, Code.UNKNOWN), code)


class _ConnectHTTPClient:
    """pyqwest client for generated Connect clients; see ``_raise_for_gateway_rejection``."""

    def __init__(self, inner: pyqwest.Client | None = None) -> None:
        self._inner = inner or pyqwest.Client()

    async def post(self, url: str, headers=None, content=None, **kwargs) -> pyqwest.FullResponse:
        response = await self._inner.post(url=url, headers=headers, content=content, **kwargs)
        return _raise_for_gateway_rejection(response)

    async def get(self, url: str, headers=None, **kwargs) -> pyqwest.FullResponse:
        response = await self._inner.get(url=url, headers=headers, **kwargs)
        return _raise_for_gateway_rejection(response)


def codec_for_config(config: TransportConfig):
    if config.wire_format == "json":
        return _PROTO_JSON_CODEC
    return proto_binary_codec()


@dataclass(frozen=True, slots=True)
class TransportConfig:
    api_url: str
    timeout: float = 10.0
    wire_format: WireFormat = "binary"

    def __repr__(self) -> str:
        return (
            f"TransportConfig(api_url={self.api_url!r}, timeout={self.timeout!r}, "
            f"wire_format={self.wire_format!r})"
        )


class TransportFactory:
    """Owns SDK HTTP clients and generated Connect-client construction."""

    def __init__(
        self,
        config: TransportConfig,
        *,
        credentials: ApiKeyCredentials | None = None,
    ) -> None:
        self.config = config
        self.credentials = credentials
        self.public_http = httpx.AsyncClient(
            base_url=config.api_url,
            timeout=config.timeout,
            headers={USER_AGENT_HEADER: USER_AGENT},
        )
        self._codec = codec_for_config(config)
        self._connect_http = _ConnectHTTPClient()
        self._user_agent_interceptor = UserAgentUnaryInterceptor()
        self._auth_interceptors: list[UnaryInterceptor] = [self._user_agent_interceptor]
        if credentials is not None:
            self._auth_interceptors.append(
                ApiKeyAuthUnaryInterceptor(
                    credentials,
                    base_url=config.api_url,
                    codec=self._codec,
                )
            )

    def __repr__(self) -> str:
        creds = "[REDACTED]" if self.credentials is not None else None
        return f"TransportFactory(config={self.config!r}, credentials={creds})"

    def _client_kwargs(self) -> dict:
        return {
            "codec": self._codec,
            "timeout_ms": int(self.config.timeout * 1000),
            "read_max_bytes": MAX_CONNECT_RESPONSE_BYTES,
            # Signing hashes the protobuf/JSON body; gzip would break API-key auth.
            "send_compression": None,
            "http_client": self._connect_http,
        }

    def create_public_client(self, client_cls: type):
        return client_cls(
            self.config.api_url,
            interceptors=[self._user_agent_interceptor],
            **self._client_kwargs(),
        )

    def create_auth_client(self, client_cls: type):
        if self.credentials is None:
            raise PolyesterAuthError("This endpoint requires Polyester API-key credentials")
        return client_cls(
            self.config.api_url,
            interceptors=self._auth_interceptors,
            **self._client_kwargs(),
        )

    async def aclose(self) -> None:
        await self.public_http.aclose()


def map_transport_error(exc: Exception) -> PolyesterTransportError:
    if isinstance(exc, (httpx.TimeoutException, httpx.NetworkError)):
        return PolyesterTransportError(str(exc))
    return PolyesterTransportError(str(exc))
