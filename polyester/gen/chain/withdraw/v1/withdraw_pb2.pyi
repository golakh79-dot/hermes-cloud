from polyester.gen.buf.validate import validate_pb2 as _validate_pb2
from polyester.gen.gnostic.openapi.v3 import annotations_pb2 as _annotations_pb2
from polyester.gen.google.api import annotations_pb2 as _annotations_pb2_1
from polyester.gen.polyester.api import options_pb2 as _options_pb2
from polyester.gen.polyester.type.v1 import u128_pb2 as _u128_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ErrorCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ERROR_CODE_UNSPECIFIED: _ClassVar[ErrorCode]
    ERROR_CODE_INSUFFICIENT_FUNDS: _ClassVar[ErrorCode]
    ERROR_CODE_INVALID_REQUEST: _ClassVar[ErrorCode]
    ERROR_CODE_UNAUTHENTICATED: _ClassVar[ErrorCode]
    ERROR_CODE_PERMISSION_DENIED: _ClassVar[ErrorCode]
    ERROR_CODE_RATE_LIMIT_EXCEEDED: _ClassVar[ErrorCode]
    ERROR_CODE_SERVICE_UNAVAILABLE: _ClassVar[ErrorCode]
    ERROR_CODE_INTERNAL_ERROR: _ClassVar[ErrorCode]
    ERROR_CODE_INVALID_SUBACCOUNT_ID: _ClassVar[ErrorCode]
    ERROR_CODE_SUBACCOUNT_NOT_FOUND: _ClassVar[ErrorCode]
    ERROR_CODE_INVALID_ACTION: _ClassVar[ErrorCode]
    ERROR_CODE_UNSUPPORTED_LEDGER: _ClassVar[ErrorCode]
    ERROR_CODE_UNSUPPORTED_ASSET: _ClassVar[ErrorCode]
    ERROR_CODE_INVALID_AMOUNT: _ClassVar[ErrorCode]
    ERROR_CODE_INVALID_DESTINATION_CHAIN: _ClassVar[ErrorCode]
    ERROR_CODE_INVALID_DESTINATION_ADDRESS: _ClassVar[ErrorCode]
    ERROR_CODE_EXTERNAL_DESTINATION_NOT_WHITELISTED: _ClassVar[ErrorCode]
    ERROR_CODE_INTERNAL_RECIPIENT_NOT_WHITELISTED: _ClassVar[ErrorCode]
    ERROR_CODE_AMOUNT_BELOW_MINIMUM: _ClassVar[ErrorCode]
    ERROR_CODE_AMOUNT_EXCEEDS_SUPPLY: _ClassVar[ErrorCode]
    ERROR_CODE_SOURCE_SMART_ACCOUNT_UNAVAILABLE: _ClassVar[ErrorCode]
    ERROR_CODE_SIGNATURE_REQUIRED: _ClassVar[ErrorCode]
    ERROR_CODE_SIGNATURE_SCHEME_UNSUPPORTED: _ClassVar[ErrorCode]
    ERROR_CODE_SIGNER_WALLET_INVALID: _ClassVar[ErrorCode]
    ERROR_CODE_WALLET_BINDING_INVALID: _ClassVar[ErrorCode]
    ERROR_CODE_WALLET_BINDING_SCOPE_MISMATCH: _ClassVar[ErrorCode]
    ERROR_CODE_WALLET_BINDING_SIGNER_MISMATCH: _ClassVar[ErrorCode]
    ERROR_CODE_API_KEY_NOT_FOUND: _ClassVar[ErrorCode]
    ERROR_CODE_API_KEY_BINDING_INVALID: _ClassVar[ErrorCode]
    ERROR_CODE_API_KEY_BINDING_SCOPE_MISMATCH: _ClassVar[ErrorCode]
    ERROR_CODE_API_KEY_BINDING_PUBLIC_KEY_MISMATCH: _ClassVar[ErrorCode]
    ERROR_CODE_IDEMPOTENCY_CONFLICT: _ClassVar[ErrorCode]
    ERROR_CODE_FUNDS_LOCK_CONFLICT: _ClassVar[ErrorCode]
    ERROR_CODE_CAPITAL_VIEW_UNAVAILABLE: _ClassVar[ErrorCode]
    ERROR_CODE_CHAIN_METADATA_UNAVAILABLE: _ClassVar[ErrorCode]
    ERROR_CODE_FEE_UNAVAILABLE: _ClassVar[ErrorCode]
    ERROR_CODE_SUPPLY_UNAVAILABLE: _ClassVar[ErrorCode]
    ERROR_CODE_STEP_UP_UNAVAILABLE: _ClassVar[ErrorCode]
    ERROR_CODE_DESTINATION_VALIDATION_UNAVAILABLE: _ClassVar[ErrorCode]
    ERROR_CODE_ACCOUNT_SHARD_UNAVAILABLE: _ClassVar[ErrorCode]
    ERROR_CODE_FAILED_PRECONDITION: _ClassVar[ErrorCode]
    ERROR_CODE_NOT_FOUND: _ClassVar[ErrorCode]
    ERROR_CODE_CONFLICT: _ClassVar[ErrorCode]
    ERROR_CODE_INVALID_AUTO_WITHDRAW_SCHEDULE: _ClassVar[ErrorCode]
    ERROR_CODE_AMOUNT_EXCEEDS_ROUTE_PRECISION: _ClassVar[ErrorCode]

class TradingWithdrawAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ACTION_UNSPECIFIED: _ClassVar[TradingWithdrawAction]
    TO_FUNDING: _ClassVar[TradingWithdrawAction]
    TO_EXTERNAL_CHAIN: _ClassVar[TradingWithdrawAction]

class WithdrawDestinationValidationCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RESULT_UNSPECIFIED: _ClassVar[WithdrawDestinationValidationCode]
    VALID: _ClassVar[WithdrawDestinationValidationCode]
    INVALID_ADDRESS: _ClassVar[WithdrawDestinationValidationCode]
    UNSUPPORTED_CHAIN: _ClassVar[WithdrawDestinationValidationCode]
    POLYESTER_SMART_ACCOUNT: _ClassVar[WithdrawDestinationValidationCode]
    TOKEN_CONTRACT: _ClassVar[WithdrawDestinationValidationCode]
    DENYLISTED_ADDRESS: _ClassVar[WithdrawDestinationValidationCode]
ERROR_CODE_UNSPECIFIED: ErrorCode
ERROR_CODE_INSUFFICIENT_FUNDS: ErrorCode
ERROR_CODE_INVALID_REQUEST: ErrorCode
ERROR_CODE_UNAUTHENTICATED: ErrorCode
ERROR_CODE_PERMISSION_DENIED: ErrorCode
ERROR_CODE_RATE_LIMIT_EXCEEDED: ErrorCode
ERROR_CODE_SERVICE_UNAVAILABLE: ErrorCode
ERROR_CODE_INTERNAL_ERROR: ErrorCode
ERROR_CODE_INVALID_SUBACCOUNT_ID: ErrorCode
ERROR_CODE_SUBACCOUNT_NOT_FOUND: ErrorCode
ERROR_CODE_INVALID_ACTION: ErrorCode
ERROR_CODE_UNSUPPORTED_LEDGER: ErrorCode
ERROR_CODE_UNSUPPORTED_ASSET: ErrorCode
ERROR_CODE_INVALID_AMOUNT: ErrorCode
ERROR_CODE_INVALID_DESTINATION_CHAIN: ErrorCode
ERROR_CODE_INVALID_DESTINATION_ADDRESS: ErrorCode
ERROR_CODE_EXTERNAL_DESTINATION_NOT_WHITELISTED: ErrorCode
ERROR_CODE_INTERNAL_RECIPIENT_NOT_WHITELISTED: ErrorCode
ERROR_CODE_AMOUNT_BELOW_MINIMUM: ErrorCode
ERROR_CODE_AMOUNT_EXCEEDS_SUPPLY: ErrorCode
ERROR_CODE_SOURCE_SMART_ACCOUNT_UNAVAILABLE: ErrorCode
ERROR_CODE_SIGNATURE_REQUIRED: ErrorCode
ERROR_CODE_SIGNATURE_SCHEME_UNSUPPORTED: ErrorCode
ERROR_CODE_SIGNER_WALLET_INVALID: ErrorCode
ERROR_CODE_WALLET_BINDING_INVALID: ErrorCode
ERROR_CODE_WALLET_BINDING_SCOPE_MISMATCH: ErrorCode
ERROR_CODE_WALLET_BINDING_SIGNER_MISMATCH: ErrorCode
ERROR_CODE_API_KEY_NOT_FOUND: ErrorCode
ERROR_CODE_API_KEY_BINDING_INVALID: ErrorCode
ERROR_CODE_API_KEY_BINDING_SCOPE_MISMATCH: ErrorCode
ERROR_CODE_API_KEY_BINDING_PUBLIC_KEY_MISMATCH: ErrorCode
ERROR_CODE_IDEMPOTENCY_CONFLICT: ErrorCode
ERROR_CODE_FUNDS_LOCK_CONFLICT: ErrorCode
ERROR_CODE_CAPITAL_VIEW_UNAVAILABLE: ErrorCode
ERROR_CODE_CHAIN_METADATA_UNAVAILABLE: ErrorCode
ERROR_CODE_FEE_UNAVAILABLE: ErrorCode
ERROR_CODE_SUPPLY_UNAVAILABLE: ErrorCode
ERROR_CODE_STEP_UP_UNAVAILABLE: ErrorCode
ERROR_CODE_DESTINATION_VALIDATION_UNAVAILABLE: ErrorCode
ERROR_CODE_ACCOUNT_SHARD_UNAVAILABLE: ErrorCode
ERROR_CODE_FAILED_PRECONDITION: ErrorCode
ERROR_CODE_NOT_FOUND: ErrorCode
ERROR_CODE_CONFLICT: ErrorCode
ERROR_CODE_INVALID_AUTO_WITHDRAW_SCHEDULE: ErrorCode
ERROR_CODE_AMOUNT_EXCEEDS_ROUTE_PRECISION: ErrorCode
ACTION_UNSPECIFIED: TradingWithdrawAction
TO_FUNDING: TradingWithdrawAction
TO_EXTERNAL_CHAIN: TradingWithdrawAction
RESULT_UNSPECIFIED: WithdrawDestinationValidationCode
VALID: WithdrawDestinationValidationCode
INVALID_ADDRESS: WithdrawDestinationValidationCode
UNSUPPORTED_CHAIN: WithdrawDestinationValidationCode
POLYESTER_SMART_ACCOUNT: WithdrawDestinationValidationCode
TOKEN_CONTRACT: WithdrawDestinationValidationCode
DENYLISTED_ADDRESS: WithdrawDestinationValidationCode

