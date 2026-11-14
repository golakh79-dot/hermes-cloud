from polyester.gen.buf.validate import validate_pb2 as _validate_pb2
from polyester.gen.gnostic.openapi.v3 import annotations_pb2 as _annotations_pb2
from polyester.gen.ledger.v1 import catalog_pb2 as _catalog_pb2
from polyester.gen.polyester.api import options_pb2 as _options_pb2
from polyester.gen.polyester.type.v1 import u128_pb2 as _u128_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BalanceRange(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RANGE_UNSPECIFIED: _ClassVar[BalanceRange]
    DAY_1: _ClassVar[BalanceRange]
    DAY_7: _ClassVar[BalanceRange]
    DAY_30: _ClassVar[BalanceRange]
    DAY_90: _ClassVar[BalanceRange]
    DAY_180: _ClassVar[BalanceRange]
    DAY_365: _ClassVar[BalanceRange]

class EquityGroupBy(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GROUP_BY_UNSPECIFIED: _ClassVar[EquityGroupBy]
    GROUP_BY_ACCOUNT: _ClassVar[EquityGroupBy]
    GROUP_BY_ASSET: _ClassVar[EquityGroupBy]

class TransferSideKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TRANSFER_SIDE_KIND_UNSPECIFIED: _ClassVar[TransferSideKind]
    FUNDING_ACCOUNT: _ClassVar[TransferSideKind]
    TRADING_ACCOUNT: _ClassVar[TransferSideKind]
    EXTERNAL_ADDRESS: _ClassVar[TransferSideKind]
    PRIVATE_COUNTERPARTY: _ClassVar[TransferSideKind]
    FEE_ACCOUNT: _ClassVar[TransferSideKind]
    SYSTEM_ACCOUNT: _ClassVar[TransferSideKind]

class ErrorCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ERROR_CODE_UNSPECIFIED: _ClassVar[ErrorCode]
    ERROR_CODE_BAD_REQUEST: _ClassVar[ErrorCode]
    ERROR_CODE_UNAUTHENTICATED: _ClassVar[ErrorCode]
    ERROR_CODE_PERMISSION_DENIED: _ClassVar[ErrorCode]
    ERROR_CODE_NOT_FOUND: _ClassVar[ErrorCode]
    ERROR_CODE_MISSING_ACCOUNT_ID: _ClassVar[ErrorCode]
    ERROR_CODE_INVALID_ACCOUNT_ID: _ClassVar[ErrorCode]
    ERROR_CODE_MISSING_WALLET: _ClassVar[ErrorCode]
    ERROR_CODE_WALLET_RESOLUTION_UNAVAILABLE: _ClassVar[ErrorCode]
    ERROR_CODE_WALLET_NOT_FOUND: _ClassVar[ErrorCode]
    ERROR_CODE_UPSTREAM_ERROR: _ClassVar[ErrorCode]
    ERROR_CODE_INVALID_SUBACCOUNT_ID: _ClassVar[ErrorCode]
RANGE_UNSPECIFIED: BalanceRange
DAY_1: BalanceRange
DAY_7: BalanceRange
DAY_30: BalanceRange
DAY_90: BalanceRange
DAY_180: BalanceRange
DAY_365: BalanceRange
GROUP_BY_UNSPECIFIED: EquityGroupBy
GROUP_BY_ACCOUNT: EquityGroupBy
GROUP_BY_ASSET: EquityGroupBy
TRANSFER_SIDE_KIND_UNSPECIFIED: TransferSideKind
FUNDING_ACCOUNT: TransferSideKind
TRADING_ACCOUNT: TransferSideKind
EXTERNAL_ADDRESS: TransferSideKind
PRIVATE_COUNTERPARTY: TransferSideKind
FEE_ACCOUNT: TransferSideKind
SYSTEM_ACCOUNT: TransferSideKind
ERROR_CODE_UNSPECIFIED: ErrorCode
ERROR_CODE_BAD_REQUEST: ErrorCode
ERROR_CODE_UNAUTHENTICATED: ErrorCode
ERROR_CODE_PERMISSION_DENIED: ErrorCode
ERROR_CODE_NOT_FOUND: ErrorCode
ERROR_CODE_MISSING_ACCOUNT_ID: ErrorCode
ERROR_CODE_INVALID_ACCOUNT_ID: ErrorCode
ERROR_CODE_MISSING_WALLET: ErrorCode
ERROR_CODE_WALLET_RESOLUTION_UNAVAILABLE: ErrorCode
ERROR_CODE_WALLET_NOT_FOUND: ErrorCode
ERROR_CODE_UPSTREAM_ERROR: ErrorCode
ERROR_CODE_INVALID_SUBACCOUNT_ID: ErrorCode

class GetBalancesRequest(_message.Message):
    __slots__ = ("subaccount_id",)
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    def __init__(self, subaccount_id: _Optional[int] = ...) -> None: ...

class AssetBalance(_message.Message):
    __slots__ = ("asset_id", "trading", "funding", "reserved", "available", "trading_revision", "funding_revision")
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    TRADING_FIELD_NUMBER: _ClassVar[int]
    FUNDING_FIELD_NUMBER: _ClassVar[int]
    RESERVED_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    TRADING_REVISION_FIELD_NUMBER: _ClassVar[int]
    FUNDING_REVISION_FIELD_NUMBER: _ClassVar[int]
    asset_id: int
    trading: _u128_pb2.U128
    funding: _u128_pb2.U128
    reserved: _u128_pb2.U128
    available: _u128_pb2.U128
    trading_revision: int
    funding_revision: int
    def __init__(self, asset_id: _Optional[int] = ..., trading: _Optional[_Union[_u128_pb2.U128, _Mapping]] = ..., funding: _Optional[_Union[_u128_pb2.U128, _Mapping]] = ..., reserved: _Optional[_Union[_u128_pb2.U128, _Mapping]] = ..., available: _Optional[_Union[_u128_pb2.U128, _Mapping]] = ..., trading_revision: _Optional[int] = ..., funding_revision: _Optional[int] = ...) -> None: ...

class GetBalancesResponse(_message.Message):
    __slots__ = ("balances",)
    BALANCES_FIELD_NUMBER: _ClassVar[int]
    balances: _containers.RepeatedCompositeFieldContainer[AssetBalance]
    def __init__(self, balances: _Optional[_Iterable[_Union[AssetBalance, _Mapping]]] = ...) -> None: ...

class GetBalanceHistoryRequest(_message.Message):
    __slots__ = ("subaccount_id", "range", "ledger", "account_codes")
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    RANGE_FIELD_NUMBER: _ClassVar[int]
    LEDGER_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_CODES_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    range: BalanceRange
    ledger: int
    account_codes: _containers.RepeatedScalarFieldContainer[_catalog_pb2.AccountCode]
    def __init__(self, subaccount_id: _Optional[int] = ..., range: _Optional[_Union[BalanceRange, str]] = ..., ledger: _Optional[int] = ..., account_codes: _Optional[_Iterable[_Union[_catalog_pb2.AccountCode, str]]] = ...) -> None: ...

class BalanceSeries(_message.Message):
    __slots__ = ("asset_id", "account_code", "balance_q")
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_CODE_FIELD_NUMBER: _ClassVar[int]
    BALANCE_Q_FIELD_NUMBER: _ClassVar[int]
    asset_id: int
    account_code: _catalog_pb2.AccountCode
    balance_q: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, asset_id: _Optional[int] = ..., account_code: _Optional[_Union[_catalog_pb2.AccountCode, str]] = ..., balance_q: _Optional[_Iterable[int]] = ...) -> None: ...

class GetBalanceHistoryResponse(_message.Message):
    __slots__ = ("range", "bucket", "start_ts_sec", "end_ts_sec", "points", "series")
    RANGE_FIELD_NUMBER: _ClassVar[int]
    BUCKET_FIELD_NUMBER: _ClassVar[int]
    START_TS_SEC_FIELD_NUMBER: _ClassVar[int]
    END_TS_SEC_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    SERIES_FIELD_NUMBER: _ClassVar[int]
    range: BalanceRange
    bucket: str
    start_ts_sec: int
    end_ts_sec: int
    points: int
    series: _containers.RepeatedCompositeFieldContainer[BalanceSeries]
    def __init__(self, range: _Optional[_Union[BalanceRange, str]] = ..., bucket: _Optional[str] = ..., start_ts_sec: _Optional[int] = ..., end_ts_sec: _Optional[int] = ..., points: _Optional[int] = ..., series: _Optional[_Iterable[_Union[BalanceSeries, _Mapping]]] = ...) -> None: ...

class AccountGrouping(_message.Message):
    __slots__ = ("account_code", "name")
    ACCOUNT_CODE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    account_code: int
    name: str
    def __init__(self, account_code: _Optional[int] = ..., name: _Optional[str] = ...) -> None: ...

class AssetGrouping(_message.Message):
    __slots__ = ("id", "symbol")
    ID_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    id: int
    symbol: str
    def __init__(self, id: _Optional[int] = ..., symbol: _Optional[str] = ...) -> None: ...

class PortfolioAccountGrouping(_message.Message):
    __slots__ = ("account_id", "remaining")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    REMAINING_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    remaining: bool
    def __init__(self, account_id: _Optional[int] = ..., remaining: _Optional[bool] = ...) -> None: ...

class GetEquityHistorySeriesRequest(_message.Message):
    __slots__ = ("subaccount_id", "range", "account_codes", "group_by")
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    RANGE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_CODES_FIELD_NUMBER: _ClassVar[int]
    GROUP_BY_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    range: BalanceRange
    account_codes: _containers.RepeatedScalarFieldContainer[_catalog_pb2.AccountCode]
    group_by: EquityGroupBy
    def __init__(self, subaccount_id: _Optional[int] = ..., range: _Optional[_Union[BalanceRange, str]] = ..., account_codes: _Optional[_Iterable[_Union[_catalog_pb2.AccountCode, str]]] = ..., group_by: _Optional[_Union[EquityGroupBy, str]] = ...) -> None: ...

class EquitySeries(_message.Message):
    __slots__ = ("account", "asset", "portfolio_account", "equity_q")
    ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    ASSET_FIELD_NUMBER: _ClassVar[int]
    PORTFOLIO_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    EQUITY_Q_FIELD_NUMBER: _ClassVar[int]
    account: AccountGrouping
    asset: AssetGrouping
    portfolio_account: PortfolioAccountGrouping
    equity_q: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, account: _Optional[_Union[AccountGrouping, _Mapping]] = ..., asset: _Optional[_Union[AssetGrouping, _Mapping]] = ..., portfolio_account: _Optional[_Union[PortfolioAccountGrouping, _Mapping]] = ..., equity_q: _Optional[_Iterable[int]] = ...) -> None: ...

