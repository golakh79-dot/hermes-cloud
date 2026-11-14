from __future__ import annotations

from datetime import UTC, datetime

from polyester.codecs.proto_helpers import has_field, proto_enum_name
from polyester.gen.vip.v1 import vip_pb2
from polyester.models.vip import (
    NextVIPTierThresholds,
    VIPMetricQuality,
    VIPStatus,
    VIPTier,
    VIPTiersList,
)


def _timestamp(ts) -> datetime | None:
    if ts is None:
        return None
    seconds = int(getattr(ts, "seconds", 0) or 0)
    nanos = int(getattr(ts, "nanos", 0) or 0)
    if seconds == 0 and nanos == 0:
        return None
    return datetime.fromtimestamp(seconds + nanos / 1_000_000_000, tz=UTC)


def vip_tier_from_proto(msg: vip_pb2.VIPTier) -> VIPTier:
    aop = None
    if has_field(msg, "aop_threshold_usd"):
        aop = msg.aop_threshold_usd
    return VIPTier(
        tier=int(msg.tier),
        volume_threshold_usd=msg.volume_threshold_usd or "",
        aop_threshold_usd=aop,
        maker_fee_rate_percent=msg.maker_fee_rate_percent or "",
        taker_fee_rate_percent=msg.taker_fee_rate_percent or "",
    )


def vip_tiers_list_from_proto(msg: vip_pb2.ListVIPTiersResponse) -> VIPTiersList:
    return VIPTiersList(
        policy_version=int(msg.policy_version),
        effective_from=_timestamp(msg.effective_from)
        if has_field(msg, "effective_from")
        else None,
        retention_threshold_bp=int(msg.retention_threshold_bp),
        tiers=[vip_tier_from_proto(item) for item in msg.tiers],
    )


def next_vip_tier_thresholds_from_proto(
    msg: vip_pb2.NextVIPTierThresholds,
) -> NextVIPTierThresholds:
    return NextVIPTierThresholds(
        tier=int(msg.tier),
        volume_threshold_usd=msg.volume_threshold_usd or "",
        aop_threshold_usd=msg.aop_threshold_usd or "",
    )


def _metric_quality(msg: vip_pb2.GetVIPStatusResponse, field: str) -> VIPMetricQuality | None:
    if not has_field(msg, field):
        return None
    quality = getattr(msg, field)
    status = proto_enum_name(vip_pb2.VIPMetricStatus, quality.status)
    return VIPMetricQuality(
        status=status.removeprefix("metric_"),
        incomplete_hours=int(quality.incomplete_hours),
    )


def vip_status_from_proto(msg: vip_pb2.GetVIPStatusResponse) -> VIPStatus:
    next_thresholds = None
    if has_field(msg, "next_tier_thresholds"):
        next_thresholds = next_vip_tier_thresholds_from_proto(msg.next_tier_thresholds)
    return VIPStatus(
        tier=int(msg.tier),
        volume_tier=int(msg.volume_tier),
        aop_tier=int(msg.aop_tier),
        settled_volume_30d_usd=msg.settled_volume_30d_usd
        if has_field(msg, "settled_volume_30d_usd")
        else None,
        average_aop_30d_usd=msg.average_aop_30d_usd
        if has_field(msg, "average_aop_30d_usd")
        else None,
        policy_version=int(msg.policy_version),
        policy_effective_from=_timestamp(msg.policy_effective_from)
        if has_field(msg, "policy_effective_from")
        else None,
        effective_from=_timestamp(msg.effective_from)
        if has_field(msg, "effective_from")
        else None,
        evaluated_at=_timestamp(msg.evaluated_at)
        if has_field(msg, "evaluated_at")
        else None,
        metrics_as_of=_timestamp(msg.metrics_as_of)
        if has_field(msg, "metrics_as_of")
        else None,
        next_tier_thresholds=next_thresholds,
        settled_volume_quality=_metric_quality(msg, "settled_volume_quality"),
        average_aop_quality=_metric_quality(msg, "average_aop_quality"),
    )
