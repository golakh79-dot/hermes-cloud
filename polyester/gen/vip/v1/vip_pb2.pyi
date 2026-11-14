import datetime

from polyester.gen.buf.validate import validate_pb2 as _validate_pb2
from polyester.gen.gnostic.openapi.v3 import annotations_pb2 as _annotations_pb2
from polyester.gen.google.api import annotations_pb2 as _annotations_pb2_1
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from polyester.gen.polyester.api import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VIPMetricStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    METRIC_UNSPECIFIED: _ClassVar[VIPMetricStatus]
    COMPLETE: _ClassVar[VIPMetricStatus]
    PRICE_UNAVAILABLE: _ClassVar[VIPMetricStatus]
    INCOMPLETE_HISTORY: _ClassVar[VIPMetricStatus]
METRIC_UNSPECIFIED: VIPMetricStatus
COMPLETE: VIPMetricStatus
PRICE_UNAVAILABLE: VIPMetricStatus
INCOMPLETE_HISTORY: VIPMetricStatus

class VIPTier(_message.Message):
    __slots__ = ("tier", "volume_threshold_usd", "aop_threshold_usd", "maker_fee_rate_percent", "taker_fee_rate_percent")
    TIER_FIELD_NUMBER: _ClassVar[int]
    VOLUME_THRESHOLD_USD_FIELD_NUMBER: _ClassVar[int]
    AOP_THRESHOLD_USD_FIELD_NUMBER: _ClassVar[int]
    MAKER_FEE_RATE_PERCENT_FIELD_NUMBER: _ClassVar[int]
    TAKER_FEE_RATE_PERCENT_FIELD_NUMBER: _ClassVar[int]
    tier: int
    volume_threshold_usd: str
    aop_threshold_usd: str
    maker_fee_rate_percent: str
    taker_fee_rate_percent: str
    def __init__(self, tier: _Optional[int] = ..., volume_threshold_usd: _Optional[str] = ..., aop_threshold_usd: _Optional[str] = ..., maker_fee_rate_percent: _Optional[str] = ..., taker_fee_rate_percent: _Optional[str] = ...) -> None: ...

class ListVIPTiersRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListVIPTiersResponse(_message.Message):
    __slots__ = ("policy_version", "effective_from", "retention_threshold_bp", "tiers")
    POLICY_VERSION_FIELD_NUMBER: _ClassVar[int]
    EFFECTIVE_FROM_FIELD_NUMBER: _ClassVar[int]
    RETENTION_THRESHOLD_BP_FIELD_NUMBER: _ClassVar[int]
    TIERS_FIELD_NUMBER: _ClassVar[int]
    policy_version: int
    effective_from: _timestamp_pb2.Timestamp
    retention_threshold_bp: int
    tiers: _containers.RepeatedCompositeFieldContainer[VIPTier]
    def __init__(self, policy_version: _Optional[int] = ..., effective_from: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., retention_threshold_bp: _Optional[int] = ..., tiers: _Optional[_Iterable[_Union[VIPTier, _Mapping]]] = ...) -> None: ...

class NextVIPTierThresholds(_message.Message):
    __slots__ = ("tier", "volume_threshold_usd", "aop_threshold_usd")
    TIER_FIELD_NUMBER: _ClassVar[int]
    VOLUME_THRESHOLD_USD_FIELD_NUMBER: _ClassVar[int]
    AOP_THRESHOLD_USD_FIELD_NUMBER: _ClassVar[int]
    tier: int
    volume_threshold_usd: str
    aop_threshold_usd: str
    def __init__(self, tier: _Optional[int] = ..., volume_threshold_usd: _Optional[str] = ..., aop_threshold_usd: _Optional[str] = ...) -> None: ...

class VIPMetricQuality(_message.Message):
    __slots__ = ("status", "incomplete_hours")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    INCOMPLETE_HOURS_FIELD_NUMBER: _ClassVar[int]
    status: VIPMetricStatus
    incomplete_hours: int
    def __init__(self, status: _Optional[_Union[VIPMetricStatus, str]] = ..., incomplete_hours: _Optional[int] = ...) -> None: ...

class GetVIPStatusRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetVIPStatusResponse(_message.Message):
    __slots__ = ("tier", "volume_tier", "aop_tier", "settled_volume_30d_usd", "average_aop_30d_usd", "policy_version", "policy_effective_from", "effective_from", "evaluated_at", "metrics_as_of", "next_tier_thresholds", "settled_volume_quality", "average_aop_quality")
    TIER_FIELD_NUMBER: _ClassVar[int]
    VOLUME_TIER_FIELD_NUMBER: _ClassVar[int]
    AOP_TIER_FIELD_NUMBER: _ClassVar[int]
    SETTLED_VOLUME_30D_USD_FIELD_NUMBER: _ClassVar[int]
    AVERAGE_AOP_30D_USD_FIELD_NUMBER: _ClassVar[int]
    POLICY_VERSION_FIELD_NUMBER: _ClassVar[int]
    POLICY_EFFECTIVE_FROM_FIELD_NUMBER: _ClassVar[int]
    EFFECTIVE_FROM_FIELD_NUMBER: _ClassVar[int]
    EVALUATED_AT_FIELD_NUMBER: _ClassVar[int]
    METRICS_AS_OF_FIELD_NUMBER: _ClassVar[int]
    NEXT_TIER_THRESHOLDS_FIELD_NUMBER: _ClassVar[int]
    SETTLED_VOLUME_QUALITY_FIELD_NUMBER: _ClassVar[int]
    AVERAGE_AOP_QUALITY_FIELD_NUMBER: _ClassVar[int]
    tier: int
    volume_tier: int
    aop_tier: int
    settled_volume_30d_usd: str
    average_aop_30d_usd: str
    policy_version: int
    policy_effective_from: _timestamp_pb2.Timestamp
    effective_from: _timestamp_pb2.Timestamp
    evaluated_at: _timestamp_pb2.Timestamp
    metrics_as_of: _timestamp_pb2.Timestamp
    next_tier_thresholds: NextVIPTierThresholds
    settled_volume_quality: VIPMetricQuality
    average_aop_quality: VIPMetricQuality
    def __init__(self, tier: _Optional[int] = ..., volume_tier: _Optional[int] = ..., aop_tier: _Optional[int] = ..., settled_volume_30d_usd: _Optional[str] = ..., average_aop_30d_usd: _Optional[str] = ..., policy_version: _Optional[int] = ..., policy_effective_from: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., effective_from: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., evaluated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., metrics_as_of: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., next_tier_thresholds: _Optional[_Union[NextVIPTierThresholds, _Mapping]] = ..., settled_volume_quality: _Optional[_Union[VIPMetricQuality, _Mapping]] = ..., average_aop_quality: _Optional[_Union[VIPMetricQuality, _Mapping]] = ...) -> None: ...
