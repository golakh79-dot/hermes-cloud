from __future__ import annotations

from datetime import UTC, datetime

from polyester.codecs.proto_helpers import has_field
from polyester.gen.ratelimit.v1 import ratelimit_pb2
from polyester.models.trading_rate_limits import (
    RateLimitConfig,
    TradingRateLimitRule,
    TradingRateLimits,
)


def _enum_label(enum_cls: object, raw: int, *, unknown_prefix: str) -> str:
    try:
        return enum_cls.Name(raw)  # type: ignore[attr-defined]
    except (ValueError, TypeError):
        return f"{unknown_prefix}({raw})"


def _timestamp(ts) -> datetime | None:
    if ts is None:
        return None
    seconds = int(getattr(ts, "seconds", 0) or 0)
    nanos = int(getattr(ts, "nanos", 0) or 0)
    if seconds == 0 and nanos == 0:
        return None
    return datetime.fromtimestamp(seconds + nanos / 1_000_000_000, tz=UTC)


def trading_rate_limit_rule_from_proto(
    msg: ratelimit_pb2.TradingRateLimitRule,
) -> TradingRateLimitRule:
    return TradingRateLimitRule(
        policy_class=_enum_label(
            ratelimit_pb2.TradingRateLimitClass,
            int(msg.policy_class),
            unknown_prefix="UNKNOWN_TRADING_RATE_LIMIT_CLASS",
        ),
        vip_tier=int(msg.vip_tier),
        quota_weight=int(msg.quota_weight),
        period_ms=int(msg.period_ms),
        burst_weight=int(msg.burst_weight),
    )


def rate_limit_config_from_proto(
    msg: ratelimit_pb2.GetRateLimitConfigResponse,
) -> RateLimitConfig:
    return RateLimitConfig(
        policy_version=int(msg.policy_version),
        effective_from=_timestamp(msg.effective_from)
        if has_field(msg, "effective_from")
        else None,
        rules=[trading_rate_limit_rule_from_proto(item) for item in msg.rules],
    )


def trading_rate_limits_from_proto(
    msg: ratelimit_pb2.GetTradingRateLimitsResponse,
) -> TradingRateLimits:
    return TradingRateLimits(
        policy_version=int(msg.policy_version),
        effective_from=_timestamp(msg.effective_from)
        if has_field(msg, "effective_from")
        else None,
        rules=[trading_rate_limit_rule_from_proto(item) for item in msg.rules],
        api_key_rules=[
            trading_rate_limit_rule_from_proto(item) for item in msg.api_key_rules
        ],
    )
