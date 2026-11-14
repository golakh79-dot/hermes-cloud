import datetime

from polyester.gen.buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from polyester.gen.polyester.api import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class HeatmapInterval(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INTERVAL_UNSPECIFIED: _ClassVar[HeatmapInterval]
    INTERVAL_1S: _ClassVar[HeatmapInterval]
    INTERVAL_1M: _ClassVar[HeatmapInterval]
    INTERVAL_5M: _ClassVar[HeatmapInterval]
    INTERVAL_1H: _ClassVar[HeatmapInterval]

class HeatmapDepth(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DEPTH_UNSPECIFIED: _ClassVar[HeatmapDepth]
    DEPTH_1: _ClassVar[HeatmapDepth]
    DEPTH_5: _ClassVar[HeatmapDepth]
    DEPTH_10: _ClassVar[HeatmapDepth]
    DEPTH_20: _ClassVar[HeatmapDepth]
    DEPTH_50: _ClassVar[HeatmapDepth]
    DEPTH_100: _ClassVar[HeatmapDepth]
    DEPTH_200: _ClassVar[HeatmapDepth]
    DEPTH_500: _ClassVar[HeatmapDepth]
    DEPTH_1000: _ClassVar[HeatmapDepth]

class HeatmapQuantityMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    QTY_MODE_UNSPECIFIED: _ClassVar[HeatmapQuantityMode]
    CLOSE: _ClassVar[HeatmapQuantityMode]
    PEAK: _ClassVar[HeatmapQuantityMode]
INTERVAL_UNSPECIFIED: HeatmapInterval
INTERVAL_1S: HeatmapInterval
INTERVAL_1M: HeatmapInterval
INTERVAL_5M: HeatmapInterval
INTERVAL_1H: HeatmapInterval
DEPTH_UNSPECIFIED: HeatmapDepth
DEPTH_1: HeatmapDepth
DEPTH_5: HeatmapDepth
DEPTH_10: HeatmapDepth
DEPTH_20: HeatmapDepth
DEPTH_50: HeatmapDepth
DEPTH_100: HeatmapDepth
DEPTH_200: HeatmapDepth
DEPTH_500: HeatmapDepth
DEPTH_1000: HeatmapDepth
QTY_MODE_UNSPECIFIED: HeatmapQuantityMode
CLOSE: HeatmapQuantityMode
PEAK: HeatmapQuantityMode

class HeatmapTimeRange(_message.Message):
    __slots__ = ("start_time", "end_time")
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    def __init__(self, start_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class GetOrderbookHeatmapRequest(_message.Message):
    __slots__ = ("symbol_id", "interval", "depth", "time_range", "page_token", "limit", "quantity_mode")
    SYMBOL_ID_FIELD_NUMBER: _ClassVar[int]
    INTERVAL_FIELD_NUMBER: _ClassVar[int]
    DEPTH_FIELD_NUMBER: _ClassVar[int]
    TIME_RANGE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_MODE_FIELD_NUMBER: _ClassVar[int]
    symbol_id: int
    interval: HeatmapInterval
    depth: HeatmapDepth
    time_range: HeatmapTimeRange
    page_token: str
    limit: int
    quantity_mode: HeatmapQuantityMode
    def __init__(self, symbol_id: _Optional[int] = ..., interval: _Optional[_Union[HeatmapInterval, str]] = ..., depth: _Optional[_Union[HeatmapDepth, str]] = ..., time_range: _Optional[_Union[HeatmapTimeRange, _Mapping]] = ..., page_token: _Optional[str] = ..., limit: _Optional[int] = ..., quantity_mode: _Optional[_Union[HeatmapQuantityMode, str]] = ...) -> None: ...

class HeatmapLevels(_message.Message):
    __slots__ = ("price_ticks", "qty_scaled")
    PRICE_TICKS_FIELD_NUMBER: _ClassVar[int]
    QTY_SCALED_FIELD_NUMBER: _ClassVar[int]
    price_ticks: _containers.RepeatedScalarFieldContainer[int]
    qty_scaled: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, price_ticks: _Optional[_Iterable[int]] = ..., qty_scaled: _Optional[_Iterable[int]] = ...) -> None: ...

class HeatmapDeltaLevels(_message.Message):
    __slots__ = ("price_ticks", "qty_scaled")
    PRICE_TICKS_FIELD_NUMBER: _ClassVar[int]
    QTY_SCALED_FIELD_NUMBER: _ClassVar[int]
    price_ticks: _containers.RepeatedScalarFieldContainer[int]
    qty_scaled: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, price_ticks: _Optional[_Iterable[int]] = ..., qty_scaled: _Optional[_Iterable[int]] = ...) -> None: ...

class HeatmapKeyframe(_message.Message):
    __slots__ = ("ts_sec", "best_bid_ticks", "best_ask_ticks", "mid_ticks", "bids", "asks", "book_seq")
    TS_SEC_FIELD_NUMBER: _ClassVar[int]
    BEST_BID_TICKS_FIELD_NUMBER: _ClassVar[int]
    BEST_ASK_TICKS_FIELD_NUMBER: _ClassVar[int]
    MID_TICKS_FIELD_NUMBER: _ClassVar[int]
    BIDS_FIELD_NUMBER: _ClassVar[int]
    ASKS_FIELD_NUMBER: _ClassVar[int]
    BOOK_SEQ_FIELD_NUMBER: _ClassVar[int]
    ts_sec: int
    best_bid_ticks: int
    best_ask_ticks: int
    mid_ticks: int
    bids: HeatmapLevels
    asks: HeatmapLevels
    book_seq: int
    def __init__(self, ts_sec: _Optional[int] = ..., best_bid_ticks: _Optional[int] = ..., best_ask_ticks: _Optional[int] = ..., mid_ticks: _Optional[int] = ..., bids: _Optional[_Union[HeatmapLevels, _Mapping]] = ..., asks: _Optional[_Union[HeatmapLevels, _Mapping]] = ..., book_seq: _Optional[int] = ...) -> None: ...

class HeatmapDeltaBucket(_message.Message):
    __slots__ = ("ts_sec", "bids", "asks", "updates_in_bucket", "book_seq_start", "book_seq_end")
    TS_SEC_FIELD_NUMBER: _ClassVar[int]
    BIDS_FIELD_NUMBER: _ClassVar[int]
    ASKS_FIELD_NUMBER: _ClassVar[int]
    UPDATES_IN_BUCKET_FIELD_NUMBER: _ClassVar[int]
    BOOK_SEQ_START_FIELD_NUMBER: _ClassVar[int]
    BOOK_SEQ_END_FIELD_NUMBER: _ClassVar[int]
    ts_sec: int
    bids: HeatmapDeltaLevels
    asks: HeatmapDeltaLevels
    updates_in_bucket: int
    book_seq_start: int
    book_seq_end: int
    def __init__(self, ts_sec: _Optional[int] = ..., bids: _Optional[_Union[HeatmapDeltaLevels, _Mapping]] = ..., asks: _Optional[_Union[HeatmapDeltaLevels, _Mapping]] = ..., updates_in_bucket: _Optional[int] = ..., book_seq_start: _Optional[int] = ..., book_seq_end: _Optional[int] = ...) -> None: ...

class HeatmapLiveBucket(_message.Message):
    __slots__ = ("symbol_id", "interval", "ts_sec", "is_final", "bids", "asks", "updates_in_bucket", "book_seq_start", "book_seq_end", "quantity_mode", "effective_bin_ticks")
    SYMBOL_ID_FIELD_NUMBER: _ClassVar[int]
    INTERVAL_FIELD_NUMBER: _ClassVar[int]
    TS_SEC_FIELD_NUMBER: _ClassVar[int]
    IS_FINAL_FIELD_NUMBER: _ClassVar[int]
    BIDS_FIELD_NUMBER: _ClassVar[int]
    ASKS_FIELD_NUMBER: _ClassVar[int]
    UPDATES_IN_BUCKET_FIELD_NUMBER: _ClassVar[int]
    BOOK_SEQ_START_FIELD_NUMBER: _ClassVar[int]
    BOOK_SEQ_END_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_MODE_FIELD_NUMBER: _ClassVar[int]
    EFFECTIVE_BIN_TICKS_FIELD_NUMBER: _ClassVar[int]
    symbol_id: int
    interval: HeatmapInterval
    ts_sec: int
    is_final: bool
    bids: HeatmapDeltaLevels
    asks: HeatmapDeltaLevels
    updates_in_bucket: int
    book_seq_start: int
    book_seq_end: int
    quantity_mode: HeatmapQuantityMode
    effective_bin_ticks: int
    def __init__(self, symbol_id: _Optional[int] = ..., interval: _Optional[_Union[HeatmapInterval, str]] = ..., ts_sec: _Optional[int] = ..., is_final: _Optional[bool] = ..., bids: _Optional[_Union[HeatmapDeltaLevels, _Mapping]] = ..., asks: _Optional[_Union[HeatmapDeltaLevels, _Mapping]] = ..., updates_in_bucket: _Optional[int] = ..., book_seq_start: _Optional[int] = ..., book_seq_end: _Optional[int] = ..., quantity_mode: _Optional[_Union[HeatmapQuantityMode, str]] = ..., effective_bin_ticks: _Optional[int] = ...) -> None: ...

class HeatmapDeltaChain(_message.Message):
    __slots__ = ("base_keyframe", "deltas")
    BASE_KEYFRAME_FIELD_NUMBER: _ClassVar[int]
    DELTAS_FIELD_NUMBER: _ClassVar[int]
    base_keyframe: HeatmapKeyframe
    deltas: _containers.RepeatedCompositeFieldContainer[HeatmapDeltaBucket]
    def __init__(self, base_keyframe: _Optional[_Union[HeatmapKeyframe, _Mapping]] = ..., deltas: _Optional[_Iterable[_Union[HeatmapDeltaBucket, _Mapping]]] = ...) -> None: ...

class GetOrderbookHeatmapResponse(_message.Message):
    __slots__ = ("symbol_id", "interval", "depth", "chain", "last_persisted_ts_sec", "live_from_book_seq_end", "has_live_anchor", "next_page_token", "server_time_sec", "quantity_mode", "live_bucket")
    SYMBOL_ID_FIELD_NUMBER: _ClassVar[int]
    INTERVAL_FIELD_NUMBER: _ClassVar[int]
    DEPTH_FIELD_NUMBER: _ClassVar[int]
    CHAIN_FIELD_NUMBER: _ClassVar[int]
    LAST_PERSISTED_TS_SEC_FIELD_NUMBER: _ClassVar[int]
    LIVE_FROM_BOOK_SEQ_END_FIELD_NUMBER: _ClassVar[int]
    HAS_LIVE_ANCHOR_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    SERVER_TIME_SEC_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_MODE_FIELD_NUMBER: _ClassVar[int]
    LIVE_BUCKET_FIELD_NUMBER: _ClassVar[int]
    symbol_id: int
    interval: HeatmapInterval
    depth: HeatmapDepth
    chain: HeatmapDeltaChain
    last_persisted_ts_sec: int
    live_from_book_seq_end: int
    has_live_anchor: bool
    next_page_token: str
    server_time_sec: int
    quantity_mode: HeatmapQuantityMode
    live_bucket: HeatmapLiveBucket
    def __init__(self, symbol_id: _Optional[int] = ..., interval: _Optional[_Union[HeatmapInterval, str]] = ..., depth: _Optional[_Union[HeatmapDepth, str]] = ..., chain: _Optional[_Union[HeatmapDeltaChain, _Mapping]] = ..., last_persisted_ts_sec: _Optional[int] = ..., live_from_book_seq_end: _Optional[int] = ..., has_live_anchor: _Optional[bool] = ..., next_page_token: _Optional[str] = ..., server_time_sec: _Optional[int] = ..., quantity_mode: _Optional[_Union[HeatmapQuantityMode, str]] = ..., live_bucket: _Optional[_Union[HeatmapLiveBucket, _Mapping]] = ...) -> None: ...
