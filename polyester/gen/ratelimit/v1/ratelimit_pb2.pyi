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

class TradingRateLimitClass(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TRADING_RATE_LIMIT_CLASS_UNSPECIFIED: _ClassVar[TradingRateLimitClass]
    TRADING_RATE_LIMIT_CLASS_PLACE: _ClassVar[TradingRateLimitClass]
    TRADING_RATE_LIMIT_CLASS_CANCEL: _ClassVar[TradingRateLimitClass]
TRADING_RATE_LIMIT_CLASS_UNSPECIFIED: TradingRateLimitClass
TRADING_RATE_LIMIT_CLASS_PLACE: TradingRateLimitClass
TRADING_RATE_LIMIT_CLASS_CANCEL: TradingRateLimitClass

class TradingRateLimitRule(_message.Message):
    __slots__ = ("policy_class", "vip_tier", "quota_weight", "period_ms", "burst_weight")
    POLICY_CLASS_FIELD_NUMBER: _ClassVar[int]
    VIP_TIER_FIELD_NUMBER: _ClassVar[int]
    QUOTA_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    PERIOD_MS_FIELD_NUMBER: _ClassVar[int]
    BURST_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    policy_class: TradingRateLimitClass
    vip_tier: int
    quota_weight: int
    period_ms: int
    burst_weight: int
    def __init__(self, policy_class: _Optional[_Union[TradingRateLimitClass, str]] = ..., vip_tier: _Optional[int] = ..., quota_weight: _Optional[int] = ..., period_ms: _Optional[int] = ..., burst_weight: _Optional[int] = ...) -> None: ...

class GetRateLimitConfigRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetRateLimitConfigResponse(_message.Message):
    __slots__ = ("policy_version", "effective_from", "rules")
    POLICY_VERSION_FIELD_NUMBER: _ClassVar[int]
    EFFECTIVE_FROM_FIELD_NUMBER: _ClassVar[int]
    RULES_FIELD_NUMBER: _ClassVar[int]
    policy_version: int
    effective_from: _timestamp_pb2.Timestamp
    rules: _containers.RepeatedCompositeFieldContainer[TradingRateLimitRule]
    def __init__(self, policy_version: _Optional[int] = ..., effective_from: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., rules: _Optional[_Iterable[_Union[TradingRateLimitRule, _Mapping]]] = ...) -> None: ...

class GetTradingRateLimitsRequest(_message.Message):
    __slots__ = ("subaccount_id",)
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    def __init__(self, subaccount_id: _Optional[int] = ...) -> None: ...

class GetTradingRateLimitsResponse(_message.Message):
    __slots__ = ("policy_version", "effective_from", "rules", "api_key_rules")
    POLICY_VERSION_FIELD_NUMBER: _ClassVar[int]
    EFFECTIVE_FROM_FIELD_NUMBER: _ClassVar[int]
    RULES_FIELD_NUMBER: _ClassVar[int]
    API_KEY_RULES_FIELD_NUMBER: _ClassVar[int]
    policy_version: int
    effective_from: _timestamp_pb2.Timestamp
    rules: _containers.RepeatedCompositeFieldContainer[TradingRateLimitRule]
    api_key_rules: _containers.RepeatedCompositeFieldContainer[TradingRateLimitRule]
    def __init__(self, policy_version: _Optional[int] = ..., effective_from: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., rules: _Optional[_Iterable[_Union[TradingRateLimitRule, _Mapping]]] = ..., api_key_rules: _Optional[_Iterable[_Union[TradingRateLimitRule, _Mapping]]] = ...) -> None: ...