class GetEquityHistorySeriesResponse(_message.Message):
    __slots__ = ("range", "bucket", "start_ts_sec", "end_ts_sec", "quote_asset", "points", "series", "btc_prices_q")
    RANGE_FIELD_NUMBER: _ClassVar[int]
    BUCKET_FIELD_NUMBER: _ClassVar[int]
    START_TS_SEC_FIELD_NUMBER: _ClassVar[int]
    END_TS_SEC_FIELD_NUMBER: _ClassVar[int]
    QUOTE_ASSET_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    SERIES_FIELD_NUMBER: _ClassVar[int]
    BTC_PRICES_Q_FIELD_NUMBER: _ClassVar[int]
    range: BalanceRange
    bucket: str
    start_ts_sec: int
    end_ts_sec: int
    quote_asset: str
    points: int
    series: _containers.RepeatedCompositeFieldContainer[EquitySeries]
    btc_prices_q: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, range: _Optional[_Union[BalanceRange, str]] = ..., bucket: _Optional[str] = ..., start_ts_sec: _Optional[int] = ..., end_ts_sec: _Optional[int] = ..., quote_asset: _Optional[str] = ..., points: _Optional[int] = ..., series: _Optional[_Iterable[_Union[EquitySeries, _Mapping]]] = ..., btc_prices_q: _Optional[_Iterable[int]] = ...) -> None: ...

