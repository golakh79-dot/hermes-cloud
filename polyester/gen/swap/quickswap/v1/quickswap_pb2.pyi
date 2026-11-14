import datetime

from polyester.gen.buf.validate import validate_pb2 as _validate_pb2
from polyester.gen.gnostic.openapi.v3 import annotations_pb2 as _annotations_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from polyester.gen.polyester.api import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class QuoteBasis(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BASIS_UNSPECIFIED: _ClassVar[QuoteBasis]
    SOURCE_AMOUNT: _ClassVar[QuoteBasis]
    DESTINATION_AMOUNT: _ClassVar[QuoteBasis]

class FeeKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FEE_UNSPECIFIED: _ClassVar[FeeKind]
    SERVICE: _ClassVar[FeeKind]
    BROKER: _ClassVar[FeeKind]
    AFFILIATE: _ClassVar[FeeKind]
    DEPOSIT_NETWORK: _ClassVar[FeeKind]
    WITHDRAWAL_NETWORK: _ClassVar[FeeKind]

class DepositAddressState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ADDRESS_UNSPECIFIED: _ClassVar[DepositAddressState]
    ACTIVE: _ClassVar[DepositAddressState]
    REFUND_MODE: _ClassVar[DepositAddressState]
    RETIRED: _ClassVar[DepositAddressState]

class DepositDisposition(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DISPOSITION_UNSPECIFIED: _ClassVar[DepositDisposition]
    EVALUATING: _ClassVar[DepositDisposition]
    ELIGIBLE: _ClassVar[DepositDisposition]
    RETURN_ONLY: _ClassVar[DepositDisposition]
    ON_HOLD: _ClassVar[DepositDisposition]
    MANUAL_RECOVERY: _ClassVar[DepositDisposition]

class QuickSwapReason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    REASON_UNSPECIFIED: _ClassVar[QuickSwapReason]
    SOURCE_SCREENING_FAILED: _ClassVar[QuickSwapReason]
    CAPACITY_UNAVAILABLE: _ClassVar[QuickSwapReason]
    PROTECTION_NOT_MET: _ClassVar[QuickSwapReason]
    EXECUTION_DEADLINE_REACHED: _ClassVar[QuickSwapReason]
    LATE_DEPOSIT: _ClassVar[QuickSwapReason]
    DEPOSIT_BELOW_MINIMUM: _ClassVar[QuickSwapReason]
    DEPOSIT_ABOVE_MAXIMUM: _ClassVar[QuickSwapReason]
    WRONG_ASSET: _ClassVar[QuickSwapReason]
    FUNDING_WINDOW_ENDED: _ClassVar[QuickSwapReason]
    WITHDRAWAL_FAILED: _ClassVar[QuickSwapReason]
    OUTCOME_RECONCILING: _ClassVar[QuickSwapReason]
    SOURCE_SCREENING_BLOCKED: _ClassVar[QuickSwapReason]
    REFUND_BELOW_MINIMUM: _ClassVar[QuickSwapReason]
    DEPOSIT_ADDRESS_CONFLICT: _ClassVar[QuickSwapReason]
    DEPOSIT_ADDRESS_ALREADY_USED: _ClassVar[QuickSwapReason]
    DEPOSIT_ADDRESS_RETIRED: _ClassVar[QuickSwapReason]
    DEPOSIT_ADDRESS_NOT_ISSUED: _ClassVar[QuickSwapReason]
    INTERMEDIATE_BELOW_MINIMUM: _ClassVar[QuickSwapReason]

class WithdrawalRole(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ROLE_UNSPECIFIED: _ClassVar[WithdrawalRole]
    DESTINATION: _ClassVar[WithdrawalRole]
    REFUND: _ClassVar[WithdrawalRole]
    RETURN: _ClassVar[WithdrawalRole]

class WithdrawalState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WITHDRAWAL_UNSPECIFIED: _ClassVar[WithdrawalState]
    QUEUED: _ClassVar[WithdrawalState]
    SUBMITTED: _ClassVar[WithdrawalState]
    FINALIZED: _ClassVar[WithdrawalState]
    FAILED: _ClassVar[WithdrawalState]
    NOT_SENT: _ClassVar[WithdrawalState]

class QuickSwapStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STATUS_UNSPECIFIED: _ClassVar[QuickSwapStatus]
    ALLOCATING: _ClassVar[QuickSwapStatus]
    AWAITING_DEPOSIT: _ClassVar[QuickSwapStatus]
    WAITING_FOR_CAPACITY: _ClassVar[QuickSwapStatus]
    PREPARING_DEPOSIT: _ClassVar[QuickSwapStatus]
    CONFIRMING: _ClassVar[QuickSwapStatus]
    CREDITED: _ClassVar[QuickSwapStatus]
    EXECUTING: _ClassVar[QuickSwapStatus]
    PAYING_OUT: _ClassVar[QuickSwapStatus]
    REFUNDING: _ClassVar[QuickSwapStatus]
    RETURNING: _ClassVar[QuickSwapStatus]
    HELD: _ClassVar[QuickSwapStatus]
    COMPLETED: _ClassVar[QuickSwapStatus]
    REFUNDED: _ClassVar[QuickSwapStatus]
    RETURNED: _ClassVar[QuickSwapStatus]
    EXPIRED: _ClassVar[QuickSwapStatus]

class ErrorCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ERROR_UNSPECIFIED: _ClassVar[ErrorCode]
    ROUTE_UNSUPPORTED: _ClassVar[ErrorCode]
    AMOUNT_OUT_OF_RANGE: _ClassVar[ErrorCode]
    DECIMALS_MISMATCH: _ClassVar[ErrorCode]
    DESTINATION_ADDRESS_INVALID: _ClassVar[ErrorCode]
    RETURN_ADDRESS_INVALID: _ClassVar[ErrorCode]
    REFUND_ADDRESS_REQUIRED: _ClassVar[ErrorCode]
    REFUND_ADDRESS_INVALID: _ClassVar[ErrorCode]
    SOURCE_WALLET_INVALID: _ClassVar[ErrorCode]
    QUOTE_UNAVAILABLE: _ClassVar[ErrorCode]
    PROTECTION_UNACHIEVABLE: _ClassVar[ErrorCode]
    ADDRESS_UNAVAILABLE: _ClassVar[ErrorCode]
    IDEMPOTENCY_CONFLICT: _ClassVar[ErrorCode]
    SWAP_NOT_FOUND: _ClassVar[ErrorCode]
    BROKER_DISABLED: _ClassVar[ErrorCode]
    BROKER_LIMIT: _ClassVar[ErrorCode]
    AFFILIATE_VAULT_UNKNOWN: _ClassVar[ErrorCode]
    BROKER_NOT_FOUND: _ClassVar[ErrorCode]
    ACTION_DENIED: _ClassVar[ErrorCode]
    STEP_UP_REQUIRED: _ClassVar[ErrorCode]
    VAULT_NOT_FOUND: _ClassVar[ErrorCode]
    KEY_NOT_FOUND: _ClassVar[ErrorCode]
    KEY_LIMIT: _ClassVar[ErrorCode]
    LAST_KEY: _ClassVar[ErrorCode]
    MEMBER_NOT_FOUND: _ClassVar[ErrorCode]
    ALREADY_MEMBER: _ClassVar[ErrorCode]
    OWNER_IMMUTABLE: _ClassVar[ErrorCode]
    INVITE_NOT_FOUND: _ClassVar[ErrorCode]
    FEES_INVALID: _ClassVar[ErrorCode]
    STATS_INCOMPLETE: _ClassVar[ErrorCode]
    ADDRESS_CONFLICT: _ClassVar[ErrorCode]
BASIS_UNSPECIFIED: QuoteBasis
SOURCE_AMOUNT: QuoteBasis
DESTINATION_AMOUNT: QuoteBasis
FEE_UNSPECIFIED: FeeKind
SERVICE: FeeKind
BROKER: FeeKind
AFFILIATE: FeeKind
DEPOSIT_NETWORK: FeeKind
WITHDRAWAL_NETWORK: FeeKind
ADDRESS_UNSPECIFIED: DepositAddressState
ACTIVE: DepositAddressState
REFUND_MODE: DepositAddressState
RETIRED: DepositAddressState
DISPOSITION_UNSPECIFIED: DepositDisposition
EVALUATING: DepositDisposition
ELIGIBLE: DepositDisposition
RETURN_ONLY: DepositDisposition
ON_HOLD: DepositDisposition
MANUAL_RECOVERY: DepositDisposition
REASON_UNSPECIFIED: QuickSwapReason
SOURCE_SCREENING_FAILED: QuickSwapReason
CAPACITY_UNAVAILABLE: QuickSwapReason
PROTECTION_NOT_MET: QuickSwapReason
EXECUTION_DEADLINE_REACHED: QuickSwapReason
LATE_DEPOSIT: QuickSwapReason
DEPOSIT_BELOW_MINIMUM: QuickSwapReason
DEPOSIT_ABOVE_MAXIMUM: QuickSwapReason
WRONG_ASSET: QuickSwapReason
FUNDING_WINDOW_ENDED: QuickSwapReason
WITHDRAWAL_FAILED: QuickSwapReason
OUTCOME_RECONCILING: QuickSwapReason
SOURCE_SCREENING_BLOCKED: QuickSwapReason
REFUND_BELOW_MINIMUM: QuickSwapReason
DEPOSIT_ADDRESS_CONFLICT: QuickSwapReason
DEPOSIT_ADDRESS_ALREADY_USED: QuickSwapReason
DEPOSIT_ADDRESS_RETIRED: QuickSwapReason
DEPOSIT_ADDRESS_NOT_ISSUED: QuickSwapReason
INTERMEDIATE_BELOW_MINIMUM: QuickSwapReason
ROLE_UNSPECIFIED: WithdrawalRole
DESTINATION: WithdrawalRole
REFUND: WithdrawalRole
RETURN: WithdrawalRole
WITHDRAWAL_UNSPECIFIED: WithdrawalState
QUEUED: WithdrawalState
SUBMITTED: WithdrawalState
FINALIZED: WithdrawalState
FAILED: WithdrawalState
NOT_SENT: WithdrawalState
STATUS_UNSPECIFIED: QuickSwapStatus
ALLOCATING: QuickSwapStatus
AWAITING_DEPOSIT: QuickSwapStatus
WAITING_FOR_CAPACITY: QuickSwapStatus
PREPARING_DEPOSIT: QuickSwapStatus
CONFIRMING: QuickSwapStatus
CREDITED: QuickSwapStatus
EXECUTING: QuickSwapStatus
PAYING_OUT: QuickSwapStatus
REFUNDING: QuickSwapStatus
RETURNING: QuickSwapStatus
HELD: QuickSwapStatus
COMPLETED: QuickSwapStatus
REFUNDED: QuickSwapStatus
RETURNED: QuickSwapStatus
EXPIRED: QuickSwapStatus
ERROR_UNSPECIFIED: ErrorCode
ROUTE_UNSUPPORTED: ErrorCode
AMOUNT_OUT_OF_RANGE: ErrorCode
DECIMALS_MISMATCH: ErrorCode
DESTINATION_ADDRESS_INVALID: ErrorCode
RETURN_ADDRESS_INVALID: ErrorCode
REFUND_ADDRESS_REQUIRED: ErrorCode
REFUND_ADDRESS_INVALID: ErrorCode
SOURCE_WALLET_INVALID: ErrorCode
QUOTE_UNAVAILABLE: ErrorCode
PROTECTION_UNACHIEVABLE: ErrorCode
ADDRESS_UNAVAILABLE: ErrorCode
IDEMPOTENCY_CONFLICT: ErrorCode
SWAP_NOT_FOUND: ErrorCode
BROKER_DISABLED: ErrorCode
BROKER_LIMIT: ErrorCode
AFFILIATE_VAULT_UNKNOWN: ErrorCode
BROKER_NOT_FOUND: ErrorCode
ACTION_DENIED: ErrorCode
STEP_UP_REQUIRED: ErrorCode
VAULT_NOT_FOUND: ErrorCode
KEY_NOT_FOUND: ErrorCode
KEY_LIMIT: ErrorCode
LAST_KEY: ErrorCode
MEMBER_NOT_FOUND: ErrorCode
ALREADY_MEMBER: ErrorCode
OWNER_IMMUTABLE: ErrorCode
INVITE_NOT_FOUND: ErrorCode
FEES_INVALID: ErrorCode
STATS_INCOMPLETE: ErrorCode
ADDRESS_CONFLICT: ErrorCode

class TokenAmount(_message.Message):
    __slots__ = ("base_units", "decimals")
    BASE_UNITS_FIELD_NUMBER: _ClassVar[int]
    DECIMALS_FIELD_NUMBER: _ClassVar[int]
    base_units: str
    decimals: int
    def __init__(self, base_units: _Optional[str] = ..., decimals: _Optional[int] = ...) -> None: ...

class Protection(_message.Message):
    __slots__ = ("max_slippage_bps", "min_amount_out")
    MAX_SLIPPAGE_BPS_FIELD_NUMBER: _ClassVar[int]
    MIN_AMOUNT_OUT_FIELD_NUMBER: _ClassVar[int]
    max_slippage_bps: int
    min_amount_out: TokenAmount
    def __init__(self, max_slippage_bps: _Optional[int] = ..., min_amount_out: _Optional[_Union[TokenAmount, _Mapping]] = ...) -> None: ...

class MarketExecution(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class TwapExecution(_message.Message):
    __slots__ = ("duration_ms", "slice_interval_ms")
    DURATION_MS_FIELD_NUMBER: _ClassVar[int]
    SLICE_INTERVAL_MS_FIELD_NUMBER: _ClassVar[int]
    duration_ms: int
    slice_interval_ms: int
    def __init__(self, duration_ms: _Optional[int] = ..., slice_interval_ms: _Optional[int] = ...) -> None: ...

class Execution(_message.Message):
    __slots__ = ("market", "twap")
    MARKET_FIELD_NUMBER: _ClassVar[int]
    TWAP_FIELD_NUMBER: _ClassVar[int]
    market: MarketExecution
    twap: TwapExecution
    def __init__(self, market: _Optional[_Union[MarketExecution, _Mapping]] = ..., twap: _Optional[_Union[TwapExecution, _Mapping]] = ...) -> None: ...

class QuickSwapTerms(_message.Message):
    __slots__ = ("source_zipped_asset_id", "destination_zipped_asset_id", "basis", "amount", "protection", "execution")
    SOURCE_ZIPPED_ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_ZIPPED_ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    BASIS_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    PROTECTION_FIELD_NUMBER: _ClassVar[int]
    EXECUTION_FIELD_NUMBER: _ClassVar[int]
    source_zipped_asset_id: int
    destination_zipped_asset_id: int
    basis: QuoteBasis
    amount: TokenAmount
    protection: Protection
    execution: Execution
    def __init__(self, source_zipped_asset_id: _Optional[int] = ..., destination_zipped_asset_id: _Optional[int] = ..., basis: _Optional[_Union[QuoteBasis, str]] = ..., amount: _Optional[_Union[TokenAmount, _Mapping]] = ..., protection: _Optional[_Union[Protection, _Mapping]] = ..., execution: _Optional[_Union[Execution, _Mapping]] = ...) -> None: ...

class QuoteFee(_message.Message):
    __slots__ = ("kind", "zipped_asset_id", "amount", "bps", "account_id")
    KIND_FIELD_NUMBER: _ClassVar[int]
    ZIPPED_ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    BPS_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    kind: FeeKind
    zipped_asset_id: int
    amount: TokenAmount
    bps: int
    account_id: int
    def __init__(self, kind: _Optional[_Union[FeeKind, str]] = ..., zipped_asset_id: _Optional[int] = ..., amount: _Optional[_Union[TokenAmount, _Mapping]] = ..., bps: _Optional[int] = ..., account_id: _Optional[int] = ...) -> None: ...

class QuickSwapQuote(_message.Message):
    __slots__ = ("deposit_amount", "expected_amount_out", "min_amount_out", "min_rate", "min_deposit_amount", "max_deposit_amount", "intermediate_asset_id", "fees", "quoted_at", "expires_at")
    DEPOSIT_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_AMOUNT_OUT_FIELD_NUMBER: _ClassVar[int]
    MIN_AMOUNT_OUT_FIELD_NUMBER: _ClassVar[int]
    MIN_RATE_FIELD_NUMBER: _ClassVar[int]
    MIN_DEPOSIT_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    MAX_DEPOSIT_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    INTERMEDIATE_ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    FEES_FIELD_NUMBER: _ClassVar[int]
    QUOTED_AT_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    deposit_amount: TokenAmount
    expected_amount_out: TokenAmount
    min_amount_out: TokenAmount
    min_rate: str
    min_deposit_amount: TokenAmount
    max_deposit_amount: TokenAmount
    intermediate_asset_id: int
    fees: _containers.RepeatedCompositeFieldContainer[QuoteFee]
    quoted_at: _timestamp_pb2.Timestamp
    expires_at: _timestamp_pb2.Timestamp
    def __init__(self, deposit_amount: _Optional[_Union[TokenAmount, _Mapping]] = ..., expected_amount_out: _Optional[_Union[TokenAmount, _Mapping]] = ..., min_amount_out: _Optional[_Union[TokenAmount, _Mapping]] = ..., min_rate: _Optional[str] = ..., min_deposit_amount: _Optional[_Union[TokenAmount, _Mapping]] = ..., max_deposit_amount: _Optional[_Union[TokenAmount, _Mapping]] = ..., intermediate_asset_id: _Optional[int] = ..., fees: _Optional[_Iterable[_Union[QuoteFee, _Mapping]]] = ..., quoted_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., expires_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class Screening(_message.Message):
    __slots__ = ("source_wallet",)
    SOURCE_WALLET_FIELD_NUMBER: _ClassVar[int]
    source_wallet: str
    def __init__(self, source_wallet: _Optional[str] = ...) -> None: ...

class DepositInstructions(_message.Message):
    __slots__ = ("address", "memo", "zipped_asset_id", "issued_at", "funding_expires_at", "address_retires_at", "address_state", "min_native_gas_limit")
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    MEMO_FIELD_NUMBER: _ClassVar[int]
    ZIPPED_ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    ISSUED_AT_FIELD_NUMBER: _ClassVar[int]
    FUNDING_EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_RETIRES_AT_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_STATE_FIELD_NUMBER: _ClassVar[int]
    MIN_NATIVE_GAS_LIMIT_FIELD_NUMBER: _ClassVar[int]
    address: str
    memo: str
    zipped_asset_id: int
    issued_at: _timestamp_pb2.Timestamp
    funding_expires_at: _timestamp_pb2.Timestamp
    address_retires_at: _timestamp_pb2.Timestamp
    address_state: DepositAddressState
    min_native_gas_limit: int
    def __init__(self, address: _Optional[str] = ..., memo: _Optional[str] = ..., zipped_asset_id: _Optional[int] = ..., issued_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., funding_expires_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., address_retires_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., address_state: _Optional[_Union[DepositAddressState, str]] = ..., min_native_gas_limit: _Optional[int] = ...) -> None: ...

class Deposit(_message.Message):
    __slots__ = ("index", "tx_hash", "tx_occurrence_index", "zipped_asset_id", "amount", "disposition", "reason", "confirmations", "required_confirmations", "detected_at", "credited_at", "flow_id")
    INDEX_FIELD_NUMBER: _ClassVar[int]
    TX_HASH_FIELD_NUMBER: _ClassVar[int]
    TX_OCCURRENCE_INDEX_FIELD_NUMBER: _ClassVar[int]
    ZIPPED_ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    DISPOSITION_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    CONFIRMATIONS_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_CONFIRMATIONS_FIELD_NUMBER: _ClassVar[int]
    DETECTED_AT_FIELD_NUMBER: _ClassVar[int]
    CREDITED_AT_FIELD_NUMBER: _ClassVar[int]
    FLOW_ID_FIELD_NUMBER: _ClassVar[int]
    index: int
    tx_hash: str
    tx_occurrence_index: int
    zipped_asset_id: int
    amount: TokenAmount
    disposition: DepositDisposition
    reason: QuickSwapReason
    confirmations: int
    required_confirmations: int
    detected_at: _timestamp_pb2.Timestamp
    credited_at: _timestamp_pb2.Timestamp
    flow_id: str
    def __init__(self, index: _Optional[int] = ..., tx_hash: _Optional[str] = ..., tx_occurrence_index: _Optional[int] = ..., zipped_asset_id: _Optional[int] = ..., amount: _Optional[_Union[TokenAmount, _Mapping]] = ..., disposition: _Optional[_Union[DepositDisposition, str]] = ..., reason: _Optional[_Union[QuickSwapReason, str]] = ..., confirmations: _Optional[int] = ..., required_confirmations: _Optional[int] = ..., detected_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., credited_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., flow_id: _Optional[str] = ...) -> None: ...

class ExecutionProgress(_message.Message):
    __slots__ = ("input_amount", "executed_input", "output_amount", "intermediate_remainder", "completed_slices", "total_slices", "started_at", "deadline", "finished_at")
    INPUT_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    EXECUTED_INPUT_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    INTERMEDIATE_REMAINDER_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_SLICES_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SLICES_FIELD_NUMBER: _ClassVar[int]
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    DEADLINE_FIELD_NUMBER: _ClassVar[int]
    FINISHED_AT_FIELD_NUMBER: _ClassVar[int]
    input_amount: TokenAmount
    executed_input: TokenAmount
    output_amount: TokenAmount
    intermediate_remainder: TokenAmount
    completed_slices: int
    total_slices: int
    started_at: _timestamp_pb2.Timestamp
    deadline: _timestamp_pb2.Timestamp
    finished_at: _timestamp_pb2.Timestamp
    def __init__(self, input_amount: _Optional[_Union[TokenAmount, _Mapping]] = ..., executed_input: _Optional[_Union[TokenAmount, _Mapping]] = ..., output_amount: _Optional[_Union[TokenAmount, _Mapping]] = ..., intermediate_remainder: _Optional[_Union[TokenAmount, _Mapping]] = ..., completed_slices: _Optional[int] = ..., total_slices: _Optional[int] = ..., started_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., deadline: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., finished_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class Withdrawal(_message.Message):
    __slots__ = ("index", "role", "deposit_index", "zipped_asset_id", "address", "memo", "amount", "network_fee", "state", "tx_hash", "submitted_at", "finalized_at", "flow_id", "unsent_amount")
    INDEX_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    DEPOSIT_INDEX_FIELD_NUMBER: _ClassVar[int]
    ZIPPED_ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    MEMO_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    NETWORK_FEE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    TX_HASH_FIELD_NUMBER: _ClassVar[int]
    SUBMITTED_AT_FIELD_NUMBER: _ClassVar[int]
    FINALIZED_AT_FIELD_NUMBER: _ClassVar[int]
    FLOW_ID_FIELD_NUMBER: _ClassVar[int]
    UNSENT_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    index: int
    role: WithdrawalRole
    deposit_index: int
    zipped_asset_id: int
    address: str
    memo: str
    amount: TokenAmount
    network_fee: TokenAmount
    state: WithdrawalState
    tx_hash: str
    submitted_at: _timestamp_pb2.Timestamp
    finalized_at: _timestamp_pb2.Timestamp
    flow_id: str
    unsent_amount: TokenAmount
    def __init__(self, index: _Optional[int] = ..., role: _Optional[_Union[WithdrawalRole, str]] = ..., deposit_index: _Optional[int] = ..., zipped_asset_id: _Optional[int] = ..., address: _Optional[str] = ..., memo: _Optional[str] = ..., amount: _Optional[_Union[TokenAmount, _Mapping]] = ..., network_fee: _Optional[_Union[TokenAmount, _Mapping]] = ..., state: _Optional[_Union[WithdrawalState, str]] = ..., tx_hash: _Optional[str] = ..., submitted_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., finalized_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., flow_id: _Optional[str] = ..., unsent_amount: _Optional[_Union[TokenAmount, _Mapping]] = ...) -> None: ...

class QuickSwap(_message.Message):
    __slots__ = ("swap_id", "idempotency_key", "status", "reason", "is_terminal", "terms", "destination_address", "destination_memo", "return_address", "return_memo", "refund_zipped_asset_id", "refund_address", "refund_memo", "quote", "deposit_instructions", "screening", "deposits", "deposits_truncated", "execution", "withdrawals", "withdrawals_truncated", "created_at", "updated_at", "terminal_at", "version", "fee_schedule_version", "fees", "charged_fees")
    SWAP_ID_FIELD_NUMBER: _ClassVar[int]
    IDEMPOTENCY_KEY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    IS_TERMINAL_FIELD_NUMBER: _ClassVar[int]
    TERMS_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_MEMO_FIELD_NUMBER: _ClassVar[int]
    RETURN_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    RETURN_MEMO_FIELD_NUMBER: _ClassVar[int]
    REFUND_ZIPPED_ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    REFUND_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    REFUND_MEMO_FIELD_NUMBER: _ClassVar[int]
    QUOTE_FIELD_NUMBER: _ClassVar[int]
    DEPOSIT_INSTRUCTIONS_FIELD_NUMBER: _ClassVar[int]
    SCREENING_FIELD_NUMBER: _ClassVar[int]
    DEPOSITS_FIELD_NUMBER: _ClassVar[int]
    DEPOSITS_TRUNCATED_FIELD_NUMBER: _ClassVar[int]
    EXECUTION_FIELD_NUMBER: _ClassVar[int]
    WITHDRAWALS_FIELD_NUMBER: _ClassVar[int]
    WITHDRAWALS_TRUNCATED_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    TERMINAL_AT_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    FEE_SCHEDULE_VERSION_FIELD_NUMBER: _ClassVar[int]
    FEES_FIELD_NUMBER: _ClassVar[int]
    CHARGED_FEES_FIELD_NUMBER: _ClassVar[int]
    swap_id: int
    idempotency_key: str
    status: QuickSwapStatus
    reason: QuickSwapReason
    is_terminal: bool
    terms: QuickSwapTerms
    destination_address: str
    destination_memo: str
    return_address: str
    return_memo: str
    refund_zipped_asset_id: int
    refund_address: str
    refund_memo: str
    quote: QuickSwapQuote
    deposit_instructions: DepositInstructions
    screening: Screening
    deposits: _containers.RepeatedCompositeFieldContainer[Deposit]
    deposits_truncated: bool
    execution: ExecutionProgress
    withdrawals: _containers.RepeatedCompositeFieldContainer[Withdrawal]
    withdrawals_truncated: bool
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    terminal_at: _timestamp_pb2.Timestamp
    version: int
    fee_schedule_version: int
    fees: RequestedFees
    charged_fees: _containers.RepeatedCompositeFieldContainer[ChargedFee]
    def __init__(self, swap_id: _Optional[int] = ..., idempotency_key: _Optional[str] = ..., status: _Optional[_Union[QuickSwapStatus, str]] = ..., reason: _Optional[_Union[QuickSwapReason, str]] = ..., is_terminal: _Optional[bool] = ..., terms: _Optional[_Union[QuickSwapTerms, _Mapping]] = ..., destination_address: _Optional[str] = ..., destination_memo: _Optional[str] = ..., return_address: _Optional[str] = ..., return_memo: _Optional[str] = ..., refund_zipped_asset_id: _Optional[int] = ..., refund_address: _Optional[str] = ..., refund_memo: _Optional[str] = ..., quote: _Optional[_Union[QuickSwapQuote, _Mapping]] = ..., deposit_instructions: _Optional[_Union[DepositInstructions, _Mapping]] = ..., screening: _Optional[_Union[Screening, _Mapping]] = ..., deposits: _Optional[_Iterable[_Union[Deposit, _Mapping]]] = ..., deposits_truncated: _Optional[bool] = ..., execution: _Optional[_Union[ExecutionProgress, _Mapping]] = ..., withdrawals: _Optional[_Iterable[_Union[Withdrawal, _Mapping]]] = ..., withdrawals_truncated: _Optional[bool] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., terminal_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., version: _Optional[int] = ..., fee_schedule_version: _Optional[int] = ..., fees: _Optional[_Union[RequestedFees, _Mapping]] = ..., charged_fees: _Optional[_Iterable[_Union[ChargedFee, _Mapping]]] = ...) -> None: ...

class RequestedFees(_message.Message):
    __slots__ = ("broker_bps", "affiliates")
    BROKER_BPS_FIELD_NUMBER: _ClassVar[int]
    AFFILIATES_FIELD_NUMBER: _ClassVar[int]
    broker_bps: int
    affiliates: _containers.RepeatedCompositeFieldContainer[AffiliateShare]
    def __init__(self, broker_bps: _Optional[int] = ..., affiliates: _Optional[_Iterable[_Union[AffiliateShare, _Mapping]]] = ...) -> None: ...

class ChargedFee(_message.Message):
    __slots__ = ("kind", "account_id", "asset_id", "amount")
    KIND_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    kind: FeeKind
    account_id: int
    asset_id: int
    amount: TokenAmount
    def __init__(self, kind: _Optional[_Union[FeeKind, str]] = ..., account_id: _Optional[int] = ..., asset_id: _Optional[int] = ..., amount: _Optional[_Union[TokenAmount, _Mapping]] = ...) -> None: ...

class QuoteQuickSwapRequest(_message.Message):
    __slots__ = ("terms", "broker_bps", "affiliates")
    TERMS_FIELD_NUMBER: _ClassVar[int]
    BROKER_BPS_FIELD_NUMBER: _ClassVar[int]
    AFFILIATES_FIELD_NUMBER: _ClassVar[int]
    terms: QuickSwapTerms
    broker_bps: int
    affiliates: _containers.RepeatedCompositeFieldContainer[AffiliateShare]
    def __init__(self, terms: _Optional[_Union[QuickSwapTerms, _Mapping]] = ..., broker_bps: _Optional[int] = ..., affiliates: _Optional[_Iterable[_Union[AffiliateShare, _Mapping]]] = ...) -> None: ...

class QuoteQuickSwapResponse(_message.Message):
    __slots__ = ("quote",)
    QUOTE_FIELD_NUMBER: _ClassVar[int]
    quote: QuickSwapQuote
    def __init__(self, quote: _Optional[_Union[QuickSwapQuote, _Mapping]] = ...) -> None: ...

class AffiliateShare(_message.Message):
    __slots__ = ("account_id", "bps")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    BPS_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    bps: int
    def __init__(self, account_id: _Optional[int] = ..., bps: _Optional[int] = ...) -> None: ...

class CreateQuickSwapRequest(_message.Message):
    __slots__ = ("idempotency_key", "terms", "destination_address", "destination_memo", "return_address", "return_memo", "refund_zipped_asset_id", "refund_address", "refund_memo", "source_wallet", "affiliates", "broker_bps")
    IDEMPOTENCY_KEY_FIELD_NUMBER: _ClassVar[int]
    TERMS_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_MEMO_FIELD_NUMBER: _ClassVar[int]
    RETURN_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    RETURN_MEMO_FIELD_NUMBER: _ClassVar[int]
    REFUND_ZIPPED_ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    REFUND_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    REFUND_MEMO_FIELD_NUMBER: _ClassVar[int]
    SOURCE_WALLET_FIELD_NUMBER: _ClassVar[int]
    AFFILIATES_FIELD_NUMBER: _ClassVar[int]
    BROKER_BPS_FIELD_NUMBER: _ClassVar[int]
    idempotency_key: str
    terms: QuickSwapTerms
    destination_address: str
    destination_memo: str
    return_address: str
    return_memo: str
    refund_zipped_asset_id: int
    refund_address: str
    refund_memo: str
    source_wallet: str
    affiliates: _containers.RepeatedCompositeFieldContainer[AffiliateShare]
    broker_bps: int
    def __init__(self, idempotency_key: _Optional[str] = ..., terms: _Optional[_Union[QuickSwapTerms, _Mapping]] = ..., destination_address: _Optional[str] = ..., destination_memo: _Optional[str] = ..., return_address: _Optional[str] = ..., return_memo: _Optional[str] = ..., refund_zipped_asset_id: _Optional[int] = ..., refund_address: _Optional[str] = ..., refund_memo: _Optional[str] = ..., source_wallet: _Optional[str] = ..., affiliates: _Optional[_Iterable[_Union[AffiliateShare, _Mapping]]] = ..., broker_bps: _Optional[int] = ...) -> None: ...

class CreateQuickSwapResponse(_message.Message):
    __slots__ = ("quick_swap",)
    QUICK_SWAP_FIELD_NUMBER: _ClassVar[int]
    quick_swap: QuickSwap
    def __init__(self, quick_swap: _Optional[_Union[QuickSwap, _Mapping]] = ...) -> None: ...

class GetQuickSwapRequest(_message.Message):
    __slots__ = ("swap_id", "idempotency_key")
    SWAP_ID_FIELD_NUMBER: _ClassVar[int]
    IDEMPOTENCY_KEY_FIELD_NUMBER: _ClassVar[int]
    swap_id: int
    idempotency_key: str
    def __init__(self, swap_id: _Optional[int] = ..., idempotency_key: _Optional[str] = ...) -> None: ...

class GetQuickSwapResponse(_message.Message):
    __slots__ = ("quick_swap",)
    QUICK_SWAP_FIELD_NUMBER: _ClassVar[int]
    quick_swap: QuickSwap
    def __init__(self, quick_swap: _Optional[_Union[QuickSwap, _Mapping]] = ...) -> None: ...

class ErrorDetail(_message.Message):
    __slots__ = ("code", "swap_id", "min_deposit_amount", "max_deposit_amount")
    CODE_FIELD_NUMBER: _ClassVar[int]
    SWAP_ID_FIELD_NUMBER: _ClassVar[int]
    MIN_DEPOSIT_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    MAX_DEPOSIT_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    code: ErrorCode
    swap_id: int
    min_deposit_amount: TokenAmount
    max_deposit_amount: TokenAmount
    def __init__(self, code: _Optional[_Union[ErrorCode, str]] = ..., swap_id: _Optional[int] = ..., min_deposit_amount: _Optional[_Union[TokenAmount, _Mapping]] = ..., max_deposit_amount: _Optional[_Union[TokenAmount, _Mapping]] = ...) -> None: ...
