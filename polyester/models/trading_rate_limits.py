from __future__ import annotations

from datetime import datetime

import msgspec


class TradingRateLimitRule(msgspec.Struct, kw_only=True, omit_defaults=True):
    """Weighted placement or cancellation quota for one VIP tier."""

    policy_class: str = ""
    vip_tier: int = 0
    quota_weight: int = 0
    period_ms: int = 0
    burst_weight: int = 0


class RateLimitConfig(msgspec.Struct, kw_only=True, omit_defaults=True):
    """Complete public trading rate-limit catalog for one policy version."""

    policy_version: int = 0
    effective_from: datetime | None = None
    rules: list[TradingRateLimitRule]


class TradingRateLimits(msgspec.Struct, kw_only=True, omit_defaults=True):
    """Effective trading limits for one account target and caller."""

    policy_version: int = 0
    effective_from: datetime | None = None
    rules: list[TradingRateLimitRule]
    api_key_rules: list[TradingRateLimitRule]
