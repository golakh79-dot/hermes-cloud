import datetime

from polyester.gen.buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from polyester.gen.ledger.v1 import catalog_pb2 as _catalog_pb2
from polyester.gen.orders.v1 import orders_pb2 as _orders_pb2
from polyester.gen.polyester.api import options_pb2 as _options_pb2
from polyester.gen.polyester.type.v1 import u128_pb2 as _u128_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OrderStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ORDER_STATUS_UNSPECIFIED: _ClassVar[OrderStatus]
    PENDING: _ClassVar[OrderStatus]
    PENDING_CANCEL: _ClassVar[OrderStatus]
    WORKING: _ClassVar[OrderStatus]
    FILLED: _ClassVar[OrderStatus]
    CANCELED: _ClassVar[OrderStatus]
    REJECTED: _ClassVar[OrderStatus]

class CancelReason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CANCEL_REASON_UNSPECIFIED: _ClassVar[CancelReason]
    CANCEL_REASON_USER_REQUEST: _ClassVar[CancelReason]
    CANCEL_REASON_IOC_REMAINDER: _ClassVar[CancelReason]
    CANCEL_REASON_MARKET_REMAINDER: _ClassVar[CancelReason]
    CANCEL_REASON_STP_EXPIRE_MAKER: _ClassVar[CancelReason]
    CANCEL_REASON_STP_EXPIRE_TAKER: _ClassVar[CancelReason]
    CANCEL_REASON_STP_EXPIRE_BOTH: _ClassVar[CancelReason]
    CANCEL_REASON_REPLACED: _ClassVar[CancelReason]
    CANCEL_REASON_GTD_EXPIRED: _ClassVar[CancelReason]
    CANCEL_REASON_QTY_AT_OR_BELOW_FILLED: _ClassVar[CancelReason]
    CANCEL_REASON_PAIR_DRAIN: _ClassVar[CancelReason]
    CANCEL_REASON_ATTACHED_RISK_REFUSED: _ClassVar[CancelReason]
    CANCEL_REASON_CANCEL_ALL_AFTER: _ClassVar[CancelReason]
    CANCEL_REASON_ACCOUNT_REPAIR: _ClassVar[CancelReason]
    CANCEL_REASON_TWAP_ROLLOVER: _ClassVar[CancelReason]
    CANCEL_REASON_STRATEGY_CANCEL: _ClassVar[CancelReason]
    CANCEL_REASON_SYSTEM: _ClassVar[CancelReason]

