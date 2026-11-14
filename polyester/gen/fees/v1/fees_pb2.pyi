from polyester.gen.buf.validate import validate_pb2 as _validate_pb2
from polyester.gen.gnostic.openapi.v3 import annotations_pb2 as _annotations_pb2
from polyester.gen.google.api import annotations_pb2 as _annotations_pb2_1
from polyester.gen.polyester.api import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SpotFeeRate(_message.Message):
    __slots__ = ("symbol_id", "maker_fee_rate_percent", "taker_fee_rate_percent", "vip_tier")
    SYMBOL_ID_FIELD_NUMBER: _ClassVar[int]
    MAKER_FEE_RATE_PERCENT_FIELD_NUMBER: _ClassVar[int]
    TAKER_FEE_RATE_PERCENT_FIELD_NUMBER: _ClassVar[int]
    VIP_TIER_FIELD_NUMBER: _ClassVar[int]
    symbol_id: int
    maker_fee_rate_percent: str
    taker_fee_rate_percent: str
    vip_tier: int
    def __init__(self, symbol_id: _Optional[int] = ..., maker_fee_rate_percent: _Optional[str] = ..., taker_fee_rate_percent: _Optional[str] = ..., vip_tier: _Optional[int] = ...) -> None: ...

class GetSpotFeeRatesRequest(_message.Message):
    __slots__ = ("subaccount_id", "symbol_id")
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_ID_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    symbol_id: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, subaccount_id: _Optional[int] = ..., symbol_id: _Optional[_Iterable[int]] = ...) -> None: ...

class GetSpotFeeRatesResponse(_message.Message):
    __slots__ = ("fee_rates",)
    FEE_RATES_FIELD_NUMBER: _ClassVar[int]
    fee_rates: _containers.RepeatedCompositeFieldContainer[SpotFeeRate]
    def __init__(self, fee_rates: _Optional[_Iterable[_Union[SpotFeeRate, _Mapping]]] = ...) -> None: ...
