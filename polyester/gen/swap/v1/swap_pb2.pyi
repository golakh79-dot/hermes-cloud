import datetime

from polyester.gen.buf.validate import validate_pb2 as _validate_pb2
from polyester.gen.gnostic.openapi.v3 import annotations_pb2 as _annotations_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from polyester.gen.polyester.api import options_pb2 as _options_pb2
from polyester.gen.polyester.type.v1 import u128_pb2 as _u128_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Side(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SIDE_UNSPECIFIED: _ClassVar[Side]
    BUY: _ClassVar[Side]
    SELL: _ClassVar[Side]

class SwapStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STATUS_UNSPECIFIED: _ClassVar[SwapStatus]
    EXECUTING: _ClassVar[SwapStatus]
    COMPLETED: _ClassVar[SwapStatus]
    PARTIALLY_COMPLETED: _ClassVar[SwapStatus]
    FAILED: _ClassVar[SwapStatus]
    RECONCILING: _ClassVar[SwapStatus]

class SwapReason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    REASON_UNSPECIFIED: _ClassVar[SwapReason]
    INSUFFICIENT_BALANCE: _ClassVar[SwapReason]
    PRICE_PROTECTION: _ClassVar[SwapReason]
    MARKET_UNAVAILABLE: _ClassVar[SwapReason]
    ORDER_SIZE_OUT_OF_RANGE: _ClassVar[SwapReason]
    RATE_LIMITED: _ClassVar[SwapReason]
    ORDER_REJECTED: _ClassVar[SwapReason]
    EXPIRED: _ClassVar[SwapReason]
    MINIMUM_NOT_MET: _ClassVar[SwapReason]
    MAX_ORDER_QUANTITY: _ClassVar[SwapReason]

class SwapOrderStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ORDER_STATUS_UNSPECIFIED: _ClassVar[SwapOrderStatus]
    PLACING: _ClassVar[SwapOrderStatus]
    PLACED: _ClassVar[SwapOrderStatus]
    REFUSED: _ClassVar[SwapOrderStatus]
    NOT_PLACED: _ClassVar[SwapOrderStatus]
    UNCONFIRMED: _ClassVar[SwapOrderStatus]

class ErrorCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ERROR_UNSPECIFIED: _ClassVar[ErrorCode]
    ROUTE_UNSUPPORTED: _ClassVar[ErrorCode]
    AMOUNT_OUT_OF_RANGE: _ClassVar[ErrorCode]
    QUOTE_UNAVAILABLE: _ClassVar[ErrorCode]
    PROTECTION_UNACHIEVABLE: _ClassVar[ErrorCode]
    QUOTE_EXPIRED: _ClassVar[ErrorCode]
    IDEMPOTENCY_CONFLICT: _ClassVar[ErrorCode]
    SWAP_NOT_FOUND: _ClassVar[ErrorCode]
    INVALID_SUBACCOUNT_ID: _ClassVar[ErrorCode]
    SUBACCOUNT_NOT_FOUND: _ClassVar[ErrorCode]
    SUBACCOUNT_INACTIVE: _ClassVar[ErrorCode]
    SWAP_NOT_PERMITTED: _ClassVar[ErrorCode]
    SERVICE_UNAVAILABLE: _ClassVar[ErrorCode]
    DIRECTION_UNSUPPORTED: _ClassVar[ErrorCode]
SIDE_UNSPECIFIED: Side
BUY: Side
SELL: Side
STATUS_UNSPECIFIED: SwapStatus
EXECUTING: SwapStatus
COMPLETED: SwapStatus
PARTIALLY_COMPLETED: SwapStatus
FAILED: SwapStatus
RECONCILING: SwapStatus
REASON_UNSPECIFIED: SwapReason
INSUFFICIENT_BALANCE: SwapReason
PRICE_PROTECTION: SwapReason
MARKET_UNAVAILABLE: SwapReason
ORDER_SIZE_OUT_OF_RANGE: SwapReason
RATE_LIMITED: SwapReason
ORDER_REJECTED: SwapReason
EXPIRED: SwapReason
MINIMUM_NOT_MET: SwapReason
MAX_ORDER_QUANTITY: SwapReason
ORDER_STATUS_UNSPECIFIED: SwapOrderStatus
PLACING: SwapOrderStatus
PLACED: SwapOrderStatus
REFUSED: SwapOrderStatus
NOT_PLACED: SwapOrderStatus
UNCONFIRMED: SwapOrderStatus
ERROR_UNSPECIFIED: ErrorCode
ROUTE_UNSUPPORTED: ErrorCode
AMOUNT_OUT_OF_RANGE: ErrorCode
QUOTE_UNAVAILABLE: ErrorCode
PROTECTION_UNACHIEVABLE: ErrorCode
QUOTE_EXPIRED: ErrorCode
IDEMPOTENCY_CONFLICT: ErrorCode
SWAP_NOT_FOUND: ErrorCode
INVALID_SUBACCOUNT_ID: ErrorCode
SUBACCOUNT_NOT_FOUND: ErrorCode
SUBACCOUNT_INACTIVE: ErrorCode
SWAP_NOT_PERMITTED: ErrorCode
SERVICE_UNAVAILABLE: ErrorCode
DIRECTION_UNSUPPORTED: ErrorCode

class SwapTerms(_message.Message):
    __slots__ = ("subaccount_id", "source_asset_id", "destination_asset_id", "amount_e18")
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_E18_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    source_asset_id: int
    destination_asset_id: int
    amount_e18: _u128_pb2.U128
    def __init__(self, subaccount_id: _Optional[int] = ..., source_asset_id: _Optional[int] = ..., destination_asset_id: _Optional[int] = ..., amount_e18: _Optional[_Union[_u128_pb2.U128, _Mapping]] = ...) -> None: ...

class SwapQuoteLeg(_message.Message):
    __slots__ = ("symbol_id", "side", "average_price", "price_impact_bps", "taker_fee_rate_percent", "fee_e18", "fee_asset_id")
    SYMBOL_ID_FIELD_NUMBER: _ClassVar[int]
    SIDE_FIELD_NUMBER: _ClassVar[int]
    AVERAGE_PRICE_FIELD_NUMBER: _ClassVar[int]
    PRICE_IMPACT_BPS_FIELD_NUMBER: _ClassVar[int]
    TAKER_FEE_RATE_PERCENT_FIELD_NUMBER: _ClassVar[int]
    FEE_E18_FIELD_NUMBER: _ClassVar[int]
    FEE_ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    symbol_id: int
    side: Side
    average_price: str
    price_impact_bps: int
    taker_fee_rate_percent: str
    fee_e18: _u128_pb2.U128
    fee_asset_id: int
    def __init__(self, symbol_id: _Optional[int] = ..., side: _Optional[_Union[Side, str]] = ..., average_price: _Optional[str] = ..., price_impact_bps: _Optional[int] = ..., taker_fee_rate_percent: _Optional[str] = ..., fee_e18: _Optional[_Union[_u128_pb2.U128, _Mapping]] = ..., fee_asset_id: _Optional[int] = ...) -> None: ...

class SwapQuote(_message.Message):
    __slots__ = ("terms", "legs", "expected_amount_out_e18", "min_amount_out_e18", "quoted_at", "expires_at")
    TERMS_FIELD_NUMBER: _ClassVar[int]
    LEGS_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_AMOUNT_OUT_E18_FIELD_NUMBER: _ClassVar[int]
    MIN_AMOUNT_OUT_E18_FIELD_NUMBER: _ClassVar[int]
    QUOTED_AT_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    terms: SwapTerms
    legs: _containers.RepeatedCompositeFieldContainer[SwapQuoteLeg]
    expected_amount_out_e18: _u128_pb2.U128
    min_amount_out_e18: _u128_pb2.U128
    quoted_at: _timestamp_pb2.Timestamp
    expires_at: _timestamp_pb2.Timestamp
    def __init__(self, terms: _Optional[_Union[SwapTerms, _Mapping]] = ..., legs: _Optional[_Iterable[_Union[SwapQuoteLeg, _Mapping]]] = ..., expected_amount_out_e18: _Optional[_Union[_u128_pb2.U128, _Mapping]] = ..., min_amount_out_e18: _Optional[_Union[_u128_pb2.U128, _Mapping]] = ..., quoted_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., expires_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class SwapOrder(_message.Message):
    __slots__ = ("order_id", "symbol_id", "side", "leg", "status", "limit_price_ticks", "spent_e18", "received_e18", "fee_e18")
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_ID_FIELD_NUMBER: _ClassVar[int]
    SIDE_FIELD_NUMBER: _ClassVar[int]
    LEG_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    LIMIT_PRICE_TICKS_FIELD_NUMBER: _ClassVar[int]
    SPENT_E18_FIELD_NUMBER: _ClassVar[int]
    RECEIVED_E18_FIELD_NUMBER: _ClassVar[int]
    FEE_E18_FIELD_NUMBER: _ClassVar[int]
    order_id: int
    symbol_id: int
    side: Side
    leg: int
    status: SwapOrderStatus
    limit_price_ticks: int
    spent_e18: _u128_pb2.U128
    received_e18: _u128_pb2.U128
    fee_e18: _u128_pb2.U128
    def __init__(self, order_id: _Optional[int] = ..., symbol_id: _Optional[int] = ..., side: _Optional[_Union[Side, str]] = ..., leg: _Optional[int] = ..., status: _Optional[_Union[SwapOrderStatus, str]] = ..., limit_price_ticks: _Optional[int] = ..., spent_e18: _Optional[_Union[_u128_pb2.U128, _Mapping]] = ..., received_e18: _Optional[_Union[_u128_pb2.U128, _Mapping]] = ..., fee_e18: _Optional[_Union[_u128_pb2.U128, _Mapping]] = ...) -> None: ...

class Swap(_message.Message):
    __slots__ = ("swap_id", "idempotency_key", "subaccount_id", "source_asset_id", "destination_asset_id", "amount_e18", "min_amount_out_e18", "status", "reason", "is_terminal", "executed_amount_e18", "unspent_amount_e18", "received_amount_e18", "fee_e18", "orders", "created_at")
    SWAP_ID_FIELD_NUMBER: _ClassVar[int]
    IDEMPOTENCY_KEY_FIELD_NUMBER: _ClassVar[int]
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_E18_FIELD_NUMBER: _ClassVar[int]
    MIN_AMOUNT_OUT_E18_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    IS_TERMINAL_FIELD_NUMBER: _ClassVar[int]
    EXECUTED_AMOUNT_E18_FIELD_NUMBER: _ClassVar[int]
    UNSPENT_AMOUNT_E18_FIELD_NUMBER: _ClassVar[int]
    RECEIVED_AMOUNT_E18_FIELD_NUMBER: _ClassVar[int]
    FEE_E18_FIELD_NUMBER: _ClassVar[int]
    ORDERS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    swap_id: int
    idempotency_key: str
    subaccount_id: int
    source_asset_id: int
    destination_asset_id: int
    amount_e18: _u128_pb2.U128
    min_amount_out_e18: _u128_pb2.U128
    status: SwapStatus
    reason: SwapReason
    is_terminal: bool
    executed_amount_e18: _u128_pb2.U128
    unspent_amount_e18: _u128_pb2.U128
    received_amount_e18: _u128_pb2.U128
    fee_e18: _u128_pb2.U128
    orders: _containers.RepeatedCompositeFieldContainer[SwapOrder]
    created_at: _timestamp_pb2.Timestamp
    def __init__(self, swap_id: _Optional[int] = ..., idempotency_key: _Optional[str] = ..., subaccount_id: _Optional[int] = ..., source_asset_id: _Optional[int] = ..., destination_asset_id: _Optional[int] = ..., amount_e18: _Optional[_Union[_u128_pb2.U128, _Mapping]] = ..., min_amount_out_e18: _Optional[_Union[_u128_pb2.U128, _Mapping]] = ..., status: _Optional[_Union[SwapStatus, str]] = ..., reason: _Optional[_Union[SwapReason, str]] = ..., is_terminal: _Optional[bool] = ..., executed_amount_e18: _Optional[_Union[_u128_pb2.U128, _Mapping]] = ..., unspent_amount_e18: _Optional[_Union[_u128_pb2.U128, _Mapping]] = ..., received_amount_e18: _Optional[_Union[_u128_pb2.U128, _Mapping]] = ..., fee_e18: _Optional[_Union[_u128_pb2.U128, _Mapping]] = ..., orders: _Optional[_Iterable[_Union[SwapOrder, _Mapping]]] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class QuoteSwapRequest(_message.Message):
    __slots__ = ("terms", "max_slippage_bps")
    TERMS_FIELD_NUMBER: _ClassVar[int]
    MAX_SLIPPAGE_BPS_FIELD_NUMBER: _ClassVar[int]
    terms: SwapTerms
    max_slippage_bps: int
    def __init__(self, terms: _Optional[_Union[SwapTerms, _Mapping]] = ..., max_slippage_bps: _Optional[int] = ...) -> None: ...

class QuoteSwapResponse(_message.Message):
    __slots__ = ("quote",)
    QUOTE_FIELD_NUMBER: _ClassVar[int]
    quote: SwapQuote
    def __init__(self, quote: _Optional[_Union[SwapQuote, _Mapping]] = ...) -> None: ...

class CreateSwapRequest(_message.Message):
    __slots__ = ("idempotency_key", "terms", "min_amount_out_e18", "quote_expires_at")
    IDEMPOTENCY_KEY_FIELD_NUMBER: _ClassVar[int]
    TERMS_FIELD_NUMBER: _ClassVar[int]
    MIN_AMOUNT_OUT_E18_FIELD_NUMBER: _ClassVar[int]
    QUOTE_EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    idempotency_key: str
    terms: SwapTerms
    min_amount_out_e18: _u128_pb2.U128
    quote_expires_at: _timestamp_pb2.Timestamp
    def __init__(self, idempotency_key: _Optional[str] = ..., terms: _Optional[_Union[SwapTerms, _Mapping]] = ..., min_amount_out_e18: _Optional[_Union[_u128_pb2.U128, _Mapping]] = ..., quote_expires_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class CreateSwapResponse(_message.Message):
    __slots__ = ("swap",)
    SWAP_FIELD_NUMBER: _ClassVar[int]
    swap: Swap
    def __init__(self, swap: _Optional[_Union[Swap, _Mapping]] = ...) -> None: ...

class GetSwapRequest(_message.Message):
    __slots__ = ("swap_id", "idempotency_key")
    SWAP_ID_FIELD_NUMBER: _ClassVar[int]
    IDEMPOTENCY_KEY_FIELD_NUMBER: _ClassVar[int]
    swap_id: int
    idempotency_key: str
    def __init__(self, swap_id: _Optional[int] = ..., idempotency_key: _Optional[str] = ...) -> None: ...

class GetSwapResponse(_message.Message):
    __slots__ = ("swap",)
    SWAP_FIELD_NUMBER: _ClassVar[int]
    swap: Swap
    def __init__(self, swap: _Optional[_Union[Swap, _Mapping]] = ...) -> None: ...

class ErrorDetail(_message.Message):
    __slots__ = ("code", "swap_id", "min_amount_e18", "max_amount_e18")
    CODE_FIELD_NUMBER: _ClassVar[int]
    SWAP_ID_FIELD_NUMBER: _ClassVar[int]
    MIN_AMOUNT_E18_FIELD_NUMBER: _ClassVar[int]
    MAX_AMOUNT_E18_FIELD_NUMBER: _ClassVar[int]
    code: ErrorCode
    swap_id: int
    min_amount_e18: _u128_pb2.U128
    max_amount_e18: _u128_pb2.U128
    def __init__(self, code: _Optional[_Union[ErrorCode, str]] = ..., swap_id: _Optional[int] = ..., min_amount_e18: _Optional[_Union[_u128_pb2.U128, _Mapping]] = ..., max_amount_e18: _Optional[_Union[_u128_pb2.U128, _Mapping]] = ...) -> None: ...
