import datetime

from polyester.gen.buf.validate import validate_pb2 as _validate_pb2
from polyester.gen.gnostic.openapi.v3 import annotations_pb2 as _annotations_pb2
from polyester.gen.google.api import annotations_pb2 as _annotations_pb2_1
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from polyester.gen.orders.v1 import orders_pb2 as _orders_pb2
from polyester.gen.polyester.api import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CheckpointBadge(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BADGE_UNSPECIFIED: _ClassVar[CheckpointBadge]
    FIRST_TRADE: _ClassVar[CheckpointBadge]
    SEVEN_DAY_STREAK: _ClassVar[CheckpointBadge]
    THREE_MARKETS: _ClassVar[CheckpointBadge]
    VOLUME_1000_USD: _ClassVar[CheckpointBadge]
    HUNDRED_TRADES: _ClassVar[CheckpointBadge]
    TEN_MARKETS: _ClassVar[CheckpointBadge]
    THIRTY_DAY_STREAK: _ClassVar[CheckpointBadge]
    EVERY_ORDER_TOOL: _ClassVar[CheckpointBadge]

class CheckpointField(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FIELD_UNSPECIFIED: _ClassVar[CheckpointField]
    VOLUME: _ClassVar[CheckpointField]
    TOP_PAIRS: _ClassVar[CheckpointField]
    ORDER_TYPES: _ClassVar[CheckpointField]
    TIME_IN_FORCE: _ClassVar[CheckpointField]
    ORDER_STATUS: _ClassVar[CheckpointField]
    TOOLS: _ClassVar[CheckpointField]
    MEDIAN_LIMIT_REST: _ClassVar[CheckpointField]
    DEPOSITS: _ClassVar[CheckpointField]
    WITHDRAWALS: _ClassVar[CheckpointField]
    INTERNAL_TRANSFERS: _ClassVar[CheckpointField]
    DAILY_CLAIM_AMOUNTS: _ClassVar[CheckpointField]
    PORTFOLIO_VALUE: _ClassVar[CheckpointField]
    TRADING_BALANCES: _ClassVar[CheckpointField]
    FUNDING_BALANCES: _ClassVar[CheckpointField]
    TRANSFERS: _ClassVar[CheckpointField]
    SEASON_RESULT: _ClassVar[CheckpointField]
BADGE_UNSPECIFIED: CheckpointBadge
FIRST_TRADE: CheckpointBadge
SEVEN_DAY_STREAK: CheckpointBadge
THREE_MARKETS: CheckpointBadge
VOLUME_1000_USD: CheckpointBadge
HUNDRED_TRADES: CheckpointBadge
TEN_MARKETS: CheckpointBadge
THIRTY_DAY_STREAK: CheckpointBadge
EVERY_ORDER_TOOL: CheckpointBadge
FIELD_UNSPECIFIED: CheckpointField
VOLUME: CheckpointField
TOP_PAIRS: CheckpointField
ORDER_TYPES: CheckpointField
TIME_IN_FORCE: CheckpointField
ORDER_STATUS: CheckpointField
TOOLS: CheckpointField
MEDIAN_LIMIT_REST: CheckpointField
DEPOSITS: CheckpointField
WITHDRAWALS: CheckpointField
INTERNAL_TRANSFERS: CheckpointField
DAILY_CLAIM_AMOUNTS: CheckpointField
PORTFOLIO_VALUE: CheckpointField
TRADING_BALANCES: CheckpointField
FUNDING_BALANCES: CheckpointField
TRANSFERS: CheckpointField
SEASON_RESULT: CheckpointField

class VolumePoint(_message.Message):
    __slots__ = ("day", "usd", "approximate", "trades")
    DAY_FIELD_NUMBER: _ClassVar[int]
    USD_FIELD_NUMBER: _ClassVar[int]
    APPROXIMATE_FIELD_NUMBER: _ClassVar[int]
    TRADES_FIELD_NUMBER: _ClassVar[int]
    day: _timestamp_pb2.Timestamp
    usd: str
    approximate: bool
    trades: int
    def __init__(self, day: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., usd: _Optional[str] = ..., approximate: _Optional[bool] = ..., trades: _Optional[int] = ...) -> None: ...

class PortfolioValuePoint(_message.Message):
    __slots__ = ("hour", "usd", "approximate")
    HOUR_FIELD_NUMBER: _ClassVar[int]
    USD_FIELD_NUMBER: _ClassVar[int]
    APPROXIMATE_FIELD_NUMBER: _ClassVar[int]
    hour: _timestamp_pb2.Timestamp
    usd: str
    approximate: bool
    def __init__(self, hour: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., usd: _Optional[str] = ..., approximate: _Optional[bool] = ...) -> None: ...

class WeekdayTrades(_message.Message):
    __slots__ = ("hours",)
    HOURS_FIELD_NUMBER: _ClassVar[int]
    hours: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, hours: _Optional[_Iterable[int]] = ...) -> None: ...

class PairActivity(_message.Message):
    __slots__ = ("symbol_id", "symbol", "volume_usd", "trades")
    SYMBOL_ID_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    VOLUME_USD_FIELD_NUMBER: _ClassVar[int]
    TRADES_FIELD_NUMBER: _ClassVar[int]
    symbol_id: int
    symbol: str
    volume_usd: str
    trades: int
    def __init__(self, symbol_id: _Optional[int] = ..., symbol: _Optional[str] = ..., volume_usd: _Optional[str] = ..., trades: _Optional[int] = ...) -> None: ...

class BiggestTrade(_message.Message):
    __slots__ = ("symbol_id", "symbol", "side", "at")
    SYMBOL_ID_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    SIDE_FIELD_NUMBER: _ClassVar[int]
    AT_FIELD_NUMBER: _ClassVar[int]
    symbol_id: int
    symbol: str
    side: _orders_pb2.Side
    at: _timestamp_pb2.Timestamp
    def __init__(self, symbol_id: _Optional[int] = ..., symbol: _Optional[str] = ..., side: _Optional[_Union[_orders_pb2.Side, str]] = ..., at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class OrderTypeCounts(_message.Message):
    __slots__ = ("limit", "market")
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    MARKET_FIELD_NUMBER: _ClassVar[int]
    limit: int
    market: int
    def __init__(self, limit: _Optional[int] = ..., market: _Optional[int] = ...) -> None: ...

class TimeInForceCounts(_message.Message):
    __slots__ = ("gtc", "ioc", "fok", "gtd")
    GTC_FIELD_NUMBER: _ClassVar[int]
    IOC_FIELD_NUMBER: _ClassVar[int]
    FOK_FIELD_NUMBER: _ClassVar[int]
    GTD_FIELD_NUMBER: _ClassVar[int]
    gtc: int
    ioc: int
    fok: int
    gtd: int
    def __init__(self, gtc: _Optional[int] = ..., ioc: _Optional[int] = ..., fok: _Optional[int] = ..., gtd: _Optional[int] = ...) -> None: ...

class OrderToolCounts(_message.Message):
    __slots__ = ("stop_loss", "take_profit", "trailing_stop", "twap", "ladder")
    STOP_LOSS_FIELD_NUMBER: _ClassVar[int]
    TAKE_PROFIT_FIELD_NUMBER: _ClassVar[int]
    TRAILING_STOP_FIELD_NUMBER: _ClassVar[int]
    TWAP_FIELD_NUMBER: _ClassVar[int]
    LADDER_FIELD_NUMBER: _ClassVar[int]
    stop_loss: int
    take_profit: int
    trailing_stop: int
    twap: int
    ladder: int
    def __init__(self, stop_loss: _Optional[int] = ..., take_profit: _Optional[int] = ..., trailing_stop: _Optional[int] = ..., twap: _Optional[int] = ..., ladder: _Optional[int] = ...) -> None: ...

class VIPTierChange(_message.Message):
    __slots__ = ("date", "tier")
    DATE_FIELD_NUMBER: _ClassVar[int]
    TIER_FIELD_NUMBER: _ClassVar[int]
    date: str
    tier: int
    def __init__(self, date: _Optional[str] = ..., tier: _Optional[int] = ...) -> None: ...

class EarnedBadge(_message.Message):
    __slots__ = ("badge", "earned_at")
    BADGE_FIELD_NUMBER: _ClassVar[int]
    EARNED_AT_FIELD_NUMBER: _ClassVar[int]
    badge: CheckpointBadge
    earned_at: _timestamp_pb2.Timestamp
    def __init__(self, badge: _Optional[_Union[CheckpointBadge, str]] = ..., earned_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class AssetAmount(_message.Message):
    __slots__ = ("asset", "amount", "usd", "excluded_from_value")
    ASSET_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    USD_FIELD_NUMBER: _ClassVar[int]
    EXCLUDED_FROM_VALUE_FIELD_NUMBER: _ClassVar[int]
    asset: str
    amount: str
    usd: str
    excluded_from_value: bool
    def __init__(self, asset: _Optional[str] = ..., amount: _Optional[str] = ..., usd: _Optional[str] = ..., excluded_from_value: _Optional[bool] = ...) -> None: ...

class FlowTotal(_message.Message):
    __slots__ = ("count", "usd")
    COUNT_FIELD_NUMBER: _ClassVar[int]
    USD_FIELD_NUMBER: _ClassVar[int]
    count: int
    usd: str
    def __init__(self, count: _Optional[int] = ..., usd: _Optional[str] = ...) -> None: ...

class ChainFlow(_message.Message):
    __slots__ = ("polyester_chain_id", "chain_name", "total")
    POLYESTER_CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    CHAIN_NAME_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    polyester_chain_id: int
    chain_name: str
    total: FlowTotal
    def __init__(self, polyester_chain_id: _Optional[int] = ..., chain_name: _Optional[str] = ..., total: _Optional[_Union[FlowTotal, _Mapping]] = ...) -> None: ...

class FundingFlowSummary(_message.Message):
    __slots__ = ("count", "chains", "amounts")
    COUNT_FIELD_NUMBER: _ClassVar[int]
    CHAINS_FIELD_NUMBER: _ClassVar[int]
    AMOUNTS_FIELD_NUMBER: _ClassVar[int]
    count: int
    chains: _containers.RepeatedCompositeFieldContainer[ChainFlow]
    amounts: _containers.RepeatedCompositeFieldContainer[AssetAmount]
    def __init__(self, count: _Optional[int] = ..., chains: _Optional[_Iterable[_Union[ChainFlow, _Mapping]]] = ..., amounts: _Optional[_Iterable[_Union[AssetAmount, _Mapping]]] = ...) -> None: ...

class FundingDay(_message.Message):
    __slots__ = ("date", "deposit_usd", "withdrawal_usd")
    DATE_FIELD_NUMBER: _ClassVar[int]
    DEPOSIT_USD_FIELD_NUMBER: _ClassVar[int]
    WITHDRAWAL_USD_FIELD_NUMBER: _ClassVar[int]
    date: str
    deposit_usd: str
    withdrawal_usd: str
    def __init__(self, date: _Optional[str] = ..., deposit_usd: _Optional[str] = ..., withdrawal_usd: _Optional[str] = ...) -> None: ...

class Checkpoint(_message.Message):
    __slots__ = ("number", "season_start", "season_end", "taken_at", "volume_usd", "trades", "orders", "days_active", "longest_streak", "top_pairs", "markets_traded", "maker_trades", "taker_trades", "self_trades", "trades_by_weekday_hour", "daily_volume", "biggest_trade_usd", "biggest_trade", "order_types", "time_in_force", "tools", "post_only", "amends", "filled_orders", "partially_filled_orders", "canceled_orders", "rejected_orders", "fill_rate", "cancel_ratio", "median_limit_rest_ms", "first_trade_at", "busiest_day", "most_active_hour_utc", "vip_tier_at_checkpoint", "peak_vip_tier", "vip_timeline", "badges", "portfolio_value", "trading_balances", "funding_balances", "deposits", "withdrawals", "funding_by_day", "transfers_in", "transfers_out", "internal_transfers", "daily_claims", "daily_claim_amounts", "inflow_usd", "outflow_usd", "net_inflow_usd", "final_value_usd", "opening_value_usd", "season_result_usd", "subaccounts", "incomplete")
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    SEASON_START_FIELD_NUMBER: _ClassVar[int]
    SEASON_END_FIELD_NUMBER: _ClassVar[int]
    TAKEN_AT_FIELD_NUMBER: _ClassVar[int]
    VOLUME_USD_FIELD_NUMBER: _ClassVar[int]
    TRADES_FIELD_NUMBER: _ClassVar[int]
    ORDERS_FIELD_NUMBER: _ClassVar[int]
    DAYS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    LONGEST_STREAK_FIELD_NUMBER: _ClassVar[int]
    TOP_PAIRS_FIELD_NUMBER: _ClassVar[int]
    MARKETS_TRADED_FIELD_NUMBER: _ClassVar[int]
    MAKER_TRADES_FIELD_NUMBER: _ClassVar[int]
    TAKER_TRADES_FIELD_NUMBER: _ClassVar[int]
    SELF_TRADES_FIELD_NUMBER: _ClassVar[int]
    TRADES_BY_WEEKDAY_HOUR_FIELD_NUMBER: _ClassVar[int]
    DAILY_VOLUME_FIELD_NUMBER: _ClassVar[int]
    BIGGEST_TRADE_USD_FIELD_NUMBER: _ClassVar[int]
    BIGGEST_TRADE_FIELD_NUMBER: _ClassVar[int]
    ORDER_TYPES_FIELD_NUMBER: _ClassVar[int]
    TIME_IN_FORCE_FIELD_NUMBER: _ClassVar[int]
    TOOLS_FIELD_NUMBER: _ClassVar[int]
    POST_ONLY_FIELD_NUMBER: _ClassVar[int]
    AMENDS_FIELD_NUMBER: _ClassVar[int]
    FILLED_ORDERS_FIELD_NUMBER: _ClassVar[int]
    PARTIALLY_FILLED_ORDERS_FIELD_NUMBER: _ClassVar[int]
    CANCELED_ORDERS_FIELD_NUMBER: _ClassVar[int]
    REJECTED_ORDERS_FIELD_NUMBER: _ClassVar[int]
    FILL_RATE_FIELD_NUMBER: _ClassVar[int]
    CANCEL_RATIO_FIELD_NUMBER: _ClassVar[int]
    MEDIAN_LIMIT_REST_MS_FIELD_NUMBER: _ClassVar[int]
    FIRST_TRADE_AT_FIELD_NUMBER: _ClassVar[int]
    BUSIEST_DAY_FIELD_NUMBER: _ClassVar[int]
    MOST_ACTIVE_HOUR_UTC_FIELD_NUMBER: _ClassVar[int]
    VIP_TIER_AT_CHECKPOINT_FIELD_NUMBER: _ClassVar[int]
    PEAK_VIP_TIER_FIELD_NUMBER: _ClassVar[int]
    VIP_TIMELINE_FIELD_NUMBER: _ClassVar[int]
    BADGES_FIELD_NUMBER: _ClassVar[int]
    PORTFOLIO_VALUE_FIELD_NUMBER: _ClassVar[int]
    TRADING_BALANCES_FIELD_NUMBER: _ClassVar[int]
    FUNDING_BALANCES_FIELD_NUMBER: _ClassVar[int]
    DEPOSITS_FIELD_NUMBER: _ClassVar[int]
    WITHDRAWALS_FIELD_NUMBER: _ClassVar[int]
    FUNDING_BY_DAY_FIELD_NUMBER: _ClassVar[int]
    TRANSFERS_IN_FIELD_NUMBER: _ClassVar[int]
    TRANSFERS_OUT_FIELD_NUMBER: _ClassVar[int]
    INTERNAL_TRANSFERS_FIELD_NUMBER: _ClassVar[int]
    DAILY_CLAIMS_FIELD_NUMBER: _ClassVar[int]
    DAILY_CLAIM_AMOUNTS_FIELD_NUMBER: _ClassVar[int]
    INFLOW_USD_FIELD_NUMBER: _ClassVar[int]
    OUTFLOW_USD_FIELD_NUMBER: _ClassVar[int]
    NET_INFLOW_USD_FIELD_NUMBER: _ClassVar[int]
    FINAL_VALUE_USD_FIELD_NUMBER: _ClassVar[int]
    OPENING_VALUE_USD_FIELD_NUMBER: _ClassVar[int]
    SEASON_RESULT_USD_FIELD_NUMBER: _ClassVar[int]
    SUBACCOUNTS_FIELD_NUMBER: _ClassVar[int]
    INCOMPLETE_FIELD_NUMBER: _ClassVar[int]
    number: int
    season_start: _timestamp_pb2.Timestamp
    season_end: _timestamp_pb2.Timestamp
    taken_at: _timestamp_pb2.Timestamp
    volume_usd: str
    trades: int
    orders: int
    days_active: int
    longest_streak: int
    top_pairs: _containers.RepeatedCompositeFieldContainer[PairActivity]
    markets_traded: int
    maker_trades: int
    taker_trades: int
    self_trades: int
    trades_by_weekday_hour: _containers.RepeatedCompositeFieldContainer[WeekdayTrades]
    daily_volume: _containers.RepeatedCompositeFieldContainer[VolumePoint]
    biggest_trade_usd: str
    biggest_trade: BiggestTrade
    order_types: OrderTypeCounts
    time_in_force: TimeInForceCounts
    tools: OrderToolCounts
    post_only: int
    amends: int
    filled_orders: int
    partially_filled_orders: int
    canceled_orders: int
    rejected_orders: int
    fill_rate: str
    cancel_ratio: str
    median_limit_rest_ms: int
    first_trade_at: _timestamp_pb2.Timestamp
    busiest_day: str
    most_active_hour_utc: int
    vip_tier_at_checkpoint: int
    peak_vip_tier: int
    vip_timeline: _containers.RepeatedCompositeFieldContainer[VIPTierChange]
    badges: _containers.RepeatedCompositeFieldContainer[EarnedBadge]
    portfolio_value: _containers.RepeatedCompositeFieldContainer[PortfolioValuePoint]
    trading_balances: _containers.RepeatedCompositeFieldContainer[AssetAmount]
    funding_balances: _containers.RepeatedCompositeFieldContainer[AssetAmount]
    deposits: FundingFlowSummary
    withdrawals: FundingFlowSummary
    funding_by_day: _containers.RepeatedCompositeFieldContainer[FundingDay]
    transfers_in: FlowTotal
    transfers_out: FlowTotal
    internal_transfers: int
    daily_claims: int
    daily_claim_amounts: _containers.RepeatedCompositeFieldContainer[AssetAmount]
    inflow_usd: str
    outflow_usd: str
    net_inflow_usd: str
    final_value_usd: str
    opening_value_usd: str
    season_result_usd: str
    subaccounts: int
    incomplete: _containers.RepeatedScalarFieldContainer[CheckpointField]
    def __init__(self, number: _Optional[int] = ..., season_start: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., season_end: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., taken_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., volume_usd: _Optional[str] = ..., trades: _Optional[int] = ..., orders: _Optional[int] = ..., days_active: _Optional[int] = ..., longest_streak: _Optional[int] = ..., top_pairs: _Optional[_Iterable[_Union[PairActivity, _Mapping]]] = ..., markets_traded: _Optional[int] = ..., maker_trades: _Optional[int] = ..., taker_trades: _Optional[int] = ..., self_trades: _Optional[int] = ..., trades_by_weekday_hour: _Optional[_Iterable[_Union[WeekdayTrades, _Mapping]]] = ..., daily_volume: _Optional[_Iterable[_Union[VolumePoint, _Mapping]]] = ..., biggest_trade_usd: _Optional[str] = ..., biggest_trade: _Optional[_Union[BiggestTrade, _Mapping]] = ..., order_types: _Optional[_Union[OrderTypeCounts, _Mapping]] = ..., time_in_force: _Optional[_Union[TimeInForceCounts, _Mapping]] = ..., tools: _Optional[_Union[OrderToolCounts, _Mapping]] = ..., post_only: _Optional[int] = ..., amends: _Optional[int] = ..., filled_orders: _Optional[int] = ..., partially_filled_orders: _Optional[int] = ..., canceled_orders: _Optional[int] = ..., rejected_orders: _Optional[int] = ..., fill_rate: _Optional[str] = ..., cancel_ratio: _Optional[str] = ..., median_limit_rest_ms: _Optional[int] = ..., first_trade_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., busiest_day: _Optional[str] = ..., most_active_hour_utc: _Optional[int] = ..., vip_tier_at_checkpoint: _Optional[int] = ..., peak_vip_tier: _Optional[int] = ..., vip_timeline: _Optional[_Iterable[_Union[VIPTierChange, _Mapping]]] = ..., badges: _Optional[_Iterable[_Union[EarnedBadge, _Mapping]]] = ..., portfolio_value: _Optional[_Iterable[_Union[PortfolioValuePoint, _Mapping]]] = ..., trading_balances: _Optional[_Iterable[_Union[AssetAmount, _Mapping]]] = ..., funding_balances: _Optional[_Iterable[_Union[AssetAmount, _Mapping]]] = ..., deposits: _Optional[_Union[FundingFlowSummary, _Mapping]] = ..., withdrawals: _Optional[_Union[FundingFlowSummary, _Mapping]] = ..., funding_by_day: _Optional[_Iterable[_Union[FundingDay, _Mapping]]] = ..., transfers_in: _Optional[_Union[FlowTotal, _Mapping]] = ..., transfers_out: _Optional[_Union[FlowTotal, _Mapping]] = ..., internal_transfers: _Optional[int] = ..., daily_claims: _Optional[int] = ..., daily_claim_amounts: _Optional[_Iterable[_Union[AssetAmount, _Mapping]]] = ..., inflow_usd: _Optional[str] = ..., outflow_usd: _Optional[str] = ..., net_inflow_usd: _Optional[str] = ..., final_value_usd: _Optional[str] = ..., opening_value_usd: _Optional[str] = ..., season_result_usd: _Optional[str] = ..., subaccounts: _Optional[int] = ..., incomplete: _Optional[_Iterable[_Union[CheckpointField, str]]] = ...) -> None: ...

class ListMyCheckpointsRequest(_message.Message):
    __slots__ = ("subaccount_id",)
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    def __init__(self, subaccount_id: _Optional[int] = ...) -> None: ...

class ListMyCheckpointsResponse(_message.Message):
    __slots__ = ("checkpoints",)
    CHECKPOINTS_FIELD_NUMBER: _ClassVar[int]
    checkpoints: _containers.RepeatedCompositeFieldContainer[Checkpoint]
    def __init__(self, checkpoints: _Optional[_Iterable[_Union[Checkpoint, _Mapping]]] = ...) -> None: ...