class CreateTradingWithdrawResponse(_message.Message):
    __slots__ = ("intent_id",)
    INTENT_ID_FIELD_NUMBER: _ClassVar[int]
    intent_id: str
    def __init__(self, intent_id: _Optional[str] = ...) -> None: ...

class CreateWalletTradingWithdrawResponse(_message.Message):
    __slots__ = ("intent_id",)
    INTENT_ID_FIELD_NUMBER: _ClassVar[int]
    intent_id: str
    def __init__(self, intent_id: _Optional[str] = ...) -> None: ...

class ErrorDetail(_message.Message):
    __slots__ = ("code",)
    CODE_FIELD_NUMBER: _ClassVar[int]
    code: ErrorCode
    def __init__(self, code: _Optional[_Union[ErrorCode, str]] = ...) -> None: ...

class TradingWithdrawIntentPayload(_message.Message):
    __slots__ = ("action", "asset_id", "destination_chain_id", "amount_e18", "deadline_ts_sec", "nonce", "destination_address", "idempotency_key")
    ACTION_FIELD_NUMBER: _ClassVar[int]
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_E18_FIELD_NUMBER: _ClassVar[int]
    DEADLINE_TS_SEC_FIELD_NUMBER: _ClassVar[int]
    NONCE_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    IDEMPOTENCY_KEY_FIELD_NUMBER: _ClassVar[int]
    action: TradingWithdrawAction
    asset_id: int
    destination_chain_id: int
    amount_e18: _u128_pb2.U128
    deadline_ts_sec: int
    nonce: _u128_pb2.U128
    destination_address: str
    idempotency_key: str
    def __init__(self, action: _Optional[_Union[TradingWithdrawAction, str]] = ..., asset_id: _Optional[int] = ..., destination_chain_id: _Optional[int] = ..., amount_e18: _Optional[_Union[_u128_pb2.U128, _Mapping]] = ..., deadline_ts_sec: _Optional[int] = ..., nonce: _Optional[_Union[_u128_pb2.U128, _Mapping]] = ..., destination_address: _Optional[str] = ..., idempotency_key: _Optional[str] = ...) -> None: ...

class CreateTradingWithdrawRequest(_message.Message):
    __slots__ = ("payload", "payload_signature")
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    payload: TradingWithdrawIntentPayload
    payload_signature: bytes
    def __init__(self, payload: _Optional[_Union[TradingWithdrawIntentPayload, _Mapping]] = ..., payload_signature: _Optional[bytes] = ...) -> None: ...

class CreateWalletTradingWithdrawRequest(_message.Message):
    __slots__ = ("payload", "subaccount_id", "signer_wallet", "payload_signature")
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    SIGNER_WALLET_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    payload: TradingWithdrawIntentPayload
    subaccount_id: int
    signer_wallet: str
    payload_signature: bytes
    def __init__(self, payload: _Optional[_Union[TradingWithdrawIntentPayload, _Mapping]] = ..., subaccount_id: _Optional[int] = ..., signer_wallet: _Optional[str] = ..., payload_signature: _Optional[bytes] = ...) -> None: ...

class ValidateWithdrawDestinationRequest(_message.Message):
    __slots__ = ("destination_chain_id", "destination_address")
    DESTINATION_CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    destination_chain_id: int
    destination_address: str
    def __init__(self, destination_chain_id: _Optional[int] = ..., destination_address: _Optional[str] = ...) -> None: ...

class ValidateWithdrawDestinationResponse(_message.Message):
    __slots__ = ("valid", "code", "message", "canonical_destination_address")
    VALID_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CANONICAL_DESTINATION_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    valid: bool
    code: WithdrawDestinationValidationCode
    message: str
    canonical_destination_address: str
    def __init__(self, valid: _Optional[bool] = ..., code: _Optional[_Union[WithdrawDestinationValidationCode, str]] = ..., message: _Optional[str] = ..., canonical_destination_address: _Optional[str] = ...) -> None: ...
