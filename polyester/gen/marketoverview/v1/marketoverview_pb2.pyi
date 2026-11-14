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

class SparklineInterval(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SPARKLINE_INTERVAL_UNSPECIFIED: _ClassVar[SparklineInterval]
    SPARKLINE_1H: _ClassVar[SparklineInterval]
    SPARKLINE_24H: _ClassVar[SparklineInterval]
    SPARKLINE_1W: _ClassVar[SparklineInterval]
    SPARKLINE_1M: _ClassVar[SparklineInterval]

class MarketOrderBy(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MARKET_ORDER_BY_UNSPECIFIED: _ClassVar[MarketOrderBy]
    ORDER_BY_CHANGE_24H_BPS: _ClassVar[MarketOrderBy]
    ORDER_BY_VOLUME_24H_USD: _ClassVar[MarketOrderBy]
    ORDER_BY_LAST_PRICE: _ClassVar[MarketOrderBy]
    ORDER_BY_DATE_ADDED: _ClassVar[MarketOrderBy]

class SortDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SORT_DIRECTION_UNSPECIFIED: _ClassVar[SortDirection]
    SORT_ASC: _ClassVar[SortDirection]
    SORT_DESC: _ClassVar[SortDirection]

class ErrorCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ERROR_CODE_UNSPECIFIED: _ClassVar[ErrorCode]
    ERROR_CODE_BAD_REQUEST: _ClassVar[ErrorCode]
    ERROR_CODE_INVALID_ARGUMENT: _ClassVar[ErrorCode]
    ERROR_CODE_NOT_FOUND: _ClassVar[ErrorCode]
    ERROR_CODE_UNAVAILABLE: _ClassVar[ErrorCode]
    ERROR_CODE_UPSTREAM_ERROR: _ClassVar[ErrorCode]
SPARKLINE_INTERVAL_UNSPECIFIED: SparklineInterval
SPARKLINE_1H: SparklineInterval
SPARKLINE_24H: SparklineInterval
SPARKLINE_1W: SparklineInterval
SPARKLINE_1M: SparklineInterval
MARKET_ORDER_BY_UNSPECIFIED: MarketOrderBy
ORDER_BY_CHANGE_24H_BPS: MarketOrderBy
ORDER_BY_VOLUME_24H_USD: MarketOrderBy
ORDER_BY_LAST_PRICE: MarketOrderBy
ORDER_BY_DATE_ADDED: MarketOrderBy
SORT_DIRECTION_UNSPECIFIED: SortDirection
SORT_ASC: SortDirection
SORT_DESC: SortDirection
ERROR_CODE_UNSPECIFIED: ErrorCode
ERROR_CODE_BAD_REQUEST: ErrorCode
ERROR_CODE_INVALID_ARGUMENT: ErrorCode
ERROR_CODE_NOT_FOUND: ErrorCode
ERROR_CODE_UNAVAILABLE: ErrorCode
ERROR_CODE_UPSTREAM_ERROR: ErrorCode

class ErrorDetail(_message.Message):
    __slots__ = ("code",)
    CODE_FIELD_NUMBER: _ClassVar[int]
    code: ErrorCode
    def __init__(self, code: _Optional[_Union[ErrorCode, str]] = ...) -> None: ...

class Sparkline(_message.Message):
    __slots__ = ("interval", "close_ticks")
    INTERVAL_FIELD_NUMBER: _ClassVar[int]
    CLOSE_TICKS_FIELD_NUMBER: _ClassVar[int]
    interval: SparklineInterval
    close_ticks: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, interval: _Optional[_Union[SparklineInterval, str]] = ..., close_ticks: _Optional[_Iterable[int]] = ...) -> None: ...

class MarketOverview(_message.Message):
    __slots__ = ("symbol_id", "last_price_ticks", "last_trade_ts_ns", "change_24h_bps", "high_24h_ticks", "low_24h_ticks", "volume_24h_base_scaled", "volume_24h_quote_scaled", "volume_24h_usd_scaled", "listed_ts_ns", "best_bid_ticks", "best_bid_qty_scaled", "best_ask_ticks", "best_ask_qty_scaled", "sparklines", "index_price_ticks")
    SYMBOL_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_PRICE_TICKS_FIELD_NUMBER: _ClassVar[int]
    LAST_TRADE_TS_NS_FIELD_NUMBER: _ClassVar[int]
    CHANGE_24H_BPS_FIELD_NUMBER: _ClassVar[int]
    HIGH_24H_TICKS_FIELD_NUMBER: _ClassVar[int]
    LOW_24H_TICKS_FIELD_NUMBER: _ClassVar[int]
    VOLUME_24H_BASE_SCALED_FIELD_NUMBER: _ClassVar[int]
    VOLUME_24H_QUOTE_SCALED_FIELD_NUMBER: _ClassVar[int]
    VOLUME_24H_USD_SCALED_FIELD_NUMBER: _ClassVar[int]
    LISTED_TS_NS_FIELD_NUMBER: _ClassVar[int]
    BEST_BID_TICKS_FIELD_NUMBER: _ClassVar[int]
    BEST_BID_QTY_SCALED_FIELD_NUMBER: _ClassVar[int]
    BEST_ASK_TICKS_FIELD_NUMBER: _ClassVar[int]
    BEST_ASK_QTY_SCALED_FIELD_NUMBER: _ClassVar[int]
    SPARKLINES_FIELD_NUMBER: _ClassVar[int]
    INDEX_PRICE_TICKS_FIELD_NUMBER: _ClassVar[int]
    symbol_id: int
    last_price_ticks: int
    last_trade_ts_ns: int
    change_24h_bps: int
    high_24h_ticks: int
    low_24h_ticks: int
    volume_24h_base_scaled: int
    volume_24h_quote_scaled: int
    volume_24h_usd_scaled: int
    listed_ts_ns: int
    best_bid_ticks: int
    best_bid_qty_scaled: int
    best_ask_ticks: int
    best_ask_qty_scaled: int
    sparklines: _containers.RepeatedCompositeFieldContainer[Sparkline]
    index_price_ticks: int
    def __init__(self, symbol_id: _Optional[int] = ..., last_price_ticks: _Optional[int] = ..., last_trade_ts_ns: _Optional[int] = ..., change_24h_bps: _Optional[int] = ..., high_24h_ticks: _Optional[int] = ..., low_24h_ticks: _Optional[int] = ..., volume_24h_base_scaled: _Optional[int] = ..., volume_24h_quote_scaled: _Optional[int] = ..., volume_24h_usd_scaled: _Optional[int] = ..., listed_ts_ns: _Optional[int] = ..., best_bid_ticks: _Optional[int] = ..., best_bid_qty_scaled: _Optional[int] = ..., best_ask_ticks: _Optional[int] = ..., best_ask_qty_scaled: _Optional[int] = ..., sparklines: _Optional[_Iterable[_Union[Sparkline, _Mapping]]] = ..., index_price_ticks: _Optional[int] = ...) -> None: ...

class ListMarketOverviewRequest(_message.Message):
    __slots__ = ("symbol_id", "limit", "page_token", "order_by", "sort", "include_sparklines", "sparkline_intervals")
    SYMBOL_ID_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    ORDER_BY_FIELD_NUMBER: _ClassVar[int]
    SORT_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_SPARKLINES_FIELD_NUMBER: _ClassVar[int]
    SPARKLINE_INTERVALS_FIELD_NUMBER: _ClassVar[int]
    symbol_id: _containers.RepeatedScalarFieldContainer[int]
    limit: int
    page_token: str
    order_by: MarketOrderBy
    sort: SortDirection
    include_sparklines: bool
    sparkline_intervals: _containers.RepeatedScalarFieldContainer[SparklineInterval]
    def __init__(self, symbol_id: _Optional[_Iterable[int]] = ..., limit: _Optional[int] = ..., page_token: _Optional[str] = ..., order_by: _Optional[_Union[MarketOrderBy, str]] = ..., sort: _Optional[_Union[SortDirection, str]] = ..., include_sparklines: _Optional[bool] = ..., sparkline_intervals: _Optional[_Iterable[_Union[SparklineInterval, str]]] = ...) -> None: ...

class ListMarketOverviewResponse(_message.Message):
    __slots__ = ("markets", "next_page_token")
    MARKETS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    markets: _containers.RepeatedCompositeFieldContainer[MarketOverview]
    next_page_token: str
    def __init__(self, markets: _Optional[_Iterable[_Union[MarketOverview, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class MarketOverviewBatch(_message.Message):
    __slots__ = ("markets", "ts_ns")
    MARKETS_FIELD_NUMBER: _ClassVar[int]
    TS_NS_FIELD_NUMBER: _ClassVar[int]
    markets: _containers.RepeatedCompositeFieldContainer[MarketOverview]
    ts_ns: int
    def __init__(self, markets: _Optional[_Iterable[_Union[MarketOverview, _Mapping]]] = ..., ts_ns: _Optional[int] = ...) -> None: ...

class GetSpotVolumeHistoryRequest(_message.Message):
    __slots__ = ("symbol_id",)
    SYMBOL_ID_FIELD_NUMBER: _ClassVar[int]
    symbol_id: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, symbol_id: _Optional[_Iterable[int]] = ...) -> None: ...

class SpotPairVolumeSeries(_message.Message):
    __slots__ = ("symbol_id", "volume_usd_scaled")
    SYMBOL_ID_FIELD_NUMBER: _ClassVar[int]
    VOLUME_USD_SCALED_FIELD_NUMBER: _ClassVar[int]
    symbol_id: int
    volume_usd_scaled: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, symbol_id: _Optional[int] = ..., volume_usd_scaled: _Optional[_Iterable[int]] = ...) -> None: ...

class GetSpotVolumeHistoryResponse(_message.Message):
    __slots__ = ("bucket", "start_ts_sec", "end_ts_sec", "points", "pairs", "total_volume_usd_scaled")
    BUCKET_FIELD_NUMBER: _ClassVar[int]
    START_TS_SEC_FIELD_NUMBER: _ClassVar[int]
    END_TS_SEC_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    PAIRS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_VOLUME_USD_SCALED_FIELD_NUMBER: _ClassVar[int]
    bucket: str
    start_ts_sec: int
    end_ts_sec: int
    points: int
    pairs: _containers.RepeatedCompositeFieldContainer[SpotPairVolumeSeries]
    total_volume_usd_scaled: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, bucket: _Optional[str] = ..., start_ts_sec: _Optional[int] = ..., end_ts_sec: _Optional[int] = ..., points: _Optional[int] = ..., pairs: _Optional[_Iterable[_Union[SpotPairVolumeSeries, _Mapping]]] = ..., total_volume_usd_scaled: _Optional[_Iterable[int]] = ...) -> None: ...

class CurrencyMetadata(_message.Message):
    __slots__ = ("code", "default_english_name", "symbol", "fraction_digits")
    CODE_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_ENGLISH_NAME_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    FRACTION_DIGITS_FIELD_NUMBER: _ClassVar[int]
    code: str
    default_english_name: str
    symbol: str
    fraction_digits: int
    def __init__(self, code: _Optional[str] = ..., default_english_name: _Optional[str] = ..., symbol: _Optional[str] = ..., fraction_digits: _Optional[int] = ...) -> None: ...

class GetCurrencyConversionConfigRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetCurrencyConversionConfigResponse(_message.Message):
    __slots__ = ("fiat", "stablecoins")
    FIAT_FIELD_NUMBER: _ClassVar[int]
    STABLECOINS_FIELD_NUMBER: _ClassVar[int]
    fiat: _containers.RepeatedCompositeFieldContainer[CurrencyMetadata]
    stablecoins: _containers.RepeatedCompositeFieldContainer[CurrencyMetadata]
    def __init__(self, fiat: _Optional[_Iterable[_Union[CurrencyMetadata, _Mapping]]] = ..., stablecoins: _Optional[_Iterable[_Union[CurrencyMetadata, _Mapping]]] = ...) -> None: ...

class FiatConversionRate(_message.Message):
    __slots__ = ("code", "units_per_usd_e8")
    CODE_FIELD_NUMBER: _ClassVar[int]
    UNITS_PER_USD_E8_FIELD_NUMBER: _ClassVar[int]
    code: str
    units_per_usd_e8: int
    def __init__(self, code: _Optional[str] = ..., units_per_usd_e8: _Optional[int] = ...) -> None: ...

class FiatConversionSnapshot(_message.Message):
    __slots__ = ("rates", "source_ts_sec", "stale")
    RATES_FIELD_NUMBER: _ClassVar[int]
    SOURCE_TS_SEC_FIELD_NUMBER: _ClassVar[int]
    STALE_FIELD_NUMBER: _ClassVar[int]
    rates: _containers.RepeatedCompositeFieldContainer[FiatConversionRate]
    source_ts_sec: int
    stale: bool
    def __init__(self, rates: _Optional[_Iterable[_Union[FiatConversionRate, _Mapping]]] = ..., source_ts_sec: _Optional[int] = ..., stale: _Optional[bool] = ...) -> None: ...

class StablecoinConversionRate(_message.Message):
    __slots__ = ("code", "usd_per_unit_e8", "source_ts_sec", "stale")
    CODE_FIELD_NUMBER: _ClassVar[int]
    USD_PER_UNIT_E8_FIELD_NUMBER: _ClassVar[int]
    SOURCE_TS_SEC_FIELD_NUMBER: _ClassVar[int]
    STALE_FIELD_NUMBER: _ClassVar[int]
    code: str
    usd_per_unit_e8: int
    source_ts_sec: int
    stale: bool
    def __init__(self, code: _Optional[str] = ..., usd_per_unit_e8: _Optional[int] = ..., source_ts_sec: _Optional[int] = ..., stale: _Optional[bool] = ...) -> None: ...

class GetCurrencyConversionRatesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetCurrencyConversionRatesResponse(_message.Message):
    __slots__ = ("fiat", "stablecoins", "snapshot_ts_sec")
    FIAT_FIELD_NUMBER: _ClassVar[int]
    STABLECOINS_FIELD_NUMBER: _ClassVar[int]
    SNAPSHOT_TS_SEC_FIELD_NUMBER: _ClassVar[int]
    fiat: FiatConversionSnapshot
    stablecoins: _containers.RepeatedCompositeFieldContainer[StablecoinConversionRate]
    snapshot_ts_sec: int
    def __init__(self, fiat: _Optional[_Union[FiatConversionSnapshot, _Mapping]] = ..., stablecoins: _Optional[_Iterable[_Union[StablecoinConversionRate, _Mapping]]] = ..., snapshot_ts_sec: _Optional[int] = ...) -> None: ...