class GetPortfolioEquityHistorySeriesRequest(_message.Message):
    __slots__ = ("range",)
    RANGE_FIELD_NUMBER: _ClassVar[int]
    range: BalanceRange
    def __init__(self, range: _Optional[_Union[BalanceRange, str]] = ...) -> None: ...

class GetPortfolioEquityHistorySeriesResponse(_message.Message):
    __slots__ = ("range", "bucket", "start_ts_sec", "end_ts_sec", "quote_asset", "points", "series", "btc_prices_q")
    RANGE_FIELD_NUMBER: _ClassVar[int]
    BUCKET_FIELD_NUMBER: _ClassVar[int]
    START_TS_SEC_FIELD_NUMBER: _ClassVar[int]
    END_TS_SEC_FIELD_NUMBER: _ClassVar[int]
    QUOTE_ASSET_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    SERIES_FIELD_NUMBER: _ClassVar[int]
    BTC_PRICES_Q_FIELD_NUMBER: _ClassVar[int]
    range: BalanceRange
    bucket: str
    start_ts_sec: int
    end_ts_sec: int
    quote_asset: str
    points: int
    series: _containers.RepeatedCompositeFieldContainer[EquitySeries]
    btc_prices_q: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, range: _Optional[_Union[BalanceRange, str]] = ..., bucket: _Optional[str] = ..., start_ts_sec: _Optional[int] = ..., end_ts_sec: _Optional[int] = ..., quote_asset: _Optional[str] = ..., points: _Optional[int] = ..., series: _Optional[_Iterable[_Union[EquitySeries, _Mapping]]] = ..., btc_prices_q: _Optional[_Iterable[int]] = ...) -> None: ...

