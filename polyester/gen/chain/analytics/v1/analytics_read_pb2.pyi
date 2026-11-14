from polyester.gen.buf.validate import validate_pb2 as _validate_pb2
from polyester.gen.gnostic.openapi.v3 import annotations_pb2 as _annotations_pb2
from polyester.gen.google.api import annotations_pb2 as _annotations_pb2_1
from polyester.gen.polyester.api import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ChainAnalyticsRange(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RANGE_UNSPECIFIED: _ClassVar[ChainAnalyticsRange]
    DAY_1: _ClassVar[ChainAnalyticsRange]
    DAY_7: _ClassVar[ChainAnalyticsRange]
    DAY_30: _ClassVar[ChainAnalyticsRange]
    DAY_90: _ClassVar[ChainAnalyticsRange]
    DAY_180: _ClassVar[ChainAnalyticsRange]
    DAY_365: _ClassVar[ChainAnalyticsRange]
RANGE_UNSPECIFIED: ChainAnalyticsRange
DAY_1: ChainAnalyticsRange
DAY_7: ChainAnalyticsRange
DAY_30: ChainAnalyticsRange
DAY_90: ChainAnalyticsRange
DAY_180: ChainAnalyticsRange
DAY_365: ChainAnalyticsRange

class GetZippedAssetSupplyRequest(_message.Message):
    __slots__ = ("zipped_asset_id", "range", "bucket", "start_ts_sec", "end_ts_sec")
    ZIPPED_ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    RANGE_FIELD_NUMBER: _ClassVar[int]
    BUCKET_FIELD_NUMBER: _ClassVar[int]
    START_TS_SEC_FIELD_NUMBER: _ClassVar[int]
    END_TS_SEC_FIELD_NUMBER: _ClassVar[int]
    zipped_asset_id: int
    range: ChainAnalyticsRange
    bucket: str
    start_ts_sec: int
    end_ts_sec: int
    def __init__(self, zipped_asset_id: _Optional[int] = ..., range: _Optional[_Union[ChainAnalyticsRange, str]] = ..., bucket: _Optional[str] = ..., start_ts_sec: _Optional[int] = ..., end_ts_sec: _Optional[int] = ...) -> None: ...

class GetZippedAssetSupplyResponse(_message.Message):
    __slots__ = ("zipped_asset_id", "range", "bucket", "start_ts_sec", "end_ts_sec", "points", "total_supply_q")
    ZIPPED_ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    RANGE_FIELD_NUMBER: _ClassVar[int]
    BUCKET_FIELD_NUMBER: _ClassVar[int]
    START_TS_SEC_FIELD_NUMBER: _ClassVar[int]
    END_TS_SEC_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SUPPLY_Q_FIELD_NUMBER: _ClassVar[int]
    zipped_asset_id: int
    range: ChainAnalyticsRange
    bucket: str
    start_ts_sec: int
    end_ts_sec: int
    points: int
    total_supply_q: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, zipped_asset_id: _Optional[int] = ..., range: _Optional[_Union[ChainAnalyticsRange, str]] = ..., bucket: _Optional[str] = ..., start_ts_sec: _Optional[int] = ..., end_ts_sec: _Optional[int] = ..., points: _Optional[int] = ..., total_supply_q: _Optional[_Iterable[int]] = ...) -> None: ...

class ZippedAssetSupplySeries(_message.Message):
    __slots__ = ("zipped_asset_id", "total_supply_q")
    ZIPPED_ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SUPPLY_Q_FIELD_NUMBER: _ClassVar[int]
    zipped_asset_id: int
    total_supply_q: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, zipped_asset_id: _Optional[int] = ..., total_supply_q: _Optional[_Iterable[int]] = ...) -> None: ...

class GetZippedAssetSupplyGroupRequest(_message.Message):
    __slots__ = ("group_id", "range", "bucket", "start_ts_sec", "end_ts_sec")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    RANGE_FIELD_NUMBER: _ClassVar[int]
    BUCKET_FIELD_NUMBER: _ClassVar[int]
    START_TS_SEC_FIELD_NUMBER: _ClassVar[int]
    END_TS_SEC_FIELD_NUMBER: _ClassVar[int]
    group_id: str
    range: ChainAnalyticsRange
    bucket: str
    start_ts_sec: int
    end_ts_sec: int
    def __init__(self, group_id: _Optional[str] = ..., range: _Optional[_Union[ChainAnalyticsRange, str]] = ..., bucket: _Optional[str] = ..., start_ts_sec: _Optional[int] = ..., end_ts_sec: _Optional[int] = ...) -> None: ...

class GetZippedAssetSupplyGroupResponse(_message.Message):
    __slots__ = ("group_id", "range", "bucket", "start_ts_sec", "end_ts_sec", "points", "series")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    RANGE_FIELD_NUMBER: _ClassVar[int]
    BUCKET_FIELD_NUMBER: _ClassVar[int]
    START_TS_SEC_FIELD_NUMBER: _ClassVar[int]
    END_TS_SEC_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    SERIES_FIELD_NUMBER: _ClassVar[int]
    group_id: str
    range: ChainAnalyticsRange
    bucket: str
    start_ts_sec: int
    end_ts_sec: int
    points: int
    series: _containers.RepeatedCompositeFieldContainer[ZippedAssetSupplySeries]
    def __init__(self, group_id: _Optional[str] = ..., range: _Optional[_Union[ChainAnalyticsRange, str]] = ..., bucket: _Optional[str] = ..., start_ts_sec: _Optional[int] = ..., end_ts_sec: _Optional[int] = ..., points: _Optional[int] = ..., series: _Optional[_Iterable[_Union[ZippedAssetSupplySeries, _Mapping]]] = ...) -> None: ...

class GetUnifiedAssetBalancesRequest(_message.Message):
    __slots__ = ("asset_id", "range", "bucket", "start_ts_sec", "end_ts_sec")
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    RANGE_FIELD_NUMBER: _ClassVar[int]
    BUCKET_FIELD_NUMBER: _ClassVar[int]
    START_TS_SEC_FIELD_NUMBER: _ClassVar[int]
    END_TS_SEC_FIELD_NUMBER: _ClassVar[int]
    asset_id: int
    range: ChainAnalyticsRange
    bucket: str
    start_ts_sec: int
    end_ts_sec: int
    def __init__(self, asset_id: _Optional[int] = ..., range: _Optional[_Union[ChainAnalyticsRange, str]] = ..., bucket: _Optional[str] = ..., start_ts_sec: _Optional[int] = ..., end_ts_sec: _Optional[int] = ...) -> None: ...

class GetUnifiedAssetBalancesResponse(_message.Message):
    __slots__ = ("asset_id", "range", "bucket", "start_ts_sec", "end_ts_sec", "points", "total_balance_q")
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    RANGE_FIELD_NUMBER: _ClassVar[int]
    BUCKET_FIELD_NUMBER: _ClassVar[int]
    START_TS_SEC_FIELD_NUMBER: _ClassVar[int]
    END_TS_SEC_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_BALANCE_Q_FIELD_NUMBER: _ClassVar[int]
    asset_id: int
    range: ChainAnalyticsRange
    bucket: str
    start_ts_sec: int
    end_ts_sec: int
    points: int
    total_balance_q: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, asset_id: _Optional[int] = ..., range: _Optional[_Union[ChainAnalyticsRange, str]] = ..., bucket: _Optional[str] = ..., start_ts_sec: _Optional[int] = ..., end_ts_sec: _Optional[int] = ..., points: _Optional[int] = ..., total_balance_q: _Optional[_Iterable[int]] = ...) -> None: ...
