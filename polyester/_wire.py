from __future__ import annotations

from typing import Any

from connectrpc.errors import ConnectError
from google.protobuf.any_pb2 import Any as AnyMessage
from google.protobuf.json_format import MessageToDict
from google.protobuf.message import Message

from polyester.codecs.decode.ratelimit import (
    rate_limit_detail_from_proto,
    retry_after_seconds_from_detail,
)
from polyester.codecs.proto_helpers import error_code_name, format_uint64_id
from polyester.errors import (
    TIMESTAMP_SKEW,
    PolyesterApiError,
    PolyesterAuthError,
    PolyesterNotImplementedError,
    PolyesterRateLimitError,
    PolyesterRouteNotFoundError,
    PolyesterServerError,
    PolyesterTimeoutError,
    PolyesterTimestampSkewError,
    PolyesterTransportError,
)
from polyester.gen.auth.v1 import auth_pb2
from polyester.gen.chain.withdraw.v1 import withdraw_pb2
from polyester.gen.orders.v1 import orders_pb2
from polyester.gen.polyester.ratelimit.v1 import types_pb2 as ratelimit_pb2
from polyester.gen.transfer.v1 import internal_transfer_pb2 as transfer_pb2
from polyester.user_agent import cloudflare_1010_message, is_cloudflare_browser_ban

_ROUTE_NOT_FOUND_MESSAGES = frozenset({"not found", "404 page not found", "404 not found"})
_EMPTY_ERROR_MESSAGE = "request failed without server error details"
# connectrpc reports a bare (non-Connect) HTTP error by its status phrase; a
# bare 501 arrives as code ``unknown`` with this message.
_HTTP_501_PHRASE = "Not Implemented"


def protobuf_to_public_dict(message: Message) -> dict[str, Any]:
    return MessageToDict(
        message,
        preserving_proto_field_name=False,
        always_print_fields_with_no_presence=True,
    )


def _unpack_error_detail(detail: Message) -> Message | None:
    if isinstance(detail, AnyMessage) or detail.DESCRIPTOR.full_name == "google.protobuf.Any":
        if detail.Is(auth_pb2.AuthErrorDetail.DESCRIPTOR):
            auth_detail = auth_pb2.AuthErrorDetail()
            detail.Unpack(auth_detail)
            return auth_detail
        if detail.Is(orders_pb2.ErrorDetail.DESCRIPTOR):
            order_detail = orders_pb2.ErrorDetail()
            detail.Unpack(order_detail)
            return order_detail
        if detail.Is(withdraw_pb2.ErrorDetail.DESCRIPTOR):
            withdraw_detail = withdraw_pb2.ErrorDetail()
            detail.Unpack(withdraw_detail)
            return withdraw_detail
        if detail.Is(transfer_pb2.ErrorDetail.DESCRIPTOR):
            transfer_detail = transfer_pb2.ErrorDetail()
            detail.Unpack(transfer_detail)
            return transfer_detail
        if detail.Is(ratelimit_pb2.RateLimitDetail.DESCRIPTOR):
            rate_limit = ratelimit_pb2.RateLimitDetail()
            detail.Unpack(rate_limit)
            return rate_limit
        return None
    return detail


def _rate_limit_error(message: str, *, proto_detail=None) -> PolyesterRateLimitError:
    detail = rate_limit_detail_from_proto(proto_detail)
    return PolyesterRateLimitError(
        message,
        retry_after=retry_after_seconds_from_detail(detail),
        detail=detail,
    )


def map_connect_error(exc: ConnectError):
    if (exc.message or "").strip() == TIMESTAMP_SKEW:
        return PolyesterTimestampSkewError(
            status_code=401 if exc.code.value == "unauthenticated" else None
        )
    error_message = exc.message or _EMPTY_ERROR_MESSAGE
    if exc.details:
        for detail in exc.details:
            unpacked = _unpack_error_detail(detail)
            if unpacked is None:
                continue
            full_name = unpacked.DESCRIPTOR.full_name
            if full_name == "auth.v1.AuthErrorDetail":
                code_name = error_code_name(auth_pb2.AuthErrorCode, unpacked.code)
                message = unpacked.message or error_message
                return PolyesterApiError(message, code=code_name, raw=unpacked)
            if full_name == "polyester.ratelimit.v1.RateLimitDetail":
                return _rate_limit_error(error_message, proto_detail=unpacked)
            if full_name == "orders.v1.ErrorDetail":
                code_name = error_code_name(orders_pb2.ErrorCode, unpacked.code)
                rate_limit = unpacked.rate_limit if unpacked.HasField("rate_limit") else None
                if rate_limit is not None or code_name == "ERROR_CODE_RATE_LIMIT_EXCEEDED":
                    return _rate_limit_error(error_message, proto_detail=rate_limit)
                if (
                    "POLICY" in code_name
                    or "UNAUTHENTICATED" in code_name
                    or "PERMISSION" in code_name
                ):
                    return PolyesterAuthError(error_message)
                return PolyesterApiError(
                    error_message,
                    code=code_name,
                    raw=unpacked,
                    existing_order_id=(
                        format_uint64_id(unpacked.existing_order_id)
                        if unpacked.existing_order_id
                        else None
                    ),
                )
            if full_name == "chain.withdraw.v1.ErrorDetail":
                code_name = error_code_name(withdraw_pb2.ErrorCode, unpacked.code)
                if (
                    "UNAUTHENTICATED" in code_name
                    or "PERMISSION" in code_name
                    or "API_KEY" in code_name
                    or "WALLET_BINDING" in code_name
                ):
                    return PolyesterAuthError(error_message)
                if code_name == "ERROR_CODE_RATE_LIMIT_EXCEEDED":
                    return _rate_limit_error(error_message)
                return PolyesterApiError(error_message, code=code_name)
            if full_name == "transfer.v1.ErrorDetail":
                code_name = error_code_name(transfer_pb2.ErrorCode, unpacked.code)
                if (
                    "UNAUTHENTICATED" in code_name
                    or "PERMISSION" in code_name
                    or "POLICY" in code_name
                ):
                    return PolyesterAuthError(error_message)
                if code_name == "ERROR_CODE_RATE_LIMIT_EXCEEDED":
                    return _rate_limit_error(error_message)
                return PolyesterApiError(error_message, code=code_name)
    code = exc.code.value
    if is_cloudflare_browser_ban(error_message):
        return PolyesterTransportError(cloudflare_1010_message())
    if code in ("unauthenticated", "permission_denied"):
        return PolyesterAuthError(error_message)
    if code in ("unavailable", "internal"):
        return PolyesterServerError(error_message)
    if code == "resource_exhausted":
        # connectrpc-python does not currently retain response metadata on
        # ConnectError, so header retry_after cannot be recovered on this path.
        # Structured RateLimitDetail above populates retry_after when attached.
        return PolyesterRateLimitError(error_message)
    if code == "deadline_exceeded":
        return PolyesterTimeoutError(error_message)
    message = (exc.message or "").strip().lower()
    if code == "unimplemented" and message in _ROUTE_NOT_FOUND_MESSAGES:
        return PolyesterRouteNotFoundError()
    if code == "unimplemented" or (code == "unknown" and exc.message == _HTTP_501_PHRASE):
        return PolyesterNotImplementedError(error_message)
    return PolyesterApiError(error_message, code=code)