class PortfolioAccountEquity(_message.Message):
    __slots__ = ("account_id", "equity_q", "top_asset_ids")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    EQUITY_Q_FIELD_NUMBER: _ClassVar[int]
    TOP_ASSET_IDS_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    equity_q: int
    top_asset_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, account_id: _Optional[int] = ..., equity_q: _Optional[int] = ..., top_asset_ids: _Optional[_Iterable[int]] = ...) -> None: ...

class PortfolioAssetEquity(_message.Message):
    __slots__ = ("asset_id", "balance_q", "equity_q")
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    BALANCE_Q_FIELD_NUMBER: _ClassVar[int]
    EQUITY_Q_FIELD_NUMBER: _ClassVar[int]
    asset_id: int
    balance_q: int
    equity_q: int
    def __init__(self, asset_id: _Optional[int] = ..., balance_q: _Optional[int] = ..., equity_q: _Optional[int] = ...) -> None: ...

class GetPortfolioEquitySnapshotRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetPortfolioEquitySnapshotResponse(_message.Message):
    __slots__ = ("quote_asset", "total_equity_q", "accounts", "assets", "btc_price_q")
    QUOTE_ASSET_FIELD_NUMBER: _ClassVar[int]
    TOTAL_EQUITY_Q_FIELD_NUMBER: _ClassVar[int]
    ACCOUNTS_FIELD_NUMBER: _ClassVar[int]
    ASSETS_FIELD_NUMBER: _ClassVar[int]
    BTC_PRICE_Q_FIELD_NUMBER: _ClassVar[int]
    quote_asset: str
    total_equity_q: int
    accounts: _containers.RepeatedCompositeFieldContainer[PortfolioAccountEquity]
    assets: _containers.RepeatedCompositeFieldContainer[PortfolioAssetEquity]
    btc_price_q: int
    def __init__(self, quote_asset: _Optional[str] = ..., total_equity_q: _Optional[int] = ..., accounts: _Optional[_Iterable[_Union[PortfolioAccountEquity, _Mapping]]] = ..., assets: _Optional[_Iterable[_Union[PortfolioAssetEquity, _Mapping]]] = ..., btc_price_q: _Optional[int] = ...) -> None: ...

