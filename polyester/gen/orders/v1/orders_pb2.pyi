import datetime

from polyester.gen.buf.validate import validate_pb2 as _validate_pb2
from polyester.gen.gnostic.openapi.v3 import annotations_pb2 as _annotations_pb2
from polyester.gen.google.api import field_behavior_pb2 as _field_behavior_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from polyester.gen.polyester.api import options_pb2 as _options_pb2
from polyester.gen.polyester.ratelimit.v1 import types_pb2 as _types_pb2
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

class OrderType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ORDER_TYPE_UNSPECIFIED: _ClassVar[OrderType]
    LIMIT: _ClassVar[OrderType]
    MARKET: _ClassVar[OrderType]

class TimeInForce(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TIME_IN_FORCE_UNSPECIFIED: _ClassVar[TimeInForce]
    GTC: _ClassVar[TimeInForce]
    IOC: _ClassVar[TimeInForce]
    FOK: _ClassVar[TimeInForce]
    GTD: _ClassVar[TimeInForce]

class FeeAsset(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FEE_ASSET_UNSPECIFIED: _ClassVar[FeeAsset]
    QUOTE: _ClassVar[FeeAsset]
    BASE: _ClassVar[FeeAsset]

class SelfTradePreventionMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SELF_TRADE_PREVENTION_MODE_UNSPECIFIED: _ClassVar[SelfTradePreventionMode]
    EXPIRE_MAKER: _ClassVar[SelfTradePreventionMode]
    EXPIRE_TAKER: _ClassVar[SelfTradePreventionMode]
    EXPIRE_BOTH: _ClassVar[SelfTradePreventionMode]

class ErrorCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ERROR_CODE_UNSPECIFIED: _ClassVar[ErrorCode]
    ERROR_CODE_BAD_REQUEST: _ClassVar[ErrorCode]
    ERROR_CODE_INVALID_ARGUMENT: _ClassVar[ErrorCode]
    ERROR_CODE_INSUFFICIENT_FUNDS: _ClassVar[ErrorCode]
    ERROR_CODE_UNKNOWN_SYMBOL: _ClassVar[ErrorCode]
    ERROR_CODE_BAD_PRICE: _ClassVar[ErrorCode]
    ERROR_CODE_BAD_QTY: _ClassVar[ErrorCode]
    ERROR_CODE_MIN_NOTIONAL: _ClassVar[ErrorCode]
    ERROR_CODE_QTY_STEP_SIZE: _ClassVar[ErrorCode]
    ERROR_CODE_CONFLICT_DUPLICATE_CLIENT_ORDER_ID: _ClassVar[ErrorCode]
    ERROR_CODE_UNAVAILABLE: _ClassVar[ErrorCode]
    ERROR_CODE_UNAUTHENTICATED: _ClassVar[ErrorCode]
    ERROR_CODE_PERMISSION_DENIED: _ClassVar[ErrorCode]
    ERROR_CODE_NOT_FOUND: _ClassVar[ErrorCode]
    ERROR_CODE_UPSTREAM_ERROR: _ClassVar[ErrorCode]
    ERROR_CODE_FEE_ASSET_NOT_ALLOWED: _ClassVar[ErrorCode]
    ERROR_CODE_PAIR_DISABLED: _ClassVar[ErrorCode]
    ERROR_CODE_ORDER_UNKNOWN: _ClassVar[ErrorCode]
    ERROR_CODE_INTERNAL_ERROR: _ClassVar[ErrorCode]
    ERROR_CODE_SUBACCOUNT_INACTIVE: _ClassVar[ErrorCode]
    ERROR_CODE_POLICY_MARKET_DENY: _ClassVar[ErrorCode]
    ERROR_CODE_POLICY_MAX_NOTIONAL: _ClassVar[ErrorCode]
    ERROR_CODE_POLICY_TRADING_HALTED: _ClassVar[ErrorCode]
    ERROR_CODE_POLICY_SPOT_TRADE_DENY: _ClassVar[ErrorCode]
    ERROR_CODE_API_KEY_ROOT_SCOPE_ONLY: _ClassVar[ErrorCode]
    ERROR_CODE_API_KEY_SUB_SCOPE_ONLY: _ClassVar[ErrorCode]
    ERROR_CODE_API_KEY_SUBACCOUNT_MISMATCH: _ClassVar[ErrorCode]
    ERROR_CODE_API_KEY_POLICY_REQUIRED: _ClassVar[ErrorCode]
    ERROR_CODE_API_KEY_UNKNOWN: _ClassVar[ErrorCode]
    ERROR_CODE_API_KEY_MARKET_DENY: _ClassVar[ErrorCode]
    ERROR_CODE_PRICE_TICK_SIZE: _ClassVar[ErrorCode]
    ERROR_CODE_MIN_QTY: _ClassVar[ErrorCode]
    ERROR_CODE_POST_ONLY_LIMIT_ONLY: _ClassVar[ErrorCode]
    ERROR_CODE_BATCH_TOO_LARGE: _ClassVar[ErrorCode]
    ERROR_CODE_POLICY_MAX_OPEN_ORDERS: _ClassVar[ErrorCode]
    ERROR_CODE_MODIFICATION_REQUIRES_REPLACE: _ClassVar[ErrorCode]
    ERROR_CODE_CONFLICT_IDEMPOTENCY_KEY_REUSE: _ClassVar[ErrorCode]
    ERROR_CODE_MARKET_PRICE_UNAVAILABLE: _ClassVar[ErrorCode]
    ERROR_CODE_PAIR_NOT_LISTED_YET: _ClassVar[ErrorCode]
    ERROR_CODE_PAIR_DELISTED: _ClassVar[ErrorCode]
    ERROR_CODE_PAIR_CANCEL_ONLY: _ClassVar[ErrorCode]
    ERROR_CODE_PAIR_POST_ONLY: _ClassVar[ErrorCode]
    ERROR_CODE_PAIR_REDUCE_ONLY: _ClassVar[ErrorCode]
    ERROR_CODE_RISK_LIMIT: _ClassVar[ErrorCode]
    ERROR_CODE_MARKET_HALTED: _ClassVar[ErrorCode]
    ERROR_CODE_ACCOUNT_UNKNOWN: _ClassVar[ErrorCode]
    ERROR_CODE_POST_ONLY_CROSS: _ClassVar[ErrorCode]
    ERROR_CODE_REDUCE_ONLY_BLOCKED: _ClassVar[ErrorCode]
    ERROR_CODE_PRICE_BAND_VIOLATION: _ClassVar[ErrorCode]
    ERROR_CODE_MARKET_CAP_VIOLATION: _ClassVar[ErrorCode]
    ERROR_CODE_EMPTY_BOOK: _ClassVar[ErrorCode]
    ERROR_CODE_FOK_INSUFFICIENT_LIQUIDITY: _ClassVar[ErrorCode]
    ERROR_CODE_ORDER_ALREADY_TERMINAL: _ClassVar[ErrorCode]
    ERROR_CODE_TRIGGER_PRICE_INVALID: _ClassVar[ErrorCode]
    ERROR_CODE_TRIGGER_PRICE_SOURCE_UNSUPPORTED: _ClassVar[ErrorCode]
    ERROR_CODE_TRAILING_DISTANCE_INVALID: _ClassVar[ErrorCode]
    ERROR_CODE_TRIGGER_NOT_FOUND: _ClassVar[ErrorCode]
    ERROR_CODE_TRIGGER_STATUS_INVALID: _ClassVar[ErrorCode]
    ERROR_CODE_TRIGGER_NOT_MODIFIABLE: _ClassVar[ErrorCode]
    ERROR_CODE_CONFLICT_DUPLICATE_CLIENT_TRIGGER_ID: _ClassVar[ErrorCode]
    ERROR_CODE_MAX_SLIPPAGE_INVALID: _ClassVar[ErrorCode]
    ERROR_CODE_STALE_QUOTE: _ClassVar[ErrorCode]
    ERROR_CODE_VALIDATION_ERROR: _ClassVar[ErrorCode]
    ERROR_CODE_OVERLOADED: _ClassVar[ErrorCode]
    ERROR_CODE_MAX_QUOTE_DEBIT_TOO_SMALL: _ClassVar[ErrorCode]
    ERROR_CODE_RATE_LIMIT_EXCEEDED: _ClassVar[ErrorCode]
    ERROR_CODE_SUBACCOUNT_READ_FORBIDDEN: _ClassVar[ErrorCode]
    ERROR_CODE_POLICY_SPOT_READ_DENY: _ClassVar[ErrorCode]
    ERROR_CODE_API_KEY_SPOT_READ_DENY: _ClassVar[ErrorCode]
    ERROR_CODE_CANCEL_REQUEST_EXPIRED: _ClassVar[ErrorCode]
    ERROR_CODE_MAX_QTY: _ClassVar[ErrorCode]
    ERROR_CODE_MAX_NOTIONAL: _ClassVar[ErrorCode]
    ERROR_CODE_QTY_AT_OR_BELOW_FILLED: _ClassVar[ErrorCode]
    ERROR_CODE_GATEWAY_MISCONFIGURED: _ClassVar[ErrorCode]
    ERROR_CODE_INVALID_ORDER_ID: _ClassVar[ErrorCode]
    ERROR_CODE_CHILD_QTY_RAISE_NOT_ALLOWED: _ClassVar[ErrorCode]
    ERROR_CODE_ATTACHED_RISK_NOT_SUPPORTED: _ClassVar[ErrorCode]
    ERROR_CODE_SETTLEMENT_BACKLOGGED: _ClassVar[ErrorCode]
    ERROR_CODE_PRICE_LEVEL_QUANTITY_LIMIT: _ClassVar[ErrorCode]
    ERROR_CODE_MARKET_QUOTE_STALE: _ClassVar[ErrorCode]
    ERROR_CODE_MARKET_QUOTE_UNHEALTHY: _ClassVar[ErrorCode]
    ERROR_CODE_INVALID_TIME_IN_FORCE: _ClassVar[ErrorCode]
    ERROR_CODE_QUICKSWAP_NOT_PERMITTED: _ClassVar[ErrorCode]
    ERROR_CODE_DUPLICATE_ORDER_ID: _ClassVar[ErrorCode]
    ERROR_CODE_MAX_OPEN_ORDERS_TOTAL: _ClassVar[ErrorCode]
    ERROR_CODE_STP_MODE_NOT_ALLOWED: _ClassVar[ErrorCode]
    ERROR_CODE_PAIR_BACKLOGGED: _ClassVar[ErrorCode]
    ERROR_CODE_PRICE_LEVELS_EXHAUSTED: _ClassVar[ErrorCode]
    ERROR_CODE_CLIENT_ORDER_IDS_EXHAUSTED: _ClassVar[ErrorCode]
    ERROR_CODE_ORDER_ID_CONFLICT: _ClassVar[ErrorCode]
    ERROR_CODE_INVALID_SIDE: _ClassVar[ErrorCode]
    ERROR_CODE_INVALID_ORDER_TYPE: _ClassVar[ErrorCode]
    ERROR_CODE_INVALID_STP_MODE: _ClassVar[ErrorCode]
    ERROR_CODE_INVALID_ORDER_FLAGS: _ClassVar[ErrorCode]
    ERROR_CODE_BATCH_OTHER_ITEM_INVALID: _ClassVar[ErrorCode]
    ERROR_CODE_REPLACE_ONTO_OWN_ID: _ClassVar[ErrorCode]
    ERROR_CODE_INVALID_CLIENT_ORDER_ID: _ClassVar[ErrorCode]
    ERROR_CODE_ORDER_SEQUENCE_EXHAUSTED: _ClassVar[ErrorCode]
    ERROR_CODE_INVALID_HANDLING_MODE: _ClassVar[ErrorCode]
    ERROR_CODE_FEE_SCHEDULE_UNAVAILABLE: _ClassVar[ErrorCode]
    ERROR_CODE_POLICY_UNAVAILABLE: _ClassVar[ErrorCode]
    ERROR_CODE_CANCEL_ALL_AFTER_TIMEOUT_INVALID: _ClassVar[ErrorCode]
    ERROR_CODE_CANCEL_SCOPE_TOO_LARGE: _ClassVar[ErrorCode]
    ERROR_CODE_RATE_LIMIT_POLICY_UNAVAILABLE: _ClassVar[ErrorCode]
    ERROR_CODE_SYSTEM_RATE_LIMITED: _ClassVar[ErrorCode]
    ERROR_CODE_ORDER_MODIFY_IN_PROGRESS: _ClassVar[ErrorCode]
    ERROR_CODE_ORDER_PLACEMENT_PENDING: _ClassVar[ErrorCode]
    ERROR_CODE_INVALID_MODIFY_BEHAVIOR: _ClassVar[ErrorCode]
    ERROR_CODE_BATCH_REPLACE_ONLY_REQUIRED: _ClassVar[ErrorCode]
    ERROR_CODE_BATCH_SINGLE_SYMBOL_REQUIRED: _ClassVar[ErrorCode]
    ERROR_CODE_REQUEST_RECEIPTS_EXHAUSTED: _ClassVar[ErrorCode]
    ERROR_CODE_INTENT_ID_INVALID: _ClassVar[ErrorCode]
    ERROR_CODE_DRY_RUN_INVALID: _ClassVar[ErrorCode]
    ERROR_CODE_CANCEL_ALL_AFTER_SCOPE_CONFLICT: _ClassVar[ErrorCode]
    ERROR_CODE_NEW_ACCOUNT_CAPACITY_REACHED: _ClassVar[ErrorCode]
    ERROR_CODE_TRIGGER_CHILD_PRICE_NOT_MODIFIABLE: _ClassVar[ErrorCode]
    ERROR_CODE_TRIGGER_GENERATIONS_EXHAUSTED: _ClassVar[ErrorCode]
    ERROR_CODE_TRIGGER_CONTROL_SHARE_EXHAUSTED: _ClassVar[ErrorCode]
    ERROR_CODE_TRIGGER_CONTROLS_BUSY: _ClassVar[ErrorCode]
    ERROR_CODE_TRIGGER_TYPE_NOT_SUPPORTED: _ClassVar[ErrorCode]
    ERROR_CODE_INVALID_TRIGGER_TYPE: _ClassVar[ErrorCode]
    ERROR_CODE_TRIGGER_DIRECTION_INVALID: _ClassVar[ErrorCode]
    ERROR_CODE_TRIGGER_QTY_INVALID: _ClassVar[ErrorCode]
    ERROR_CODE_TRIGGER_BUY_REQUIRES_LIMIT: _ClassVar[ErrorCode]
    ERROR_CODE_ACCOUNT_ROUTING_INVALID: _ClassVar[ErrorCode]
    ERROR_CODE_TRIGGER_LIMIT_EXCEEDED: _ClassVar[ErrorCode]
    ERROR_CODE_TRIGGER_CONTROL_IN_PROGRESS: _ClassVar[ErrorCode]
    ERROR_CODE_TRIGGER_PATCH_EMPTY: _ClassVar[ErrorCode]
    ERROR_CODE_CLIENT_TRIGGER_ID_INVALID: _ClassVar[ErrorCode]
    ERROR_CODE_TRIGGER_ACTIVATION_PRICE_INVALID: _ClassVar[ErrorCode]
    ERROR_CODE_SLIPPAGE_TICKS_INVALID: _ClassVar[ErrorCode]
    ERROR_CODE_SLIPPAGE_BPS_INVALID: _ClassVar[ErrorCode]
    ERROR_CODE_TRIGGER_CONTROL_OUTCOME_UNKNOWN: _ClassVar[ErrorCode]
    ERROR_CODE_TRIGGER_CAPACITY_REACHED: _ClassVar[ErrorCode]
    ERROR_CODE_RESERVATION_CAPACITY_REACHED: _ClassVar[ErrorCode]
    ERROR_CODE_CLIENT_ORDER_ID_CAPACITY_REACHED: _ClassVar[ErrorCode]
    ERROR_CODE_ACCOUNT_RESERVATION_LIMIT_REACHED: _ClassVar[ErrorCode]
    ERROR_CODE_INVALID_TRIGGER_CONTROL: _ClassVar[ErrorCode]
    ERROR_CODE_TRIGGER_PATCH_NOT_ALLOWED: _ClassVar[ErrorCode]
    ERROR_CODE_TRIGGER_PATCH_FIELD_UNKNOWN: _ClassVar[ErrorCode]
    ERROR_CODE_TRIGGER_PATCH_VALUE_UNMASKED: _ClassVar[ErrorCode]
    ERROR_CODE_TRIGGER_PATCH_PRICE_MODE_INVALID: _ClassVar[ErrorCode]
    ERROR_CODE_ACCOUNT_ORDERS_SUSPENDED: _ClassVar[ErrorCode]
    ERROR_CODE_TRAILING_SIDE_NOT_SUPPORTED: _ClassVar[ErrorCode]
    ERROR_CODE_TRAILING_CHILD_NOT_MARKET: _ClassVar[ErrorCode]
    ERROR_CODE_TWAP_DURATION_INVALID: _ClassVar[ErrorCode]
    ERROR_CODE_LIMIT_CHILD_SLIPPAGE_SET: _ClassVar[ErrorCode]
    ERROR_CODE_SLIPPAGE_BOUNDS_CONFLICT: _ClassVar[ErrorCode]
    ERROR_CODE_TWAP_INTERVAL_INVALID: _ClassVar[ErrorCode]
    ERROR_CODE_LADDER_LEVEL_REJECTED: _ClassVar[ErrorCode]
    ERROR_CODE_LADDER_RANGE_TOO_NARROW: _ClassVar[ErrorCode]
    ERROR_CODE_LADDER_LEVELS_INVALID: _ClassVar[ErrorCode]
    ERROR_CODE_ORDER_LIMITS_UNAVAILABLE: _ClassVar[ErrorCode]
    ERROR_CODE_ORDER_TYPE_NOT_ALLOWED_IN_AUCTION: _ClassVar[ErrorCode]
    ERROR_CODE_POST_ONLY_NOT_ALLOWED_IN_AUCTION: _ClassVar[ErrorCode]
    ERROR_CODE_QUICKSWAP_FEE_DETAILS_INCOMPLETE: _ClassVar[ErrorCode]
    ERROR_CODE_QUICKSWAP_MARKET_NOT_PRICED: _ClassVar[ErrorCode]
    ERROR_CODE_QUICKSWAP_BROKER_FEE_TERMS_MISMATCH: _ClassVar[ErrorCode]
    ERROR_CODE_QUICKSWAP_FEE_RECIPIENT_IS_PAYER: _ClassVar[ErrorCode]
    ERROR_CODE_QUICKSWAP_BROKER_FEE_TERMS_UNAVAILABLE: _ClassVar[ErrorCode]
    ERROR_CODE_QUICKSWAP_BROKER_ACCOUNT_UNAVAILABLE: _ClassVar[ErrorCode]
    ERROR_CODE_QUICKSWAP_ACCOUNT_OWNER_UNKNOWN: _ClassVar[ErrorCode]
    ERROR_CODE_QUICKSWAP_DISABLED: _ClassVar[ErrorCode]
    ERROR_CODE_QUICKSWAP_ATTACHED_RISK_NOT_ALLOWED: _ClassVar[ErrorCode]
    ERROR_CODE_QUICKSWAP_ORDER_NOT_MODIFIABLE: _ClassVar[ErrorCode]
    ERROR_CODE_QUICKSWAP_FEE_TOTAL_TOO_HIGH: _ClassVar[ErrorCode]
    ERROR_CODE_QUICKSWAP_BROKER_FEE_TERMS_INVALID: _ClassVar[ErrorCode]
    ERROR_CODE_QUICKSWAP_BROKER_INVALID: _ClassVar[ErrorCode]
    ERROR_CODE_QUICKSWAP_FEE_SCHEDULE_INVALID: _ClassVar[ErrorCode]
    ERROR_CODE_QUICKSWAP_MARKET_FEE_INVALID: _ClassVar[ErrorCode]
    ERROR_CODE_QUICKSWAP_SETUP_INVALID: _ClassVar[ErrorCode]
    ERROR_CODE_QUICKSWAP_CAPACITY_REACHED: _ClassVar[ErrorCode]
    ERROR_CODE_ATTACHED_EXIT_WORKING: _ClassVar[ErrorCode]
    ERROR_CODE_MARKET_TRIGGER_LIMIT_EXCEEDED: _ClassVar[ErrorCode]
    ERROR_CODE_MARKET_TWAP_LIMIT_EXCEEDED: _ClassVar[ErrorCode]
    ERROR_CODE_MARKET_LADDER_LIMIT_EXCEEDED: _ClassVar[ErrorCode]
    ERROR_CODE_CHILD_QTY_EXCEEDS_REMAINING: _ClassVar[ErrorCode]
    ERROR_CODE_ORDER_CANCEL_OUTCOME_UNKNOWN: _ClassVar[ErrorCode]
    ERROR_CODE_ORDER_MODIFY_OUTCOME_UNKNOWN: _ClassVar[ErrorCode]
    ERROR_CODE_ORDER_REPAIRING: _ClassVar[ErrorCode]
    ERROR_CODE_ACCOUNT_REPAIRING: _ClassVar[ErrorCode]
    ERROR_CODE_TRIGGER_WOULD_TRIGGER_IMMEDIATELY: _ClassVar[ErrorCode]
    ERROR_CODE_ORDER_CREATE_OUTCOME_UNKNOWN: _ClassVar[ErrorCode]
    ERROR_CODE_TRIGGER_CREATE_OUTCOME_UNKNOWN: _ClassVar[ErrorCode]
    ERROR_CODE_TRIGGER_SYMBOL_MISMATCH: _ClassVar[ErrorCode]
    ERROR_CODE_MAX_OPEN_ORDERS_PER_PAIR: _ClassVar[ErrorCode]
    ERROR_CODE_ATTACHED_LEGS_EXCEEDED: _ClassVar[ErrorCode]
    ERROR_CODE_FEE_ASSET_INVALID: _ClassVar[ErrorCode]
    ERROR_CODE_FEE_CEILING_INVALID: _ClassVar[ErrorCode]
    ERROR_CODE_UNSUPPORTED_FIELD_SET: _ClassVar[ErrorCode]
    ERROR_CODE_TRIGGER_FIRE_LIMIT_REACHED: _ClassVar[ErrorCode]
    ERROR_CODE_CONDITION_FLAGS_INVALID: _ClassVar[ErrorCode]
    ERROR_CODE_CONDITION_PARAMETER_SET: _ClassVar[ErrorCode]
    ERROR_CODE_TWAP_CAPACITY_REACHED: _ClassVar[ErrorCode]
    ERROR_CODE_CHILD_ORDER_INCONSISTENT: _ClassVar[ErrorCode]

class TriggerPriceSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TRIGGER_PRICE_SOURCE_UNSPECIFIED: _ClassVar[TriggerPriceSource]
    LAST_PRICE: _ClassVar[TriggerPriceSource]
    INDEX_PRICE: _ClassVar[TriggerPriceSource]
    MARK_PRICE: _ClassVar[TriggerPriceSource]

class TriggerDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TRIGGER_DIRECTION_UNSPECIFIED: _ClassVar[TriggerDirection]
    ABOVE: _ClassVar[TriggerDirection]
    BELOW: _ClassVar[TriggerDirection]

class ModifyBehavior(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MODIFY_BEHAVIOR_UNSPECIFIED: _ClassVar[ModifyBehavior]
    AMEND_OR_REPLACE: _ClassVar[ModifyBehavior]
    AMEND_ONLY: _ClassVar[ModifyBehavior]
    REPLACE_ONLY: _ClassVar[ModifyBehavior]

class ModifyActionTaken(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MODIFY_ACTION_UNSPECIFIED: _ClassVar[ModifyActionTaken]
    AMENDED: _ClassVar[ModifyActionTaken]
    REPLACED: _ClassVar[ModifyActionTaken]

class BatchReplaceAdmissionStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BATCH_REPLACE_ADMISSION_STATUS_UNSPECIFIED: _ClassVar[BatchReplaceAdmissionStatus]
    BATCH_REPLACE_ADMISSION_STATUS_ADMITTED: _ClassVar[BatchReplaceAdmissionStatus]
    BATCH_REPLACE_ADMISSION_STATUS_PARTIALLY_ADMITTED: _ClassVar[BatchReplaceAdmissionStatus]
    BATCH_REPLACE_ADMISSION_STATUS_REJECTED: _ClassVar[BatchReplaceAdmissionStatus]

class BatchReplaceItemAdmissionStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BATCH_REPLACE_ITEM_ADMISSION_STATUS_UNSPECIFIED: _ClassVar[BatchReplaceItemAdmissionStatus]
    BATCH_REPLACE_ITEM_ADMISSION_STATUS_ADMITTED: _ClassVar[BatchReplaceItemAdmissionStatus]
    BATCH_REPLACE_ITEM_ADMISSION_STATUS_REJECTED: _ClassVar[BatchReplaceItemAdmissionStatus]
SIDE_UNSPECIFIED: Side
BUY: Side
SELL: Side
ORDER_TYPE_UNSPECIFIED: OrderType
LIMIT: OrderType
MARKET: OrderType
TIME_IN_FORCE_UNSPECIFIED: TimeInForce
GTC: TimeInForce
IOC: TimeInForce
FOK: TimeInForce
GTD: TimeInForce
FEE_ASSET_UNSPECIFIED: FeeAsset
QUOTE: FeeAsset
BASE: FeeAsset
SELF_TRADE_PREVENTION_MODE_UNSPECIFIED: SelfTradePreventionMode
EXPIRE_MAKER: SelfTradePreventionMode
EXPIRE_TAKER: SelfTradePreventionMode
EXPIRE_BOTH: SelfTradePreventionMode
ERROR_CODE_UNSPECIFIED: ErrorCode
ERROR_CODE_BAD_REQUEST: ErrorCode
ERROR_CODE_INVALID_ARGUMENT: ErrorCode
ERROR_CODE_INSUFFICIENT_FUNDS: ErrorCode
ERROR_CODE_UNKNOWN_SYMBOL: ErrorCode
ERROR_CODE_BAD_PRICE: ErrorCode
ERROR_CODE_BAD_QTY: ErrorCode
ERROR_CODE_MIN_NOTIONAL: ErrorCode
ERROR_CODE_QTY_STEP_SIZE: ErrorCode
ERROR_CODE_CONFLICT_DUPLICATE_CLIENT_ORDER_ID: ErrorCode
ERROR_CODE_UNAVAILABLE: ErrorCode
ERROR_CODE_UNAUTHENTICATED: ErrorCode
ERROR_CODE_PERMISSION_DENIED: ErrorCode
ERROR_CODE_NOT_FOUND: ErrorCode
ERROR_CODE_UPSTREAM_ERROR: ErrorCode
ERROR_CODE_FEE_ASSET_NOT_ALLOWED: ErrorCode
ERROR_CODE_PAIR_DISABLED: ErrorCode
ERROR_CODE_ORDER_UNKNOWN: ErrorCode
ERROR_CODE_INTERNAL_ERROR: ErrorCode
ERROR_CODE_SUBACCOUNT_INACTIVE: ErrorCode
ERROR_CODE_POLICY_MARKET_DENY: ErrorCode
ERROR_CODE_POLICY_MAX_NOTIONAL: ErrorCode
ERROR_CODE_POLICY_TRADING_HALTED: ErrorCode
ERROR_CODE_POLICY_SPOT_TRADE_DENY: ErrorCode
ERROR_CODE_API_KEY_ROOT_SCOPE_ONLY: ErrorCode
ERROR_CODE_API_KEY_SUB_SCOPE_ONLY: ErrorCode
ERROR_CODE_API_KEY_SUBACCOUNT_MISMATCH: ErrorCode
ERROR_CODE_API_KEY_POLICY_REQUIRED: ErrorCode
ERROR_CODE_API_KEY_UNKNOWN: ErrorCode
ERROR_CODE_API_KEY_MARKET_DENY: ErrorCode
ERROR_CODE_PRICE_TICK_SIZE: ErrorCode
ERROR_CODE_MIN_QTY: ErrorCode
ERROR_CODE_POST_ONLY_LIMIT_ONLY: ErrorCode
ERROR_CODE_BATCH_TOO_LARGE: ErrorCode
ERROR_CODE_POLICY_MAX_OPEN_ORDERS: ErrorCode
ERROR_CODE_MODIFICATION_REQUIRES_REPLACE: ErrorCode
ERROR_CODE_CONFLICT_IDEMPOTENCY_KEY_REUSE: ErrorCode
ERROR_CODE_MARKET_PRICE_UNAVAILABLE: ErrorCode
ERROR_CODE_PAIR_NOT_LISTED_YET: ErrorCode
ERROR_CODE_PAIR_DELISTED: ErrorCode
ERROR_CODE_PAIR_CANCEL_ONLY: ErrorCode
ERROR_CODE_PAIR_POST_ONLY: ErrorCode
ERROR_CODE_PAIR_REDUCE_ONLY: ErrorCode
ERROR_CODE_RISK_LIMIT: ErrorCode
ERROR_CODE_MARKET_HALTED: ErrorCode
ERROR_CODE_ACCOUNT_UNKNOWN: ErrorCode
ERROR_CODE_POST_ONLY_CROSS: ErrorCode
ERROR_CODE_REDUCE_ONLY_BLOCKED: ErrorCode
ERROR_CODE_PRICE_BAND_VIOLATION: ErrorCode
ERROR_CODE_MARKET_CAP_VIOLATION: ErrorCode
ERROR_CODE_EMPTY_BOOK: ErrorCode
ERROR_CODE_FOK_INSUFFICIENT_LIQUIDITY: ErrorCode
ERROR_CODE_ORDER_ALREADY_TERMINAL: ErrorCode
ERROR_CODE_TRIGGER_PRICE_INVALID: ErrorCode
ERROR_CODE_TRIGGER_PRICE_SOURCE_UNSUPPORTED: ErrorCode
ERROR_CODE_TRAILING_DISTANCE_INVALID: ErrorCode
ERROR_CODE_TRIGGER_NOT_FOUND: ErrorCode
ERROR_CODE_TRIGGER_STATUS_INVALID: ErrorCode
ERROR_CODE_TRIGGER_NOT_MODIFIABLE: ErrorCode
ERROR_CODE_CONFLICT_DUPLICATE_CLIENT_TRIGGER_ID: ErrorCode
ERROR_CODE_MAX_SLIPPAGE_INVALID: ErrorCode
ERROR_CODE_STALE_QUOTE: ErrorCode
ERROR_CODE_VALIDATION_ERROR: ErrorCode
ERROR_CODE_OVERLOADED: ErrorCode
ERROR_CODE_MAX_QUOTE_DEBIT_TOO_SMALL: ErrorCode
ERROR_CODE_RATE_LIMIT_EXCEEDED: ErrorCode
ERROR_CODE_SUBACCOUNT_READ_FORBIDDEN: ErrorCode
ERROR_CODE_POLICY_SPOT_READ_DENY: ErrorCode
ERROR_CODE_API_KEY_SPOT_READ_DENY: ErrorCode
ERROR_CODE_CANCEL_REQUEST_EXPIRED: ErrorCode
ERROR_CODE_MAX_QTY: ErrorCode
ERROR_CODE_MAX_NOTIONAL: ErrorCode
ERROR_CODE_QTY_AT_OR_BELOW_FILLED: ErrorCode
ERROR_CODE_GATEWAY_MISCONFIGURED: ErrorCode
ERROR_CODE_INVALID_ORDER_ID: ErrorCode
ERROR_CODE_CHILD_QTY_RAISE_NOT_ALLOWED: ErrorCode
ERROR_CODE_ATTACHED_RISK_NOT_SUPPORTED: ErrorCode
ERROR_CODE_SETTLEMENT_BACKLOGGED: ErrorCode
ERROR_CODE_PRICE_LEVEL_QUANTITY_LIMIT: ErrorCode
ERROR_CODE_MARKET_QUOTE_STALE: ErrorCode
ERROR_CODE_MARKET_QUOTE_UNHEALTHY: ErrorCode
ERROR_CODE_INVALID_TIME_IN_FORCE: ErrorCode
ERROR_CODE_QUICKSWAP_NOT_PERMITTED: ErrorCode
ERROR_CODE_DUPLICATE_ORDER_ID: ErrorCode
ERROR_CODE_MAX_OPEN_ORDERS_TOTAL: ErrorCode
ERROR_CODE_STP_MODE_NOT_ALLOWED: ErrorCode
ERROR_CODE_PAIR_BACKLOGGED: ErrorCode
ERROR_CODE_PRICE_LEVELS_EXHAUSTED: ErrorCode
ERROR_CODE_CLIENT_ORDER_IDS_EXHAUSTED: ErrorCode
ERROR_CODE_ORDER_ID_CONFLICT: ErrorCode
ERROR_CODE_INVALID_SIDE: ErrorCode
ERROR_CODE_INVALID_ORDER_TYPE: ErrorCode
ERROR_CODE_INVALID_STP_MODE: ErrorCode
ERROR_CODE_INVALID_ORDER_FLAGS: ErrorCode
ERROR_CODE_BATCH_OTHER_ITEM_INVALID: ErrorCode
ERROR_CODE_REPLACE_ONTO_OWN_ID: ErrorCode
ERROR_CODE_INVALID_CLIENT_ORDER_ID: ErrorCode
ERROR_CODE_ORDER_SEQUENCE_EXHAUSTED: ErrorCode
ERROR_CODE_INVALID_HANDLING_MODE: ErrorCode
ERROR_CODE_FEE_SCHEDULE_UNAVAILABLE: ErrorCode
ERROR_CODE_POLICY_UNAVAILABLE: ErrorCode
ERROR_CODE_CANCEL_ALL_AFTER_TIMEOUT_INVALID: ErrorCode
ERROR_CODE_CANCEL_SCOPE_TOO_LARGE: ErrorCode
ERROR_CODE_RATE_LIMIT_POLICY_UNAVAILABLE: ErrorCode
ERROR_CODE_SYSTEM_RATE_LIMITED: ErrorCode
ERROR_CODE_ORDER_MODIFY_IN_PROGRESS: ErrorCode
ERROR_CODE_ORDER_PLACEMENT_PENDING: ErrorCode
ERROR_CODE_INVALID_MODIFY_BEHAVIOR: ErrorCode
ERROR_CODE_BATCH_REPLACE_ONLY_REQUIRED: ErrorCode
ERROR_CODE_BATCH_SINGLE_SYMBOL_REQUIRED: ErrorCode
ERROR_CODE_REQUEST_RECEIPTS_EXHAUSTED: ErrorCode
ERROR_CODE_INTENT_ID_INVALID: ErrorCode
ERROR_CODE_DRY_RUN_INVALID: ErrorCode
ERROR_CODE_CANCEL_ALL_AFTER_SCOPE_CONFLICT: ErrorCode
ERROR_CODE_NEW_ACCOUNT_CAPACITY_REACHED: ErrorCode
ERROR_CODE_TRIGGER_CHILD_PRICE_NOT_MODIFIABLE: ErrorCode
ERROR_CODE_TRIGGER_GENERATIONS_EXHAUSTED: ErrorCode
ERROR_CODE_TRIGGER_CONTROL_SHARE_EXHAUSTED: ErrorCode
ERROR_CODE_TRIGGER_CONTROLS_BUSY: ErrorCode
ERROR_CODE_TRIGGER_TYPE_NOT_SUPPORTED: ErrorCode
ERROR_CODE_INVALID_TRIGGER_TYPE: ErrorCode
ERROR_CODE_TRIGGER_DIRECTION_INVALID: ErrorCode
ERROR_CODE_TRIGGER_QTY_INVALID: ErrorCode
ERROR_CODE_TRIGGER_BUY_REQUIRES_LIMIT: ErrorCode
ERROR_CODE_ACCOUNT_ROUTING_INVALID: ErrorCode
ERROR_CODE_TRIGGER_LIMIT_EXCEEDED: ErrorCode
ERROR_CODE_TRIGGER_CONTROL_IN_PROGRESS: ErrorCode
ERROR_CODE_TRIGGER_PATCH_EMPTY: ErrorCode
ERROR_CODE_CLIENT_TRIGGER_ID_INVALID: ErrorCode
ERROR_CODE_TRIGGER_ACTIVATION_PRICE_INVALID: ErrorCode
ERROR_CODE_SLIPPAGE_TICKS_INVALID: ErrorCode
ERROR_CODE_SLIPPAGE_BPS_INVALID: ErrorCode
ERROR_CODE_TRIGGER_CONTROL_OUTCOME_UNKNOWN: ErrorCode
ERROR_CODE_TRIGGER_CAPACITY_REACHED: ErrorCode
ERROR_CODE_RESERVATION_CAPACITY_REACHED: ErrorCode
ERROR_CODE_CLIENT_ORDER_ID_CAPACITY_REACHED: ErrorCode
ERROR_CODE_ACCOUNT_RESERVATION_LIMIT_REACHED: ErrorCode
ERROR_CODE_INVALID_TRIGGER_CONTROL: ErrorCode
ERROR_CODE_TRIGGER_PATCH_NOT_ALLOWED: ErrorCode
ERROR_CODE_TRIGGER_PATCH_FIELD_UNKNOWN: ErrorCode
ERROR_CODE_TRIGGER_PATCH_VALUE_UNMASKED: ErrorCode
ERROR_CODE_TRIGGER_PATCH_PRICE_MODE_INVALID: ErrorCode
ERROR_CODE_ACCOUNT_ORDERS_SUSPENDED: ErrorCode
ERROR_CODE_TRAILING_SIDE_NOT_SUPPORTED: ErrorCode
ERROR_CODE_TRAILING_CHILD_NOT_MARKET: ErrorCode
ERROR_CODE_TWAP_DURATION_INVALID: ErrorCode
ERROR_CODE_LIMIT_CHILD_SLIPPAGE_SET: ErrorCode
ERROR_CODE_SLIPPAGE_BOUNDS_CONFLICT: ErrorCode
ERROR_CODE_TWAP_INTERVAL_INVALID: ErrorCode
ERROR_CODE_LADDER_LEVEL_REJECTED: ErrorCode
ERROR_CODE_LADDER_RANGE_TOO_NARROW: ErrorCode
ERROR_CODE_LADDER_LEVELS_INVALID: ErrorCode
ERROR_CODE_ORDER_LIMITS_UNAVAILABLE: ErrorCode
ERROR_CODE_ORDER_TYPE_NOT_ALLOWED_IN_AUCTION: ErrorCode
ERROR_CODE_POST_ONLY_NOT_ALLOWED_IN_AUCTION: ErrorCode
ERROR_CODE_QUICKSWAP_FEE_DETAILS_INCOMPLETE: ErrorCode
ERROR_CODE_QUICKSWAP_MARKET_NOT_PRICED: ErrorCode
ERROR_CODE_QUICKSWAP_BROKER_FEE_TERMS_MISMATCH: ErrorCode
ERROR_CODE_QUICKSWAP_FEE_RECIPIENT_IS_PAYER: ErrorCode
ERROR_CODE_QUICKSWAP_BROKER_FEE_TERMS_UNAVAILABLE: ErrorCode
ERROR_CODE_QUICKSWAP_BROKER_ACCOUNT_UNAVAILABLE: ErrorCode
ERROR_CODE_QUICKSWAP_ACCOUNT_OWNER_UNKNOWN: ErrorCode
ERROR_CODE_QUICKSWAP_DISABLED: ErrorCode
ERROR_CODE_QUICKSWAP_ATTACHED_RISK_NOT_ALLOWED: ErrorCode
ERROR_CODE_QUICKSWAP_ORDER_NOT_MODIFIABLE: ErrorCode
ERROR_CODE_QUICKSWAP_FEE_TOTAL_TOO_HIGH: ErrorCode
ERROR_CODE_QUICKSWAP_BROKER_FEE_TERMS_INVALID: ErrorCode
ERROR_CODE_QUICKSWAP_BROKER_INVALID: ErrorCode
ERROR_CODE_QUICKSWAP_FEE_SCHEDULE_INVALID: ErrorCode
ERROR_CODE_QUICKSWAP_MARKET_FEE_INVALID: ErrorCode
ERROR_CODE_QUICKSWAP_SETUP_INVALID: ErrorCode
ERROR_CODE_QUICKSWAP_CAPACITY_REACHED: ErrorCode
ERROR_CODE_ATTACHED_EXIT_WORKING: ErrorCode
ERROR_CODE_MARKET_TRIGGER_LIMIT_EXCEEDED: ErrorCode
ERROR_CODE_MARKET_TWAP_LIMIT_EXCEEDED: ErrorCode
ERROR_CODE_MARKET_LADDER_LIMIT_EXCEEDED: ErrorCode
ERROR_CODE_CHILD_QTY_EXCEEDS_REMAINING: ErrorCode
ERROR_CODE_ORDER_CANCEL_OUTCOME_UNKNOWN: ErrorCode
ERROR_CODE_ORDER_MODIFY_OUTCOME_UNKNOWN: ErrorCode
ERROR_CODE_ORDER_REPAIRING: ErrorCode
ERROR_CODE_ACCOUNT_REPAIRING: ErrorCode
ERROR_CODE_TRIGGER_WOULD_TRIGGER_IMMEDIATELY: ErrorCode
ERROR_CODE_ORDER_CREATE_OUTCOME_UNKNOWN: ErrorCode
ERROR_CODE_TRIGGER_CREATE_OUTCOME_UNKNOWN: ErrorCode
ERROR_CODE_TRIGGER_SYMBOL_MISMATCH: ErrorCode
ERROR_CODE_MAX_OPEN_ORDERS_PER_PAIR: ErrorCode
ERROR_CODE_ATTACHED_LEGS_EXCEEDED: ErrorCode
ERROR_CODE_FEE_ASSET_INVALID: ErrorCode
ERROR_CODE_FEE_CEILING_INVALID: ErrorCode
ERROR_CODE_UNSUPPORTED_FIELD_SET: ErrorCode
ERROR_CODE_TRIGGER_FIRE_LIMIT_REACHED: ErrorCode
ERROR_CODE_CONDITION_FLAGS_INVALID: ErrorCode
ERROR_CODE_CONDITION_PARAMETER_SET: ErrorCode
ERROR_CODE_TWAP_CAPACITY_REACHED: ErrorCode
ERROR_CODE_CHILD_ORDER_INCONSISTENT: ErrorCode
TRIGGER_PRICE_SOURCE_UNSPECIFIED: TriggerPriceSource
LAST_PRICE: TriggerPriceSource
INDEX_PRICE: TriggerPriceSource
MARK_PRICE: TriggerPriceSource
TRIGGER_DIRECTION_UNSPECIFIED: TriggerDirection
ABOVE: TriggerDirection
BELOW: TriggerDirection
MODIFY_BEHAVIOR_UNSPECIFIED: ModifyBehavior
AMEND_OR_REPLACE: ModifyBehavior
AMEND_ONLY: ModifyBehavior
REPLACE_ONLY: ModifyBehavior
MODIFY_ACTION_UNSPECIFIED: ModifyActionTaken
AMENDED: ModifyActionTaken
REPLACED: ModifyActionTaken
BATCH_REPLACE_ADMISSION_STATUS_UNSPECIFIED: BatchReplaceAdmissionStatus
BATCH_REPLACE_ADMISSION_STATUS_ADMITTED: BatchReplaceAdmissionStatus
BATCH_REPLACE_ADMISSION_STATUS_PARTIALLY_ADMITTED: BatchReplaceAdmissionStatus
BATCH_REPLACE_ADMISSION_STATUS_REJECTED: BatchReplaceAdmissionStatus
BATCH_REPLACE_ITEM_ADMISSION_STATUS_UNSPECIFIED: BatchReplaceItemAdmissionStatus
BATCH_REPLACE_ITEM_ADMISSION_STATUS_ADMITTED: BatchReplaceItemAdmissionStatus
BATCH_REPLACE_ITEM_ADMISSION_STATUS_REJECTED: BatchReplaceItemAdmissionStatus

class MarketIoc(_message.Message):
    __slots__ = ("max_slippage_ticks", "max_slippage_bps", "client_ref_price_ticks")
    MAX_SLIPPAGE_TICKS_FIELD_NUMBER: _ClassVar[int]
    MAX_SLIPPAGE_BPS_FIELD_NUMBER: _ClassVar[int]
    CLIENT_REF_PRICE_TICKS_FIELD_NUMBER: _ClassVar[int]
    max_slippage_ticks: int
    max_slippage_bps: int
    client_ref_price_ticks: int
    def __init__(self, max_slippage_ticks: _Optional[int] = ..., max_slippage_bps: _Optional[int] = ..., client_ref_price_ticks: _Optional[int] = ...) -> None: ...

class LimitGtc(_message.Message):
    __slots__ = ("price_ticks", "post_only")
    PRICE_TICKS_FIELD_NUMBER: _ClassVar[int]
    POST_ONLY_FIELD_NUMBER: _ClassVar[int]
    price_ticks: int
    post_only: bool
    def __init__(self, price_ticks: _Optional[int] = ..., post_only: _Optional[bool] = ...) -> None: ...

class LimitGtd(_message.Message):
    __slots__ = ("price_ticks", "post_only", "expire_at")
    PRICE_TICKS_FIELD_NUMBER: _ClassVar[int]
    POST_ONLY_FIELD_NUMBER: _ClassVar[int]
    EXPIRE_AT_FIELD_NUMBER: _ClassVar[int]
    price_ticks: int
    post_only: bool
    expire_at: _timestamp_pb2.Timestamp
    def __init__(self, price_ticks: _Optional[int] = ..., post_only: _Optional[bool] = ..., expire_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class LimitIoc(_message.Message):
    __slots__ = ("price_ticks",)
    PRICE_TICKS_FIELD_NUMBER: _ClassVar[int]
    price_ticks: int
    def __init__(self, price_ticks: _Optional[int] = ...) -> None: ...

class LimitFok(_message.Message):
    __slots__ = ("price_ticks",)
    PRICE_TICKS_FIELD_NUMBER: _ClassVar[int]
    price_ticks: int
    def __init__(self, price_ticks: _Optional[int] = ...) -> None: ...

class OrderIntent(_message.Message):
    __slots__ = ("symbol_id", "side", "base_qty_scaled", "max_quote_debit_scaled", "market_ioc", "limit_gtc", "limit_ioc", "limit_fok", "limit_gtd", "client_order_id", "fee_asset", "self_trade_prevention_mode", "attached_risk")
    SYMBOL_ID_FIELD_NUMBER: _ClassVar[int]
    SIDE_FIELD_NUMBER: _ClassVar[int]
    BASE_QTY_SCALED_FIELD_NUMBER: _ClassVar[int]
    MAX_QUOTE_DEBIT_SCALED_FIELD_NUMBER: _ClassVar[int]
    MARKET_IOC_FIELD_NUMBER: _ClassVar[int]
    LIMIT_GTC_FIELD_NUMBER: _ClassVar[int]
    LIMIT_IOC_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FOK_FIELD_NUMBER: _ClassVar[int]
    LIMIT_GTD_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    FEE_ASSET_FIELD_NUMBER: _ClassVar[int]
    SELF_TRADE_PREVENTION_MODE_FIELD_NUMBER: _ClassVar[int]
    ATTACHED_RISK_FIELD_NUMBER: _ClassVar[int]
    symbol_id: int
    side: Side
    base_qty_scaled: int
    max_quote_debit_scaled: int
    market_ioc: MarketIoc
    limit_gtc: LimitGtc
    limit_ioc: LimitIoc
    limit_fok: LimitFok
    limit_gtd: LimitGtd
    client_order_id: str
    fee_asset: FeeAsset
    self_trade_prevention_mode: SelfTradePreventionMode
    attached_risk: RiskPolicy
    def __init__(self, symbol_id: _Optional[int] = ..., side: _Optional[_Union[Side, str]] = ..., base_qty_scaled: _Optional[int] = ..., max_quote_debit_scaled: _Optional[int] = ..., market_ioc: _Optional[_Union[MarketIoc, _Mapping]] = ..., limit_gtc: _Optional[_Union[LimitGtc, _Mapping]] = ..., limit_ioc: _Optional[_Union[LimitIoc, _Mapping]] = ..., limit_fok: _Optional[_Union[LimitFok, _Mapping]] = ..., limit_gtd: _Optional[_Union[LimitGtd, _Mapping]] = ..., client_order_id: _Optional[str] = ..., fee_asset: _Optional[_Union[FeeAsset, str]] = ..., self_trade_prevention_mode: _Optional[_Union[SelfTradePreventionMode, str]] = ..., attached_risk: _Optional[_Union[RiskPolicy, _Mapping]] = ...) -> None: ...

class CreateOrderRequest(_message.Message):
    __slots__ = ("subaccount_id", "order")
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    order: OrderIntent
    def __init__(self, subaccount_id: _Optional[int] = ..., order: _Optional[_Union[OrderIntent, _Mapping]] = ...) -> None: ...

class CreateOrderResponse(_message.Message):
    __slots__ = ("order_id", "client_order_id", "accepted_at", "accepted_at_ts_ns", "resolved_base_qty_scaled", "submitted_max_quote_debit_scaled", "take_profit_trigger_id", "stop_loss_trigger_id", "trailing_stop_trigger_id")
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    ACCEPTED_AT_FIELD_NUMBER: _ClassVar[int]
    ACCEPTED_AT_TS_NS_FIELD_NUMBER: _ClassVar[int]
    RESOLVED_BASE_QTY_SCALED_FIELD_NUMBER: _ClassVar[int]
    SUBMITTED_MAX_QUOTE_DEBIT_SCALED_FIELD_NUMBER: _ClassVar[int]
    TAKE_PROFIT_TRIGGER_ID_FIELD_NUMBER: _ClassVar[int]
    STOP_LOSS_TRIGGER_ID_FIELD_NUMBER: _ClassVar[int]
    TRAILING_STOP_TRIGGER_ID_FIELD_NUMBER: _ClassVar[int]
    order_id: int
    client_order_id: str
    accepted_at: _timestamp_pb2.Timestamp
    accepted_at_ts_ns: int
    resolved_base_qty_scaled: int
    submitted_max_quote_debit_scaled: int
    take_profit_trigger_id: int
    stop_loss_trigger_id: int
    trailing_stop_trigger_id: int
    def __init__(self, order_id: _Optional[int] = ..., client_order_id: _Optional[str] = ..., accepted_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., accepted_at_ts_ns: _Optional[int] = ..., resolved_base_qty_scaled: _Optional[int] = ..., submitted_max_quote_debit_scaled: _Optional[int] = ..., take_profit_trigger_id: _Optional[int] = ..., stop_loss_trigger_id: _Optional[int] = ..., trailing_stop_trigger_id: _Optional[int] = ...) -> None: ...

class PreviewOrderRequest(_message.Message):
    __slots__ = ("subaccount_id", "order")
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    order: OrderIntent
    def __init__(self, subaccount_id: _Optional[int] = ..., order: _Optional[_Union[OrderIntent, _Mapping]] = ...) -> None: ...

class PreviewOrderResponse(_message.Message):
    __slots__ = ("admissible", "rejection", "resolved_base_qty_scaled", "protected_price_bound_ticks", "evaluated_at")
    ADMISSIBLE_FIELD_NUMBER: _ClassVar[int]
    REJECTION_FIELD_NUMBER: _ClassVar[int]
    RESOLVED_BASE_QTY_SCALED_FIELD_NUMBER: _ClassVar[int]
    PROTECTED_PRICE_BOUND_TICKS_FIELD_NUMBER: _ClassVar[int]
    EVALUATED_AT_FIELD_NUMBER: _ClassVar[int]
    admissible: bool
    rejection: ErrorDetail
    resolved_base_qty_scaled: int
    protected_price_bound_ticks: int
    evaluated_at: _timestamp_pb2.Timestamp
    def __init__(self, admissible: _Optional[bool] = ..., rejection: _Optional[_Union[ErrorDetail, _Mapping]] = ..., resolved_base_qty_scaled: _Optional[int] = ..., protected_price_bound_ticks: _Optional[int] = ..., evaluated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class CancelOrderRequest(_message.Message):
    __slots__ = ("order_id", "client_order_id", "symbol_id", "subaccount_id")
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_ID_FIELD_NUMBER: _ClassVar[int]
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    order_id: int
    client_order_id: str
    symbol_id: int
    subaccount_id: int
    def __init__(self, order_id: _Optional[int] = ..., client_order_id: _Optional[str] = ..., symbol_id: _Optional[int] = ..., subaccount_id: _Optional[int] = ...) -> None: ...

class CancelOrderResponse(_message.Message):
    __slots__ = ("status", "order_id", "ts", "ts_ns")
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        STATUS_UNSPECIFIED: _ClassVar[CancelOrderResponse.Status]
        ACCEPTED: _ClassVar[CancelOrderResponse.Status]
    STATUS_UNSPECIFIED: CancelOrderResponse.Status
    ACCEPTED: CancelOrderResponse.Status
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    TS_FIELD_NUMBER: _ClassVar[int]
    TS_NS_FIELD_NUMBER: _ClassVar[int]
    status: CancelOrderResponse.Status
    order_id: int
    ts: _timestamp_pb2.Timestamp
    ts_ns: int
    def __init__(self, status: _Optional[_Union[CancelOrderResponse.Status, str]] = ..., order_id: _Optional[int] = ..., ts: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., ts_ns: _Optional[int] = ...) -> None: ...

class FieldViolation(_message.Message):
    __slots__ = ("field_path", "rule_id", "message")
    FIELD_PATH_FIELD_NUMBER: _ClassVar[int]
    RULE_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    field_path: str
    rule_id: str
    message: str
    def __init__(self, field_path: _Optional[str] = ..., rule_id: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class ErrorDetail(_message.Message):
    __slots__ = ("code", "violations", "rate_limit", "existing_order_id")
    CODE_FIELD_NUMBER: _ClassVar[int]
    VIOLATIONS_FIELD_NUMBER: _ClassVar[int]
    RATE_LIMIT_FIELD_NUMBER: _ClassVar[int]
    EXISTING_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    code: ErrorCode
    violations: _containers.RepeatedCompositeFieldContainer[FieldViolation]
    rate_limit: _types_pb2.RateLimitDetail
    existing_order_id: int
    def __init__(self, code: _Optional[_Union[ErrorCode, str]] = ..., violations: _Optional[_Iterable[_Union[FieldViolation, _Mapping]]] = ..., rate_limit: _Optional[_Union[_types_pb2.RateLimitDetail, _Mapping]] = ..., existing_order_id: _Optional[int] = ...) -> None: ...

class RiskMarketIoc(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class RiskLimitGtc(_message.Message):
    __slots__ = ("price_ticks",)
    PRICE_TICKS_FIELD_NUMBER: _ClassVar[int]
    price_ticks: int
    def __init__(self, price_ticks: _Optional[int] = ...) -> None: ...

class RiskExecution(_message.Message):
    __slots__ = ("market_ioc", "limit_gtc")
    MARKET_IOC_FIELD_NUMBER: _ClassVar[int]
    LIMIT_GTC_FIELD_NUMBER: _ClassVar[int]
    market_ioc: RiskMarketIoc
    limit_gtc: RiskLimitGtc
    def __init__(self, market_ioc: _Optional[_Union[RiskMarketIoc, _Mapping]] = ..., limit_gtc: _Optional[_Union[RiskLimitGtc, _Mapping]] = ...) -> None: ...

class TakeProfitPolicy(_message.Message):
    __slots__ = ("trigger_price_ticks", "child", "trigger_price_source")
    TRIGGER_PRICE_TICKS_FIELD_NUMBER: _ClassVar[int]
    CHILD_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_PRICE_SOURCE_FIELD_NUMBER: _ClassVar[int]
    trigger_price_ticks: int
    child: RiskExecution
    trigger_price_source: TriggerPriceSource
    def __init__(self, trigger_price_ticks: _Optional[int] = ..., child: _Optional[_Union[RiskExecution, _Mapping]] = ..., trigger_price_source: _Optional[_Union[TriggerPriceSource, str]] = ...) -> None: ...

class StopLossPolicy(_message.Message):
    __slots__ = ("trigger_price_ticks", "child", "trigger_price_source")
    TRIGGER_PRICE_TICKS_FIELD_NUMBER: _ClassVar[int]
    CHILD_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_PRICE_SOURCE_FIELD_NUMBER: _ClassVar[int]
    trigger_price_ticks: int
    child: RiskExecution
    trigger_price_source: TriggerPriceSource
    def __init__(self, trigger_price_ticks: _Optional[int] = ..., child: _Optional[_Union[RiskExecution, _Mapping]] = ..., trigger_price_source: _Optional[_Union[TriggerPriceSource, str]] = ...) -> None: ...

class TrailingStopPolicy(_message.Message):
    __slots__ = ("trailing_distance_ticks", "trailing_distance_bps", "max_slippage_ticks", "max_slippage_bps", "activation_price_ticks", "trigger_price_source", "limit_price_ticks")
    TRAILING_DISTANCE_TICKS_FIELD_NUMBER: _ClassVar[int]
    TRAILING_DISTANCE_BPS_FIELD_NUMBER: _ClassVar[int]
    MAX_SLIPPAGE_TICKS_FIELD_NUMBER: _ClassVar[int]
    MAX_SLIPPAGE_BPS_FIELD_NUMBER: _ClassVar[int]
    ACTIVATION_PRICE_TICKS_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_PRICE_SOURCE_FIELD_NUMBER: _ClassVar[int]
    LIMIT_PRICE_TICKS_FIELD_NUMBER: _ClassVar[int]
    trailing_distance_ticks: int
    trailing_distance_bps: int
    max_slippage_ticks: int
    max_slippage_bps: int
    activation_price_ticks: int
    trigger_price_source: TriggerPriceSource
    limit_price_ticks: int
    def __init__(self, trailing_distance_ticks: _Optional[int] = ..., trailing_distance_bps: _Optional[int] = ..., max_slippage_ticks: _Optional[int] = ..., max_slippage_bps: _Optional[int] = ..., activation_price_ticks: _Optional[int] = ..., trigger_price_source: _Optional[_Union[TriggerPriceSource, str]] = ..., limit_price_ticks: _Optional[int] = ...) -> None: ...

class RiskPolicy(_message.Message):
    __slots__ = ("take_profit", "stop_loss", "trailing_stop", "oco")
    TAKE_PROFIT_FIELD_NUMBER: _ClassVar[int]
    STOP_LOSS_FIELD_NUMBER: _ClassVar[int]
    TRAILING_STOP_FIELD_NUMBER: _ClassVar[int]
    OCO_FIELD_NUMBER: _ClassVar[int]
    take_profit: TakeProfitPolicy
    stop_loss: StopLossPolicy
    trailing_stop: TrailingStopPolicy
    oco: bool
    def __init__(self, take_profit: _Optional[_Union[TakeProfitPolicy, _Mapping]] = ..., stop_loss: _Optional[_Union[StopLossPolicy, _Mapping]] = ..., trailing_stop: _Optional[_Union[TrailingStopPolicy, _Mapping]] = ..., oco: _Optional[bool] = ...) -> None: ...

class CancelAllOrdersRequest(_message.Message):
    __slots__ = ("subaccount_id", "symbol_ids", "side", "dry_run", "request_id")
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_IDS_FIELD_NUMBER: _ClassVar[int]
    SIDE_FIELD_NUMBER: _ClassVar[int]
    DRY_RUN_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    symbol_ids: _containers.RepeatedScalarFieldContainer[int]
    side: Side
    dry_run: bool
    request_id: str
    def __init__(self, subaccount_id: _Optional[int] = ..., symbol_ids: _Optional[_Iterable[int]] = ..., side: _Optional[_Union[Side, str]] = ..., dry_run: _Optional[bool] = ..., request_id: _Optional[str] = ...) -> None: ...

class CancelledOrder(_message.Message):
    __slots__ = ("order_id", "client_order_id")
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    order_id: int
    client_order_id: str
    def __init__(self, order_id: _Optional[int] = ..., client_order_id: _Optional[str] = ...) -> None: ...

class CancelAllOrdersResponse(_message.Message):
    __slots__ = ("status", "matched_orders", "submitted_cancels", "failed_cancels", "ts", "ts_ns", "cancelled_orders", "total_cancelled", "truncated", "listing_status")
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        STATUS_UNSPECIFIED: _ClassVar[CancelAllOrdersResponse.Status]
        SUBMITTED: _ClassVar[CancelAllOrdersResponse.Status]
        DRY_RUN: _ClassVar[CancelAllOrdersResponse.Status]
    STATUS_UNSPECIFIED: CancelAllOrdersResponse.Status
    SUBMITTED: CancelAllOrdersResponse.Status
    DRY_RUN: CancelAllOrdersResponse.Status
    class ListingStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        LISTING_UNSPECIFIED: _ClassVar[CancelAllOrdersResponse.ListingStatus]
        INCLUDED: _ClassVar[CancelAllOrdersResponse.ListingStatus]
        NOT_RETAINED_READ_OPEN_ORDERS: _ClassVar[CancelAllOrdersResponse.ListingStatus]
    LISTING_UNSPECIFIED: CancelAllOrdersResponse.ListingStatus
    INCLUDED: CancelAllOrdersResponse.ListingStatus
    NOT_RETAINED_READ_OPEN_ORDERS: CancelAllOrdersResponse.ListingStatus
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MATCHED_ORDERS_FIELD_NUMBER: _ClassVar[int]
    SUBMITTED_CANCELS_FIELD_NUMBER: _ClassVar[int]
    FAILED_CANCELS_FIELD_NUMBER: _ClassVar[int]
    TS_FIELD_NUMBER: _ClassVar[int]
    TS_NS_FIELD_NUMBER: _ClassVar[int]
    CANCELLED_ORDERS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_CANCELLED_FIELD_NUMBER: _ClassVar[int]
    TRUNCATED_FIELD_NUMBER: _ClassVar[int]
    LISTING_STATUS_FIELD_NUMBER: _ClassVar[int]
    status: CancelAllOrdersResponse.Status
    matched_orders: int
    submitted_cancels: int
    failed_cancels: int
    ts: _timestamp_pb2.Timestamp
    ts_ns: int
    cancelled_orders: _containers.RepeatedCompositeFieldContainer[CancelledOrder]
    total_cancelled: int
    truncated: bool
    listing_status: CancelAllOrdersResponse.ListingStatus
    def __init__(self, status: _Optional[_Union[CancelAllOrdersResponse.Status, str]] = ..., matched_orders: _Optional[int] = ..., submitted_cancels: _Optional[int] = ..., failed_cancels: _Optional[int] = ..., ts: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., ts_ns: _Optional[int] = ..., cancelled_orders: _Optional[_Iterable[_Union[CancelledOrder, _Mapping]]] = ..., total_cancelled: _Optional[int] = ..., truncated: _Optional[bool] = ..., listing_status: _Optional[_Union[CancelAllOrdersResponse.ListingStatus, str]] = ...) -> None: ...

class CancelAllAfterRequest(_message.Message):
    __slots__ = ("subaccount_id", "timeout_sec", "symbol_id", "side", "request_id")
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_SEC_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_ID_FIELD_NUMBER: _ClassVar[int]
    SIDE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    timeout_sec: int
    symbol_id: int
    side: Side
    request_id: str
    def __init__(self, subaccount_id: _Optional[int] = ..., timeout_sec: _Optional[int] = ..., symbol_id: _Optional[int] = ..., side: _Optional[_Union[Side, str]] = ..., request_id: _Optional[str] = ...) -> None: ...

class DeadManSwitchScope(_message.Message):
    __slots__ = ("account_id", "symbol_id", "side")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_ID_FIELD_NUMBER: _ClassVar[int]
    SIDE_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    symbol_id: int
    side: Side
    def __init__(self, account_id: _Optional[int] = ..., symbol_id: _Optional[int] = ..., side: _Optional[_Union[Side, str]] = ...) -> None: ...

class CancelAllAfterResponse(_message.Message):
    __slots__ = ("status", "effective_timeout_sec", "expires_at_ts_ns", "ts", "ts_ns", "effective_scope")
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        STATUS_UNSPECIFIED: _ClassVar[CancelAllAfterResponse.Status]
        ARMED: _ClassVar[CancelAllAfterResponse.Status]
        DISABLED: _ClassVar[CancelAllAfterResponse.Status]
    STATUS_UNSPECIFIED: CancelAllAfterResponse.Status
    ARMED: CancelAllAfterResponse.Status
    DISABLED: CancelAllAfterResponse.Status
    STATUS_FIELD_NUMBER: _ClassVar[int]
    EFFECTIVE_TIMEOUT_SEC_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_TS_NS_FIELD_NUMBER: _ClassVar[int]
    TS_FIELD_NUMBER: _ClassVar[int]
    TS_NS_FIELD_NUMBER: _ClassVar[int]
    EFFECTIVE_SCOPE_FIELD_NUMBER: _ClassVar[int]
    status: CancelAllAfterResponse.Status
    effective_timeout_sec: int
    expires_at_ts_ns: int
    ts: _timestamp_pb2.Timestamp
    ts_ns: int
    effective_scope: DeadManSwitchScope
    def __init__(self, status: _Optional[_Union[CancelAllAfterResponse.Status, str]] = ..., effective_timeout_sec: _Optional[int] = ..., expires_at_ts_ns: _Optional[int] = ..., ts: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., ts_ns: _Optional[int] = ..., effective_scope: _Optional[_Union[DeadManSwitchScope, _Mapping]] = ...) -> None: ...

class BatchCreateAccepted(_message.Message):
    __slots__ = ("order_id", "take_profit_trigger_id", "stop_loss_trigger_id", "trailing_stop_trigger_id", "resolved_base_qty_scaled", "submitted_max_quote_debit_scaled")
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    TAKE_PROFIT_TRIGGER_ID_FIELD_NUMBER: _ClassVar[int]
    STOP_LOSS_TRIGGER_ID_FIELD_NUMBER: _ClassVar[int]
    TRAILING_STOP_TRIGGER_ID_FIELD_NUMBER: _ClassVar[int]
    RESOLVED_BASE_QTY_SCALED_FIELD_NUMBER: _ClassVar[int]
    SUBMITTED_MAX_QUOTE_DEBIT_SCALED_FIELD_NUMBER: _ClassVar[int]
    order_id: int
    take_profit_trigger_id: int
    stop_loss_trigger_id: int
    trailing_stop_trigger_id: int
    resolved_base_qty_scaled: int
    submitted_max_quote_debit_scaled: int
    def __init__(self, order_id: _Optional[int] = ..., take_profit_trigger_id: _Optional[int] = ..., stop_loss_trigger_id: _Optional[int] = ..., trailing_stop_trigger_id: _Optional[int] = ..., resolved_base_qty_scaled: _Optional[int] = ..., submitted_max_quote_debit_scaled: _Optional[int] = ...) -> None: ...

class BatchCreateRejected(_message.Message):
    __slots__ = ("error",)
    ERROR_FIELD_NUMBER: _ClassVar[int]
    error: ErrorDetail
    def __init__(self, error: _Optional[_Union[ErrorDetail, _Mapping]] = ...) -> None: ...

class BatchCreateResultItem(_message.Message):
    __slots__ = ("client_order_id", "accepted", "rejected")
    CLIENT_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    ACCEPTED_FIELD_NUMBER: _ClassVar[int]
    REJECTED_FIELD_NUMBER: _ClassVar[int]
    client_order_id: str
    accepted: BatchCreateAccepted
    rejected: BatchCreateRejected
    def __init__(self, client_order_id: _Optional[str] = ..., accepted: _Optional[_Union[BatchCreateAccepted, _Mapping]] = ..., rejected: _Optional[_Union[BatchCreateRejected, _Mapping]] = ...) -> None: ...

class BatchCreateOrdersRequest(_message.Message):
    __slots__ = ("subaccount_id", "request_id", "items")
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    request_id: str
    items: _containers.RepeatedCompositeFieldContainer[OrderIntent]
    def __init__(self, subaccount_id: _Optional[int] = ..., request_id: _Optional[str] = ..., items: _Optional[_Iterable[_Union[OrderIntent, _Mapping]]] = ...) -> None: ...

class BatchCreateOrdersResponse(_message.Message):
    __slots__ = ("results", "accepted_count", "rejected_count", "ts", "ts_ns")
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    ACCEPTED_COUNT_FIELD_NUMBER: _ClassVar[int]
    REJECTED_COUNT_FIELD_NUMBER: _ClassVar[int]
    TS_FIELD_NUMBER: _ClassVar[int]
    TS_NS_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[BatchCreateResultItem]
    accepted_count: int
    rejected_count: int
    ts: _timestamp_pb2.Timestamp
    ts_ns: int
    def __init__(self, results: _Optional[_Iterable[_Union[BatchCreateResultItem, _Mapping]]] = ..., accepted_count: _Optional[int] = ..., rejected_count: _Optional[int] = ..., ts: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., ts_ns: _Optional[int] = ...) -> None: ...

class ModifyOrderRequest(_message.Message):
    __slots__ = ("subaccount_id", "order_id", "client_order_id", "request_id", "new_price_ticks", "new_qty_scaled", "new_attached_risk", "behavior", "new_client_order_id", "symbol_id")
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    NEW_PRICE_TICKS_FIELD_NUMBER: _ClassVar[int]
    NEW_QTY_SCALED_FIELD_NUMBER: _ClassVar[int]
    NEW_ATTACHED_RISK_FIELD_NUMBER: _ClassVar[int]
    BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    NEW_CLIENT_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_ID_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    order_id: int
    client_order_id: str
    request_id: str
    new_price_ticks: int
    new_qty_scaled: int
    new_attached_risk: RiskPolicy
    behavior: ModifyBehavior
    new_client_order_id: str
    symbol_id: int
    def __init__(self, subaccount_id: _Optional[int] = ..., order_id: _Optional[int] = ..., client_order_id: _Optional[str] = ..., request_id: _Optional[str] = ..., new_price_ticks: _Optional[int] = ..., new_qty_scaled: _Optional[int] = ..., new_attached_risk: _Optional[_Union[RiskPolicy, _Mapping]] = ..., behavior: _Optional[_Union[ModifyBehavior, str]] = ..., new_client_order_id: _Optional[str] = ..., symbol_id: _Optional[int] = ...) -> None: ...

class ModifyOrderResponse(_message.Message):
    __slots__ = ("action_taken", "old_order_id", "final_order_id", "code", "take_profit_trigger_id", "stop_loss_trigger_id", "trailing_stop_trigger_id", "ts", "ts_ns")
    ACTION_TAKEN_FIELD_NUMBER: _ClassVar[int]
    OLD_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    FINAL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    TAKE_PROFIT_TRIGGER_ID_FIELD_NUMBER: _ClassVar[int]
    STOP_LOSS_TRIGGER_ID_FIELD_NUMBER: _ClassVar[int]
    TRAILING_STOP_TRIGGER_ID_FIELD_NUMBER: _ClassVar[int]
    TS_FIELD_NUMBER: _ClassVar[int]
    TS_NS_FIELD_NUMBER: _ClassVar[int]
    action_taken: ModifyActionTaken
    old_order_id: int
    final_order_id: int
    code: str
    take_profit_trigger_id: int
    stop_loss_trigger_id: int
    trailing_stop_trigger_id: int
    ts: _timestamp_pb2.Timestamp
    ts_ns: int
    def __init__(self, action_taken: _Optional[_Union[ModifyActionTaken, str]] = ..., old_order_id: _Optional[int] = ..., final_order_id: _Optional[int] = ..., code: _Optional[str] = ..., take_profit_trigger_id: _Optional[int] = ..., stop_loss_trigger_id: _Optional[int] = ..., trailing_stop_trigger_id: _Optional[int] = ..., ts: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., ts_ns: _Optional[int] = ...) -> None: ...

class BatchReplaceOrderItem(_message.Message):
    __slots__ = ("order_id", "client_order_id", "new_price_ticks", "new_qty_scaled", "new_attached_risk", "new_client_order_id")
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    NEW_PRICE_TICKS_FIELD_NUMBER: _ClassVar[int]
    NEW_QTY_SCALED_FIELD_NUMBER: _ClassVar[int]
    NEW_ATTACHED_RISK_FIELD_NUMBER: _ClassVar[int]
    NEW_CLIENT_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    order_id: int
    client_order_id: str
    new_price_ticks: int
    new_qty_scaled: int
    new_attached_risk: RiskPolicy
    new_client_order_id: str
    def __init__(self, order_id: _Optional[int] = ..., client_order_id: _Optional[str] = ..., new_price_ticks: _Optional[int] = ..., new_qty_scaled: _Optional[int] = ..., new_attached_risk: _Optional[_Union[RiskPolicy, _Mapping]] = ..., new_client_order_id: _Optional[str] = ...) -> None: ...

class BatchReplaceAdmissionItem(_message.Message):
    __slots__ = ("item_index", "status", "old_order_id", "replacement_order_id", "client_order_id", "code", "error", "action_taken")
    ITEM_INDEX_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    OLD_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    REPLACEMENT_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ACTION_TAKEN_FIELD_NUMBER: _ClassVar[int]
    item_index: int
    status: BatchReplaceItemAdmissionStatus
    old_order_id: int
    replacement_order_id: int
    client_order_id: str
    code: str
    error: ErrorDetail
    action_taken: ModifyActionTaken
    def __init__(self, item_index: _Optional[int] = ..., status: _Optional[_Union[BatchReplaceItemAdmissionStatus, str]] = ..., old_order_id: _Optional[int] = ..., replacement_order_id: _Optional[int] = ..., client_order_id: _Optional[str] = ..., code: _Optional[str] = ..., error: _Optional[_Union[ErrorDetail, _Mapping]] = ..., action_taken: _Optional[_Union[ModifyActionTaken, str]] = ...) -> None: ...

class BatchReplaceOrdersRequest(_message.Message):
    __slots__ = ("subaccount_id", "symbol_id", "request_id", "items")
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    symbol_id: int
    request_id: str
    items: _containers.RepeatedCompositeFieldContainer[BatchReplaceOrderItem]
    def __init__(self, subaccount_id: _Optional[int] = ..., symbol_id: _Optional[int] = ..., request_id: _Optional[str] = ..., items: _Optional[_Iterable[_Union[BatchReplaceOrderItem, _Mapping]]] = ...) -> None: ...

class BatchReplaceOrdersResponse(_message.Message):
    __slots__ = ("batch_request_id", "status", "results", "accepted_count", "rejected_count", "accepted_ts", "accepted_ts_ns")
    BATCH_REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    ACCEPTED_COUNT_FIELD_NUMBER: _ClassVar[int]
    REJECTED_COUNT_FIELD_NUMBER: _ClassVar[int]
    ACCEPTED_TS_FIELD_NUMBER: _ClassVar[int]
    ACCEPTED_TS_NS_FIELD_NUMBER: _ClassVar[int]
    batch_request_id: int
    status: BatchReplaceAdmissionStatus
    results: _containers.RepeatedCompositeFieldContainer[BatchReplaceAdmissionItem]
    accepted_count: int
    rejected_count: int
    accepted_ts: _timestamp_pb2.Timestamp
    accepted_ts_ns: int
    def __init__(self, batch_request_id: _Optional[int] = ..., status: _Optional[_Union[BatchReplaceAdmissionStatus, str]] = ..., results: _Optional[_Iterable[_Union[BatchReplaceAdmissionItem, _Mapping]]] = ..., accepted_count: _Optional[int] = ..., rejected_count: _Optional[int] = ..., accepted_ts: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., accepted_ts_ns: _Optional[int] = ...) -> None: ...

class BatchCancelItem(_message.Message):
    __slots__ = ("order_id", "client_order_id", "symbol_id")
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_ID_FIELD_NUMBER: _ClassVar[int]
    order_id: int
    client_order_id: str
    symbol_id: int
    def __init__(self, order_id: _Optional[int] = ..., client_order_id: _Optional[str] = ..., symbol_id: _Optional[int] = ...) -> None: ...

class BatchCancelResultItem(_message.Message):
    __slots__ = ("status", "order_id", "client_order_id", "code", "error")
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        STATUS_UNSPECIFIED: _ClassVar[BatchCancelResultItem.Status]
        ACCEPTED: _ClassVar[BatchCancelResultItem.Status]
        REJECTED: _ClassVar[BatchCancelResultItem.Status]
    STATUS_UNSPECIFIED: BatchCancelResultItem.Status
    ACCEPTED: BatchCancelResultItem.Status
    REJECTED: BatchCancelResultItem.Status
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    status: BatchCancelResultItem.Status
    order_id: int
    client_order_id: str
    code: str
    error: ErrorDetail
    def __init__(self, status: _Optional[_Union[BatchCancelResultItem.Status, str]] = ..., order_id: _Optional[int] = ..., client_order_id: _Optional[str] = ..., code: _Optional[str] = ..., error: _Optional[_Union[ErrorDetail, _Mapping]] = ...) -> None: ...

class BatchCancelOrdersRequest(_message.Message):
    __slots__ = ("subaccount_id", "request_id", "items")
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    request_id: str
    items: _containers.RepeatedCompositeFieldContainer[BatchCancelItem]
    def __init__(self, subaccount_id: _Optional[int] = ..., request_id: _Optional[str] = ..., items: _Optional[_Iterable[_Union[BatchCancelItem, _Mapping]]] = ...) -> None: ...

class BatchCancelOrdersResponse(_message.Message):
    __slots__ = ("results", "accepted_count", "rejected_count", "ts", "ts_ns")
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    ACCEPTED_COUNT_FIELD_NUMBER: _ClassVar[int]
    REJECTED_COUNT_FIELD_NUMBER: _ClassVar[int]
    TS_FIELD_NUMBER: _ClassVar[int]
    TS_NS_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[BatchCancelResultItem]
    accepted_count: int
    rejected_count: int
    ts: _timestamp_pb2.Timestamp
    ts_ns: int
    def __init__(self, results: _Optional[_Iterable[_Union[BatchCancelResultItem, _Mapping]]] = ..., accepted_count: _Optional[int] = ..., rejected_count: _Optional[int] = ..., ts: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., ts_ns: _Optional[int] = ...) -> None: ...
