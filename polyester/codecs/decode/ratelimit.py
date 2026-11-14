from __future__ import annotations

from polyester.gen.polyester.ratelimit.v1 import types_pb2
from polyester.models.ratelimit import RateLimitDetail


def _enum_label(enum_cls: object, raw: int, *, unknown_prefix: str) -> str:
    try:
        return enum_cls.Name(raw)  # type: ignore[attr-defined]
    except (ValueError, TypeError):
        return f"{unknown_prefix}({raw})"


def rate_limit_detail_from_proto(msg: types_pb2.RateLimitDetail | None) -> RateLimitDetail | None:
    if msg is None:
        return None
    return RateLimitDetail(
        reason=_enum_label(
            types_pb2.FailureReason, int(msg.reason), unknown_prefix="UNKNOWN_FAILURE_REASON"
        ),
        limit=int(msg.limit) if msg.HasField("limit") else None,
        remaining=int(msg.remaining) if msg.HasField("remaining") else None,
        retry_after_ms=int(msg.retry_after_ms) if msg.HasField("retry_after_ms") else None,
        policy_version=int(msg.policy_version) if msg.HasField("policy_version") else None,
        operation_id=msg.operation_id or "",
        policy_class=_enum_label(
            types_pb2.PolicyClass, int(msg.policy_class), unknown_prefix="UNKNOWN_POLICY_CLASS"
        ),
        scope=_enum_label(
            types_pb2.LimiterScope, int(msg.scope), unknown_prefix="UNKNOWN_LIMITER_SCOPE"
        ),
        refill_model=_enum_label(
            types_pb2.RefillModel, int(msg.refill_model), unknown_prefix="UNKNOWN_REFILL_MODEL"
        ),
    )


def retry_after_seconds_from_detail(detail: RateLimitDetail | None) -> float | None:
    if detail is None or detail.retry_after_ms is None:
        return None
    return float(detail.retry_after_ms) / 1000.0
