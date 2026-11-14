from __future__ import annotations

from datetime import datetime

import msgspec


class VIPTier(msgspec.Struct, kw_only=True, omit_defaults=True):
    """One VIP0–VIP10 catalog row."""

    tier: int = 0
    volume_threshold_usd: str = ""
    aop_threshold_usd: str | None = None
    maker_fee_rate_percent: str = ""
    taker_fee_rate_percent: str = ""


class VIPTiersList(msgspec.Struct, kw_only=True, omit_defaults=True):
    """Complete active VIP policy catalog."""

    policy_version: int = 0
    effective_from: datetime | None = None
    retention_threshold_bp: int = 0
    tiers: list[VIPTier]


class NextVIPTierThresholds(msgspec.Struct, kw_only=True, omit_defaults=True):
    """Entry thresholds for the tier immediately above the effective tier."""

    tier: int = 0
    volume_threshold_usd: str = ""
    aop_threshold_usd: str = ""


class VIPMetricQuality(msgspec.Struct, kw_only=True, omit_defaults=True):
    """Completeness of one rolling 30-day VIP metric.

    ``status`` is ``complete``, ``price_unavailable`` (every hour is present,
    but some contributions had no USD reference price, so the metric is a
    lower bound) or ``incomplete_history`` (some hours are missing).
    ``incomplete_hours`` counts the incomplete hourly buckets of the 720.
    """

    status: str = ""
    incomplete_hours: int = 0


class VIPStatus(msgspec.Struct, kw_only=True, omit_defaults=True):
    """Authenticated caller-root VIP assignment and qualification facts.

    ``settled_volume_quality`` and ``average_aop_quality`` say how complete
    each 30-day metric is; both are ``None`` when the assignment carries no
    qualification evidence (for example a new account's default tier).
    """

    tier: int = 0
    volume_tier: int = 0
    aop_tier: int = 0
    settled_volume_30d_usd: str | None = None
    average_aop_30d_usd: str | None = None
    policy_version: int = 0
    policy_effective_from: datetime | None = None
    effective_from: datetime | None = None
    evaluated_at: datetime | None = None
    metrics_as_of: datetime | None = None
    next_tier_thresholds: NextVIPTierThresholds | None = None
    settled_volume_quality: VIPMetricQuality | None = None
    average_aop_quality: VIPMetricQuality | None = None