class BatchReplacePhase(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BATCH_REPLACE_PHASE_UNSPECIFIED: _ClassVar[BatchReplacePhase]
    BATCH_REPLACE_PHASE_ADMITTED: _ClassVar[BatchReplacePhase]
    BATCH_REPLACE_PHASE_WORKING: _ClassVar[BatchReplacePhase]
    BATCH_REPLACE_PHASE_REJECTED: _ClassVar[BatchReplacePhase]
    BATCH_REPLACE_PHASE_TERMINAL: _ClassVar[BatchReplacePhase]

class OrderOriginScope(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ORDER_ORIGIN_SCOPE_UNSPECIFIED: _ClassVar[OrderOriginScope]
    DIRECT: _ClassVar[OrderOriginScope]
    ATTACHED_RISK: _ClassVar[OrderOriginScope]
    STANDALONE_TRIGGER: _ClassVar[OrderOriginScope]
    SYSTEM: _ClassVar[OrderOriginScope]

class OrderTriggerType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ORDER_TRIGGER_TYPE_UNSPECIFIED: _ClassVar[OrderTriggerType]
    STOP_LOSS: _ClassVar[OrderTriggerType]
    TAKE_PROFIT: _ClassVar[OrderTriggerType]
    TRAILING_STOP: _ClassVar[OrderTriggerType]
    TWAP: _ClassVar[OrderTriggerType]
    LADDER: _ClassVar[OrderTriggerType]
ORDER_STATUS_UNSPECIFIED: OrderStatus
PENDING: OrderStatus
PENDING_CANCEL: OrderStatus
WORKING: OrderStatus
FILLED: OrderStatus
CANCELED: OrderStatus
REJECTED: OrderStatus
CANCEL_REASON_UNSPECIFIED: CancelReason
CANCEL_REASON_USER_REQUEST: CancelReason
CANCEL_REASON_IOC_REMAINDER: CancelReason
CANCEL_REASON_MARKET_REMAINDER: CancelReason
CANCEL_REASON_STP_EXPIRE_MAKER: CancelReason
CANCEL_REASON_STP_EXPIRE_TAKER: CancelReason
CANCEL_REASON_STP_EXPIRE_BOTH: CancelReason
CANCEL_REASON_REPLACED: CancelReason
CANCEL_REASON_GTD_EXPIRED: CancelReason
CANCEL_REASON_QTY_AT_OR_BELOW_FILLED: CancelReason
CANCEL_REASON_PAIR_DRAIN: CancelReason
CANCEL_REASON_ATTACHED_RISK_REFUSED: CancelReason
CANCEL_REASON_CANCEL_ALL_AFTER: CancelReason
CANCEL_REASON_ACCOUNT_REPAIR: CancelReason
CANCEL_REASON_TWAP_ROLLOVER: CancelReason
CANCEL_REASON_STRATEGY_CANCEL: CancelReason
CANCEL_REASON_SYSTEM: CancelReason
BATCH_REPLACE_PHASE_UNSPECIFIED: BatchReplacePhase
BATCH_REPLACE_PHASE_ADMITTED: BatchReplacePhase
BATCH_REPLACE_PHASE_WORKING: BatchReplacePhase
BATCH_REPLACE_PHASE_REJECTED: BatchReplacePhase
BATCH_REPLACE_PHASE_TERMINAL: BatchReplacePhase
ORDER_ORIGIN_SCOPE_UNSPECIFIED: OrderOriginScope
DIRECT: OrderOriginScope
ATTACHED_RISK: OrderOriginScope
STANDALONE_TRIGGER: OrderOriginScope
SYSTEM: OrderOriginScope
ORDER_TRIGGER_TYPE_UNSPECIFIED: OrderTriggerType
STOP_LOSS: OrderTriggerType
TAKE_PROFIT: OrderTriggerType
TRAILING_STOP: OrderTriggerType
TWAP: OrderTriggerType
LADDER: OrderTriggerType

class OrderOrigin(_message.Message):
    __slots__ = ("scope", "trigger_type", "trigger_id", "parent_order_id", "child_seq")
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_TYPE_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_ID_FIELD_NUMBER: _ClassVar[int]
    PARENT_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    CHILD_SEQ_FIELD_NUMBER: _ClassVar[int]
    scope: OrderOriginScope
    trigger_type: OrderTriggerType
    trigger_id: int
    parent_order_id: int
    child_seq: int
    def __init__(self, scope: _Optional[_Union[OrderOriginScope, str]] = ..., trigger_type: _Optional[_Union[OrderTriggerType, str]] = ..., trigger_id: _Optional[int] = ..., parent_order_id: _Optional[int] = ..., child_seq: _Optional[int] = ...) -> None: ...

class AttachedRiskLegState(_message.Message):
    __slots__ = ("status", "armed_ts_ns", "terminal_ts_ns", "trigger_id", "child_order_id")
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        STATUS_UNSPECIFIED: _ClassVar[AttachedRiskLegState.Status]
        NOT_CONFIGURED: _ClassVar[AttachedRiskLegState.Status]
        CREATED: _ClassVar[AttachedRiskLegState.Status]
        ARMED: _ClassVar[AttachedRiskLegState.Status]
        RUNNING: _ClassVar[AttachedRiskLegState.Status]
        COMPLETED: _ClassVar[AttachedRiskLegState.Status]
        CANCELED: _ClassVar[AttachedRiskLegState.Status]
        FAILED: _ClassVar[AttachedRiskLegState.Status]
        PAUSED: _ClassVar[AttachedRiskLegState.Status]
    STATUS_UNSPECIFIED: AttachedRiskLegState.Status
    NOT_CONFIGURED: AttachedRiskLegState.Status
    CREATED: AttachedRiskLegState.Status
    ARMED: AttachedRiskLegState.Status
    RUNNING: AttachedRiskLegState.Status
    COMPLETED: AttachedRiskLegState.Status
    CANCELED: AttachedRiskLegState.Status
    FAILED: AttachedRiskLegState.Status
    PAUSED: AttachedRiskLegState.Status
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ARMED_TS_NS_FIELD_NUMBER: _ClassVar[int]
    TERMINAL_TS_NS_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_ID_FIELD_NUMBER: _ClassVar[int]
    CHILD_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    status: AttachedRiskLegState.Status
    armed_ts_ns: int
    terminal_ts_ns: int
    trigger_id: int
    child_order_id: int
    def __init__(self, status: _Optional[_Union[AttachedRiskLegState.Status, str]] = ..., armed_ts_ns: _Optional[int] = ..., terminal_ts_ns: _Optional[int] = ..., trigger_id: _Optional[int] = ..., child_order_id: _Optional[int] = ...) -> None: ...

class AttachedRiskTakeProfit(_message.Message):
    __slots__ = ("policy", "state")
    POLICY_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    policy: _orders_pb2.TakeProfitPolicy
    state: AttachedRiskLegState
    def __init__(self, policy: _Optional[_Union[_orders_pb2.TakeProfitPolicy, _Mapping]] = ..., state: _Optional[_Union[AttachedRiskLegState, _Mapping]] = ...) -> None: ...

class AttachedRiskStopLoss(_message.Message):
    __slots__ = ("policy", "state")
    POLICY_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    policy: _orders_pb2.StopLossPolicy
    state: AttachedRiskLegState
    def __init__(self, policy: _Optional[_Union[_orders_pb2.StopLossPolicy, _Mapping]] = ..., state: _Optional[_Union[AttachedRiskLegState, _Mapping]] = ...) -> None: ...

class AttachedRiskTrailingStop(_message.Message):
    __slots__ = ("policy", "state")
    POLICY_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    policy: _orders_pb2.TrailingStopPolicy
    state: AttachedRiskLegState
    def __init__(self, policy: _Optional[_Union[_orders_pb2.TrailingStopPolicy, _Mapping]] = ..., state: _Optional[_Union[AttachedRiskLegState, _Mapping]] = ...) -> None: ...

class AttachedRisk(_message.Message):
    __slots__ = ("take_profit", "stop_loss", "trailing_stop", "oco")
    TAKE_PROFIT_FIELD_NUMBER: _ClassVar[int]
    STOP_LOSS_FIELD_NUMBER: _ClassVar[int]
    TRAILING_STOP_FIELD_NUMBER: _ClassVar[int]
    OCO_FIELD_NUMBER: _ClassVar[int]
    take_profit: AttachedRiskTakeProfit
    stop_loss: AttachedRiskStopLoss
    trailing_stop: AttachedRiskTrailingStop
    oco: bool
    def __init__(self, take_profit: _Optional[_Union[AttachedRiskTakeProfit, _Mapping]] = ..., stop_loss: _Optional[_Union[AttachedRiskStopLoss, _Mapping]] = ..., trailing_stop: _Optional[_Union[AttachedRiskTrailingStop, _Mapping]] = ..., oco: _Optional[bool] = ...) -> None: ...

class OrderLineage(_message.Message):
    __slots__ = ("id", "generation")
    ID_FIELD_NUMBER: _ClassVar[int]
    GENERATION_FIELD_NUMBER: _ClassVar[int]
    id: int
    generation: int
    def __init__(self, id: _Optional[int] = ..., generation: _Optional[int] = ...) -> None: ...

class Order(_message.Message):
    __slots__ = ("order_id", "symbol_id", "client_order_id", "side", "status", "order_type", "time_in_force", "self_trade_prevention_mode", "fee_asset", "post_only", "orig_qty_scaled", "cum_qty_scaled", "inherited_cum_qty_scaled", "leaves_qty_scaled", "avg_price_ticks", "price_ticks", "created_ts_ns", "terminal_ts_ns", "reject_reason", "cancel_reason", "attached_risk", "origin", "market_client_ref_price_ticks", "market_max_slippage_ticks", "market_max_slippage_bps", "version", "batch_request_id", "submitted_max_quote_debit_scaled", "lineage", "expire_at")
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    SIDE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ORDER_TYPE_FIELD_NUMBER: _ClassVar[int]
    TIME_IN_FORCE_FIELD_NUMBER: _ClassVar[int]
    SELF_TRADE_PREVENTION_MODE_FIELD_NUMBER: _ClassVar[int]
    FEE_ASSET_FIELD_NUMBER: _ClassVar[int]
    POST_ONLY_FIELD_NUMBER: _ClassVar[int]
    ORIG_QTY_SCALED_FIELD_NUMBER: _ClassVar[int]
    CUM_QTY_SCALED_FIELD_NUMBER: _ClassVar[int]
    INHERITED_CUM_QTY_SCALED_FIELD_NUMBER: _ClassVar[int]
    LEAVES_QTY_SCALED_FIELD_NUMBER: _ClassVar[int]
    AVG_PRICE_TICKS_FIELD_NUMBER: _ClassVar[int]
    PRICE_TICKS_FIELD_NUMBER: _ClassVar[int]
    CREATED_TS_NS_FIELD_NUMBER: _ClassVar[int]
    TERMINAL_TS_NS_FIELD_NUMBER: _ClassVar[int]
    REJECT_REASON_FIELD_NUMBER: _ClassVar[int]
    CANCEL_REASON_FIELD_NUMBER: _ClassVar[int]
    ATTACHED_RISK_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    MARKET_CLIENT_REF_PRICE_TICKS_FIELD_NUMBER: _ClassVar[int]
    MARKET_MAX_SLIPPAGE_TICKS_FIELD_NUMBER: _ClassVar[int]
    MARKET_MAX_SLIPPAGE_BPS_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    BATCH_REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    SUBMITTED_MAX_QUOTE_DEBIT_SCALED_FIELD_NUMBER: _ClassVar[int]
    LINEAGE_FIELD_NUMBER: _ClassVar[int]
    EXPIRE_AT_FIELD_NUMBER: _ClassVar[int]
    order_id: int
    symbol_id: int
    client_order_id: str
    side: _orders_pb2.Side
    status: OrderStatus
    order_type: _orders_pb2.OrderType
    time_in_force: _orders_pb2.TimeInForce
    self_trade_prevention_mode: _orders_pb2.SelfTradePreventionMode
    fee_asset: _orders_pb2.FeeAsset
    post_only: bool
    orig_qty_scaled: int
    cum_qty_scaled: int
    inherited_cum_qty_scaled: int
    leaves_qty_scaled: int
    avg_price_ticks: int
    price_ticks: int
    created_ts_ns: int
    terminal_ts_ns: int
    reject_reason: _orders_pb2.ErrorCode
    cancel_reason: CancelReason
    attached_risk: AttachedRisk
    origin: OrderOrigin
    market_client_ref_price_ticks: int
    market_max_slippage_ticks: int
    market_max_slippage_bps: int
    version: int
    batch_request_id: int
    submitted_max_quote_debit_scaled: int
    lineage: OrderLineage
    expire_at: _timestamp_pb2.Timestamp
    def __init__(self, order_id: _Optional[int] = ..., symbol_id: _Optional[int] = ..., client_order_id: _Optional[str] = ..., side: _Optional[_Union[_orders_pb2.Side, str]] = ..., status: _Optional[_Union[OrderStatus, str]] = ..., order_type: _Optional[_Union[_orders_pb2.OrderType, str]] = ..., time_in_force: _Optional[_Union[_orders_pb2.TimeInForce, str]] = ..., self_trade_prevention_mode: _Optional[_Union[_orders_pb2.SelfTradePreventionMode, str]] = ..., fee_asset: _Optional[_Union[_orders_pb2.FeeAsset, str]] = ..., post_only: _Optional[bool] = ..., orig_qty_scaled: _Optional[int] = ..., cum_qty_scaled: _Optional[int] = ..., inherited_cum_qty_scaled: _Optional[int] = ..., leaves_qty_scaled: _Optional[int] = ..., avg_price_ticks: _Optional[int] = ..., price_ticks: _Optional[int] = ..., created_ts_ns: _Optional[int] = ..., terminal_ts_ns: _Optional[int] = ..., reject_reason: _Optional[_Union[_orders_pb2.ErrorCode, str]] = ..., cancel_reason: _Optional[_Union[CancelReason, str]] = ..., attached_risk: _Optional[_Union[AttachedRisk, _Mapping]] = ..., origin: _Optional[_Union[OrderOrigin, _Mapping]] = ..., market_client_ref_price_ticks: _Optional[int] = ..., market_max_slippage_ticks: _Optional[int] = ..., market_max_slippage_bps: _Optional[int] = ..., version: _Optional[int] = ..., batch_request_id: _Optional[int] = ..., submitted_max_quote_debit_scaled: _Optional[int] = ..., lineage: _Optional[_Union[OrderLineage, _Mapping]] = ..., expire_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class UserTrade(_message.Message):
    __slots__ = ("symbol_id", "match_id", "order_id", "side", "is_maker", "price_ticks", "qty_scaled", "fee_amount_e18", "fee_asset", "referral_share_amount_e18", "ts_ns", "fee_is_rebate", "lineage")
    SYMBOL_ID_FIELD_NUMBER: _ClassVar[int]
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    SIDE_FIELD_NUMBER: _ClassVar[int]
    IS_MAKER_FIELD_NUMBER: _ClassVar[int]
    PRICE_TICKS_FIELD_NUMBER: _ClassVar[int]
    QTY_SCALED_FIELD_NUMBER: _ClassVar[int]
    FEE_AMOUNT_E18_FIELD_NUMBER: _ClassVar[int]
    FEE_ASSET_FIELD_NUMBER: _ClassVar[int]
    REFERRAL_SHARE_AMOUNT_E18_FIELD_NUMBER: _ClassVar[int]
    TS_NS_FIELD_NUMBER: _ClassVar[int]
    FEE_IS_REBATE_FIELD_NUMBER: _ClassVar[int]
    LINEAGE_FIELD_NUMBER: _ClassVar[int]
    symbol_id: int
    match_id: int
    order_id: int
    side: _orders_pb2.Side
    is_maker: bool
    price_ticks: int
    qty_scaled: int
    fee_amount_e18: _u128_pb2.U128
    fee_asset: _orders_pb2.FeeAsset
    referral_share_amount_e18: _u128_pb2.U128
    ts_ns: int
    fee_is_rebate: bool
    lineage: OrderLineage
    def __init__(self, symbol_id: _Optional[int] = ..., match_id: _Optional[int] = ..., order_id: _Optional[int] = ..., side: _Optional[_Union[_orders_pb2.Side, str]] = ..., is_maker: _Optional[bool] = ..., price_ticks: _Optional[int] = ..., qty_scaled: _Optional[int] = ..., fee_amount_e18: _Optional[_Union[_u128_pb2.U128, _Mapping]] = ..., fee_asset: _Optional[_Union[_orders_pb2.FeeAsset, str]] = ..., referral_share_amount_e18: _Optional[_Union[_u128_pb2.U128, _Mapping]] = ..., ts_ns: _Optional[int] = ..., fee_is_rebate: _Optional[bool] = ..., lineage: _Optional[_Union[OrderLineage, _Mapping]] = ...) -> None: ...

class UserTradeBatch(_message.Message):
    __slots__ = ("events",)
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    events: _containers.RepeatedCompositeFieldContainer[UserTrade]
    def __init__(self, events: _Optional[_Iterable[_Union[UserTrade, _Mapping]]] = ...) -> None: ...

class OrderTransfer(_message.Message):
    __slots__ = ("match_id", "symbol_id", "asset_id", "amount_e18", "is_debit", "transfer_code", "account_code", "ts_ns", "tx_id")
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_ID_FIELD_NUMBER: _ClassVar[int]
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_E18_FIELD_NUMBER: _ClassVar[int]
    IS_DEBIT_FIELD_NUMBER: _ClassVar[int]
    TRANSFER_CODE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_CODE_FIELD_NUMBER: _ClassVar[int]
    TS_NS_FIELD_NUMBER: _ClassVar[int]
    TX_ID_FIELD_NUMBER: _ClassVar[int]
    match_id: int
    symbol_id: int
    asset_id: int
    amount_e18: _u128_pb2.U128
    is_debit: bool
    transfer_code: _catalog_pb2.TransferCode
    account_code: _catalog_pb2.AccountCode
    ts_ns: int
    tx_id: str
    def __init__(self, match_id: _Optional[int] = ..., symbol_id: _Optional[int] = ..., asset_id: _Optional[int] = ..., amount_e18: _Optional[_Union[_u128_pb2.U128, _Mapping]] = ..., is_debit: _Optional[bool] = ..., transfer_code: _Optional[_Union[_catalog_pb2.TransferCode, str]] = ..., account_code: _Optional[_Union[_catalog_pb2.AccountCode, str]] = ..., ts_ns: _Optional[int] = ..., tx_id: _Optional[str] = ...) -> None: ...

class GetOpenOrdersRequest(_message.Message):
    __slots__ = ("subaccount_id", "symbol_id", "side", "limit", "page_token", "include_attached_risk", "include_attached_risk_state", "trigger_id")
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_ID_FIELD_NUMBER: _ClassVar[int]
    SIDE_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_ATTACHED_RISK_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_ATTACHED_RISK_STATE_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_ID_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    symbol_id: _containers.RepeatedScalarFieldContainer[int]
    side: _orders_pb2.Side
    limit: int
    page_token: str
    include_attached_risk: bool
    include_attached_risk_state: bool
    trigger_id: int
    def __init__(self, subaccount_id: _Optional[int] = ..., symbol_id: _Optional[_Iterable[int]] = ..., side: _Optional[_Union[_orders_pb2.Side, str]] = ..., limit: _Optional[int] = ..., page_token: _Optional[str] = ..., include_attached_risk: _Optional[bool] = ..., include_attached_risk_state: _Optional[bool] = ..., trigger_id: _Optional[int] = ...) -> None: ...

class GetOpenOrdersResponse(_message.Message):
    __slots__ = ("orders", "next_page_token")
    ORDERS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    orders: _containers.RepeatedCompositeFieldContainer[Order]
    next_page_token: str
    def __init__(self, orders: _Optional[_Iterable[_Union[Order, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class GetOrderHistoryRequest(_message.Message):
    __slots__ = ("subaccount_id", "symbol_id", "side", "status", "start_ts_ns", "end_ts_ns", "limit", "page_token", "include_attached_risk", "include_attached_risk_state", "trigger_id")
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_ID_FIELD_NUMBER: _ClassVar[int]
    SIDE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    START_TS_NS_FIELD_NUMBER: _ClassVar[int]
    END_TS_NS_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_ATTACHED_RISK_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_ATTACHED_RISK_STATE_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_ID_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    symbol_id: _containers.RepeatedScalarFieldContainer[int]
    side: _orders_pb2.Side
    status: OrderStatus
    start_ts_ns: int
    end_ts_ns: int
    limit: int
    page_token: str
    include_attached_risk: bool
    include_attached_risk_state: bool
    trigger_id: int
    def __init__(self, subaccount_id: _Optional[int] = ..., symbol_id: _Optional[_Iterable[int]] = ..., side: _Optional[_Union[_orders_pb2.Side, str]] = ..., status: _Optional[_Union[OrderStatus, str]] = ..., start_ts_ns: _Optional[int] = ..., end_ts_ns: _Optional[int] = ..., limit: _Optional[int] = ..., page_token: _Optional[str] = ..., include_attached_risk: _Optional[bool] = ..., include_attached_risk_state: _Optional[bool] = ..., trigger_id: _Optional[int] = ...) -> None: ...

class GetOrderHistoryResponse(_message.Message):
    __slots__ = ("orders", "next_page_token")
    ORDERS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    orders: _containers.RepeatedCompositeFieldContainer[Order]
    next_page_token: str
    def __init__(self, orders: _Optional[_Iterable[_Union[Order, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class GetUserTradesRequest(_message.Message):
    __slots__ = ("subaccount_id", "symbol_id", "side", "start_ts_ns", "end_ts_ns", "limit", "page_token", "after_match_id", "order_id", "lineage_id", "through_generation", "include_transfers")
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_ID_FIELD_NUMBER: _ClassVar[int]
    SIDE_FIELD_NUMBER: _ClassVar[int]
    START_TS_NS_FIELD_NUMBER: _ClassVar[int]
    END_TS_NS_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    AFTER_MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    LINEAGE_ID_FIELD_NUMBER: _ClassVar[int]
    THROUGH_GENERATION_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_TRANSFERS_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    symbol_id: int
    side: _orders_pb2.Side
    start_ts_ns: int
    end_ts_ns: int
    limit: int
    page_token: str
    after_match_id: int
    order_id: int
    lineage_id: int
    through_generation: int
    include_transfers: bool
    def __init__(self, subaccount_id: _Optional[int] = ..., symbol_id: _Optional[int] = ..., side: _Optional[_Union[_orders_pb2.Side, str]] = ..., start_ts_ns: _Optional[int] = ..., end_ts_ns: _Optional[int] = ..., limit: _Optional[int] = ..., page_token: _Optional[str] = ..., after_match_id: _Optional[int] = ..., order_id: _Optional[int] = ..., lineage_id: _Optional[int] = ..., through_generation: _Optional[int] = ..., include_transfers: _Optional[bool] = ...) -> None: ...

class GetUserTradesResponse(_message.Message):
    __slots__ = ("trades", "next_page_token", "transfers")
    TRADES_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TRANSFERS_FIELD_NUMBER: _ClassVar[int]
    trades: _containers.RepeatedCompositeFieldContainer[UserTrade]
    next_page_token: str
    transfers: _containers.RepeatedCompositeFieldContainer[OrderTransfer]
    def __init__(self, trades: _Optional[_Iterable[_Union[UserTrade, _Mapping]]] = ..., next_page_token: _Optional[str] = ..., transfers: _Optional[_Iterable[_Union[OrderTransfer, _Mapping]]] = ...) -> None: ...

class GetOrderRequest(_message.Message):
    __slots__ = ("subaccount_id", "order_id", "client_order_id", "include_attached_risk", "include_attached_risk_state", "include_execution_history", "limit", "page_token")
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_ATTACHED_RISK_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_ATTACHED_RISK_STATE_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_EXECUTION_HISTORY_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    order_id: int
    client_order_id: str
    include_attached_risk: bool
    include_attached_risk_state: bool
    include_execution_history: bool
    limit: int
    page_token: str
    def __init__(self, subaccount_id: _Optional[int] = ..., order_id: _Optional[int] = ..., client_order_id: _Optional[str] = ..., include_attached_risk: _Optional[bool] = ..., include_attached_risk_state: _Optional[bool] = ..., include_execution_history: _Optional[bool] = ..., limit: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class GetOrderResponse(_message.Message):
    __slots__ = ("order", "trades", "transfers", "next_page_token", "executions_complete")
    ORDER_FIELD_NUMBER: _ClassVar[int]
    TRADES_FIELD_NUMBER: _ClassVar[int]
    TRANSFERS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    EXECUTIONS_COMPLETE_FIELD_NUMBER: _ClassVar[int]
    order: Order
    trades: _containers.RepeatedCompositeFieldContainer[UserTrade]
    transfers: _containers.RepeatedCompositeFieldContainer[OrderTransfer]
    next_page_token: str
    executions_complete: bool
    def __init__(self, order: _Optional[_Union[Order, _Mapping]] = ..., trades: _Optional[_Iterable[_Union[UserTrade, _Mapping]]] = ..., transfers: _Optional[_Iterable[_Union[OrderTransfer, _Mapping]]] = ..., next_page_token: _Optional[str] = ..., executions_complete: _Optional[bool] = ...) -> None: ...

class GetBatchReplaceStatusRequest(_message.Message):
    __slots__ = ("subaccount_id", "batch_request_id")
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    BATCH_REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    batch_request_id: int
    def __init__(self, subaccount_id: _Optional[int] = ..., batch_request_id: _Optional[int] = ...) -> None: ...

class BatchReplaceStatusItem(_message.Message):
    __slots__ = ("item_index", "phase", "old_order_id", "replacement_order_id", "order_status", "code", "updated_ts_ns", "action_taken")
    ITEM_INDEX_FIELD_NUMBER: _ClassVar[int]
    PHASE_FIELD_NUMBER: _ClassVar[int]
    OLD_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    REPLACEMENT_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    ORDER_STATUS_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    UPDATED_TS_NS_FIELD_NUMBER: _ClassVar[int]
    ACTION_TAKEN_FIELD_NUMBER: _ClassVar[int]
    item_index: int
    phase: BatchReplacePhase
    old_order_id: int
    replacement_order_id: int
    order_status: OrderStatus
    code: str
    updated_ts_ns: int
    action_taken: _orders_pb2.ModifyActionTaken
    def __init__(self, item_index: _Optional[int] = ..., phase: _Optional[_Union[BatchReplacePhase, str]] = ..., old_order_id: _Optional[int] = ..., replacement_order_id: _Optional[int] = ..., order_status: _Optional[_Union[OrderStatus, str]] = ..., code: _Optional[str] = ..., updated_ts_ns: _Optional[int] = ..., action_taken: _Optional[_Union[_orders_pb2.ModifyActionTaken, str]] = ...) -> None: ...

class GetBatchReplaceStatusResponse(_message.Message):
    __slots__ = ("batch_request_id", "admission_status", "items", "accepted_count", "rejected_count", "accepted_ts_ns", "updated_ts_ns")
    BATCH_REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    ADMISSION_STATUS_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    ACCEPTED_COUNT_FIELD_NUMBER: _ClassVar[int]
    REJECTED_COUNT_FIELD_NUMBER: _ClassVar[int]
    ACCEPTED_TS_NS_FIELD_NUMBER: _ClassVar[int]
    UPDATED_TS_NS_FIELD_NUMBER: _ClassVar[int]
    batch_request_id: int
    admission_status: _orders_pb2.BatchReplaceAdmissionStatus
    items: _containers.RepeatedCompositeFieldContainer[BatchReplaceStatusItem]
    accepted_count: int
    rejected_count: int
    accepted_ts_ns: int
    updated_ts_ns: int
    def __init__(self, batch_request_id: _Optional[int] = ..., admission_status: _Optional[_Union[_orders_pb2.BatchReplaceAdmissionStatus, str]] = ..., items: _Optional[_Iterable[_Union[BatchReplaceStatusItem, _Mapping]]] = ..., accepted_count: _Optional[int] = ..., rejected_count: _Optional[int] = ..., accepted_ts_ns: _Optional[int] = ..., updated_ts_ns: _Optional[int] = ...) -> None: ...