class ListTransfersRequest(_message.Message):
    __slots__ = ("subaccount_id", "limit", "reversed", "ts_min_us", "ts_max_us", "transfer_code", "ledger", "page_token")
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    REVERSED_FIELD_NUMBER: _ClassVar[int]
    TS_MIN_US_FIELD_NUMBER: _ClassVar[int]
    TS_MAX_US_FIELD_NUMBER: _ClassVar[int]
    TRANSFER_CODE_FIELD_NUMBER: _ClassVar[int]
    LEDGER_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    limit: int
    reversed: bool
    ts_min_us: int
    ts_max_us: int
    transfer_code: _catalog_pb2.TransferCode
    ledger: int
    page_token: str
    def __init__(self, subaccount_id: _Optional[int] = ..., limit: _Optional[int] = ..., reversed: _Optional[bool] = ..., ts_min_us: _Optional[int] = ..., ts_max_us: _Optional[int] = ..., transfer_code: _Optional[_Union[_catalog_pb2.TransferCode, str]] = ..., ledger: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class TransferSide(_message.Message):
    __slots__ = ("kind", "account_id", "address", "chain_id")
    KIND_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    kind: TransferSideKind
    account_id: int
    address: str
    chain_id: int
    def __init__(self, kind: _Optional[_Union[TransferSideKind, str]] = ..., account_id: _Optional[int] = ..., address: _Optional[str] = ..., chain_id: _Optional[int] = ...) -> None: ...

class TransferRow(_message.Message):
    __slots__ = ("asset_id", "amount_e18", "transfer_code", "account_code", "ts_us", "balance_after_e18", "is_debit", "link_id", "flow_id", "source", "destination", "transfer_id")
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_E18_FIELD_NUMBER: _ClassVar[int]
    TRANSFER_CODE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_CODE_FIELD_NUMBER: _ClassVar[int]
    TS_US_FIELD_NUMBER: _ClassVar[int]
    BALANCE_AFTER_E18_FIELD_NUMBER: _ClassVar[int]
    IS_DEBIT_FIELD_NUMBER: _ClassVar[int]
    LINK_ID_FIELD_NUMBER: _ClassVar[int]
    FLOW_ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_FIELD_NUMBER: _ClassVar[int]
    TRANSFER_ID_FIELD_NUMBER: _ClassVar[int]
    asset_id: int
    amount_e18: _u128_pb2.U128
    transfer_code: _catalog_pb2.TransferCode
    account_code: _catalog_pb2.AccountCode
    ts_us: int
    balance_after_e18: _u128_pb2.U128
    is_debit: bool
    link_id: int
    flow_id: str
    source: TransferSide
    destination: TransferSide
    transfer_id: str
    def __init__(self, asset_id: _Optional[int] = ..., amount_e18: _Optional[_Union[_u128_pb2.U128, _Mapping]] = ..., transfer_code: _Optional[_Union[_catalog_pb2.TransferCode, str]] = ..., account_code: _Optional[_Union[_catalog_pb2.AccountCode, str]] = ..., ts_us: _Optional[int] = ..., balance_after_e18: _Optional[_Union[_u128_pb2.U128, _Mapping]] = ..., is_debit: _Optional[bool] = ..., link_id: _Optional[int] = ..., flow_id: _Optional[str] = ..., source: _Optional[_Union[TransferSide, _Mapping]] = ..., destination: _Optional[_Union[TransferSide, _Mapping]] = ..., transfer_id: _Optional[str] = ...) -> None: ...

class TransferRowBatch(_message.Message):
    __slots__ = ("events",)
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    events: _containers.RepeatedCompositeFieldContainer[TransferRow]
    def __init__(self, events: _Optional[_Iterable[_Union[TransferRow, _Mapping]]] = ...) -> None: ...

class ListTransfersResponse(_message.Message):
    __slots__ = ("transfers", "next_page_token")
    TRANSFERS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    transfers: _containers.RepeatedCompositeFieldContainer[TransferRow]
    next_page_token: str
    def __init__(self, transfers: _Optional[_Iterable[_Union[TransferRow, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class ListHoldsRequest(_message.Message):
    __slots__ = ("subaccount_id", "limit", "reversed", "page_token")
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    REVERSED_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    limit: int
    reversed: bool
    page_token: str
    def __init__(self, subaccount_id: _Optional[int] = ..., limit: _Optional[int] = ..., reversed: _Optional[bool] = ..., page_token: _Optional[str] = ...) -> None: ...

class HoldRow(_message.Message):
    __slots__ = ("hold_id", "amount_reserved_e18", "asset_id", "expires_at_ns")
    HOLD_ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_RESERVED_E18_FIELD_NUMBER: _ClassVar[int]
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_NS_FIELD_NUMBER: _ClassVar[int]
    hold_id: int
    amount_reserved_e18: _u128_pb2.U128
    asset_id: int
    expires_at_ns: int
    def __init__(self, hold_id: _Optional[int] = ..., amount_reserved_e18: _Optional[_Union[_u128_pb2.U128, _Mapping]] = ..., asset_id: _Optional[int] = ..., expires_at_ns: _Optional[int] = ...) -> None: ...

class ListHoldsResponse(_message.Message):
    __slots__ = ("holds", "next_page_token")
    HOLDS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    holds: _containers.RepeatedCompositeFieldContainer[HoldRow]
    next_page_token: str
    def __init__(self, holds: _Optional[_Iterable[_Union[HoldRow, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class ErrorDetail(_message.Message):
    __slots__ = ("code",)
    CODE_FIELD_NUMBER: _ClassVar[int]
    code: ErrorCode
    def __init__(self, code: _Optional[_Union[ErrorCode, str]] = ...) -> None: ...
