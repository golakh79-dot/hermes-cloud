from __future__ import annotations

import asyncio
import json
from urllib.parse import quote

import httpx

from polyester.auth import ApiKeyCredentials, sign_request_async
from polyester.errors import (
    TIMESTAMP_SKEW,
    PolyesterAuthError,
    PolyesterRealtimeError,
    PolyesterTimestampSkewError,
    PolyesterTransportError,
)
from polyester.user_agent import cloudflare_1010_message, is_cloudflare_browser_ban

MAX_TOKEN_RESPONSE_BYTES = 64 * 1024
_MAX_ERROR_BODY_CHARS = 512
_DEFAULT_TIMEOUT_SECONDS = 10.0


def connection_token_url(api_url: str) -> str:
    return f"{api_url.rstrip('/')}/v1/rt/token"


def subscription_token_url(api_url: str, channel: str) -> str:
    base = f"{api_url.rstrip('/')}/v1/rt/subscribe"
    return f"{base}?channel={quote(channel, safe='')}"


def _client_timeout_seconds(http: httpx.AsyncClient) -> float:
    """Resolve the SDK-configured timeout as one absolute wall-clock budget."""
    timeout = http.timeout
    if timeout is None:
        return _DEFAULT_TIMEOUT_SECONDS
    if isinstance(timeout, (int, float)):
        return float(timeout)
    for name in ("read", "write", "connect", "pool"):
        value = getattr(timeout, name, None)
        if isinstance(value, (int, float)):
            return float(value)
    return _DEFAULT_TIMEOUT_SECONDS


def _content_length_exceeds_limit(response: httpx.Response, max_bytes: int) -> bool:
    raw = response.headers.get("content-length")
    if raw is None:
        return False
    try:
        return int(raw) > max_bytes
    except ValueError:
        return False


def _truncate_body(raw: bytes) -> str:
    text = raw.decode("utf-8", errors="replace").strip()
    if len(text) > _MAX_ERROR_BODY_CHARS:
        return text[:_MAX_ERROR_BODY_CHARS] + "…"
    return text


async def _read_limited(response: httpx.Response, max_bytes: int, *, label: str) -> bytes:
    if _content_length_exceeds_limit(response, max_bytes):
        raise PolyesterRealtimeError(f"{label}: response exceeds {max_bytes} bytes")
    chunks: list[bytes] = []
    total = 0
    async for chunk in response.aiter_bytes():
        total += len(chunk)
        if total > max_bytes:
            raise PolyesterRealtimeError(f"{label}: response exceeds {max_bytes} bytes")
        chunks.append(chunk)
    return b"".join(chunks)


def _auth_http_error(
    *,
    status_code: int,
    label: str,
    endpoint: str,
    body: bytes,
) -> PolyesterAuthError | PolyesterTimestampSkewError:
    truncated = _truncate_body(body)
    code: str | None = None
    server_message: str | None = None
    try:
        payload = json.loads(body)
        if isinstance(payload, dict):
            raw_code = payload.get("code")
            raw_message = payload.get("message")
            if isinstance(raw_code, str) and raw_code.strip():
                code = raw_code.strip()
            if isinstance(raw_message, str) and raw_message.strip():
                server_message = raw_message.strip()
    except (json.JSONDecodeError, UnicodeDecodeError):
        pass
    if code == TIMESTAMP_SKEW:
        return PolyesterTimestampSkewError(f"{label}: {TIMESTAMP_SKEW}", status_code=status_code)
    code = code or ("permission_denied" if status_code == 403 else "unauthenticated")
    kind = "permission denied" if status_code == 403 else "authentication failed"
    detail = server_message or truncated
    message = f"{label}: {kind} (HTTP {status_code}, code {code})"
    if detail:
        message = f"{message}: {detail}"
    message = f"{message} [{endpoint}]"
    return PolyesterAuthError(
        message,
        status_code=status_code,
        label=label,
        body=truncated or None,
        code=code,
        context=label,
        endpoint=endpoint,
    )


async def fetch_rt_token(
    http: httpx.AsyncClient,
    credentials: ApiKeyCredentials,
    *,
    url: str,
    label: str,
) -> str:
    headers = await sign_request_async(credentials, method="GET", url=url, body=b"")
    # One absolute wall-clock deadline covers request headers + bounded body.
    # httpx per-phase timeouts alone are insufficient: slow-drip chunks can each
    # arrive within the read timeout while the total exceeds the SDK budget.
    timeout = _client_timeout_seconds(http)
    try:
        async with asyncio.timeout(timeout):
            async with http.stream("GET", url, headers=headers) as response:
                try:
                    raw = await _read_limited(response, MAX_TOKEN_RESPONSE_BYTES, label=label)
                except asyncio.CancelledError:
                    # Ensure the streamed peer is aborted promptly on cancel (E6).
                    await response.aclose()
                    raise
                if response.status_code == 403 and is_cloudflare_browser_ban(
                    raw.decode("utf-8", errors="replace")
                ):
                    raise PolyesterTransportError(cloudflare_1010_message())
                if response.status_code in (401, 403):
                    raise _auth_http_error(
                        status_code=response.status_code,
                        label=label,
                        endpoint=url,
                        body=raw,
                    )
                if response.status_code >= 400:
                    truncated = _truncate_body(raw)
                    detail = f": {truncated}" if truncated else ""
                    raise PolyesterRealtimeError(f"{label}: HTTP {response.status_code}{detail}")
    except TimeoutError as exc:
        raise PolyesterRealtimeError(f"{label}: timed out") from exc
    except httpx.TimeoutException as exc:
        raise PolyesterRealtimeError(f"{label}: timed out") from exc
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise PolyesterRealtimeError(f"{label}: response is not valid JSON") from exc
    token = payload.get("token") if isinstance(payload, dict) else None
    if not token:
        raise PolyesterRealtimeError(f"{label}: response missing token")
    return str(token)


async def fetch_connection_token(
    http: httpx.AsyncClient,
    credentials: ApiKeyCredentials,
    *,
    api_url: str,
) -> str:
    return await fetch_rt_token(
        http,
        credentials,
        url=connection_token_url(api_url),
        label="realtime connection token",
    )


async def fetch_subscription_token(
    http: httpx.AsyncClient,
    credentials: ApiKeyCredentials,
    *,
    api_url: str,
    channel: str,
) -> str:
    return await fetch_rt_token(
        http,
        credentials,
        url=subscription_token_url(api_url, channel),
        label=f"realtime subscription token for {channel}",
    )
