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
    ERROR_CODE_SOURCE_ACCOUNT_INACTIVE: _ClassVar[ErrorCode]
    ERROR_CODE_UNSUPPORTED_ASSET: _ClassVar[ErrorCode]
    ERROR_CODE_INVALID_AMOUNT: _ClassVar[ErrorCode]
    ERROR_CODE_INVALID_DESTINATION: _ClassVar[ErrorCode]
    ERROR_CODE_DESTINATION_NOT_FOUND: _ClassVar[ErrorCode]
    ERROR_CODE_DESTINATION_INACTIVE: _ClassVar[ErrorCode]
    ERROR_CODE_SAME_SOURCE_DESTINATION: _ClassVar[ErrorCode]
    ERROR_CODE_DESTINATION_NOT_WHITELISTED: _ClassVar[ErrorCode]
    ERROR_CODE_SMART_ACCOUNT_UNAVAILABLE: _ClassVar[ErrorCode]
    ERROR_CODE_STEP_UP_UNAVAILABLE: _ClassVar[ErrorCode]
    ERROR_CODE_IDEMPOTENCY_CONFLICT: _ClassVar[ErrorCode]
    ERROR_CODE_FUNDS_LOCK_CONFLICT: _ClassVar[ErrorCode]
    ERROR_CODE_CAPITAL_VIEW_UNAVAILABLE: _ClassVar[ErrorCode]
    ERROR_CODE_ACCOUNT_SHARD_UNAVAILABLE: _ClassVar[ErrorCode]
    ERROR_CODE_POLICY_DENIED: _ClassVar[ErrorCode]
    ERROR_CODE_FAILED_PRECONDITION: _ClassVar[ErrorCode]
    ERROR_CODE_NOT_FOUND: _ClassVar[ErrorCode]
    ERROR_CODE_CONFLICT: _ClassVar[ErrorCode]

class InternalTransferStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INTERNAL_TRANSFER_STATUS_UNSPECIFIED: _ClassVar[InternalTransferStatus]
    INTERNAL_TRANSFER_STATUS_ACCEPTED: _ClassVar[InternalTransferStatus]
    INTERNAL_TRANSFER_STATUS_REJECTED: _ClassVar[InternalTransferStatus]
    INTERNAL_TRANSFER_STATUS_FAILED: _ClassVar[InternalTransferStatus]
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
ERROR_CODE_SOURCE_ACCOUNT_INACTIVE: ErrorCode
ERROR_CODE_UNSUPPORTED_ASSET: ErrorCode
ERROR_CODE_INVALID_AMOUNT: ErrorCode
ERROR_CODE_INVALID_DESTINATION: ErrorCode
ERROR_CODE_DESTINATION_NOT_FOUND: ErrorCode
ERROR_CODE_DESTINATION_INACTIVE: ErrorCode
ERROR_CODE_SAME_SOURCE_DESTINATION: ErrorCode
ERROR_CODE_DESTINATION_NOT_WHITELISTED: ErrorCode
ERROR_CODE_SMART_ACCOUNT_UNAVAILABLE: ErrorCode
ERROR_CODE_STEP_UP_UNAVAILABLE: ErrorCode
ERROR_CODE_IDEMPOTENCY_CONFLICT: ErrorCode
ERROR_CODE_FUNDS_LOCK_CONFLICT: ErrorCode
ERROR_CODE_CAPITAL_VIEW_UNAVAILABLE: ErrorCode
ERROR_CODE_ACCOUNT_SHARD_UNAVAILABLE: ErrorCode
ERROR_CODE_POLICY_DENIED: ErrorCode
ERROR_CODE_FAILED_PRECONDITION: ErrorCode
ERROR_CODE_NOT_FOUND: ErrorCode
ERROR_CODE_CONFLICT: ErrorCode
INTERNAL_TRANSFER_STATUS_UNSPECIFIED: InternalTransferStatus
INTERNAL_TRANSFER_STATUS_ACCEPTED: InternalTransferStatus
INTERNAL_TRANSFER_STATUS_REJECTED: InternalTransferStatus
INTERNAL_TRANSFER_STATUS_FAILED: InternalTransferStatus

class CreateInternalTransferRequest(_message.Message):
    __slots__ = ("subaccount_id", "destination_account_id", "destination_subaccount_id", "destination_smart_account_address", "asset_id", "amount_e18", "idempotency_key")
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_SMART_ACCOUNT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_E18_FIELD_NUMBER: _ClassVar[int]
    IDEMPOTENCY_KEY_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    destination_account_id: int
    destination_subaccount_id: int
    destination_smart_account_address: str
    asset_id: int
    amount_e18: _u128_pb2.U128
    idempotency_key: str
    def __init__(self, subaccount_id: _Optional[int] = ..., destination_account_id: _Optional[int] = ..., destination_subaccount_id: _Optional[int] = ..., destination_smart_account_address: _Optional[str] = ..., asset_id: _Optional[int] = ..., amount_e18: _Optional[_Union[_u128_pb2.U128, _Mapping]] = ..., idempotency_key: _Optional[str] = ...) -> None: ...

class ResolvedDestination(_message.Message):
    __slots__ = ("root_account_public_id", "subaccount_public_id", "smart_account_address")
    ROOT_ACCOUNT_PUBLIC_ID_FIELD_NUMBER: _ClassVar[int]
    SUBACCOUNT_PUBLIC_ID_FIELD_NUMBER: _ClassVar[int]
    SMART_ACCOUNT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    root_account_public_id: str
    subaccount_public_id: str
    smart_account_address: str
    def __init__(self, root_account_public_id: _Optional[str] = ..., subaccount_public_id: _Optional[str] = ..., smart_account_address: _Optional[str] = ...) -> None: ...

class ErrorDetail(_message.Message):
    __slots__ = ("code",)
    CODE_FIELD_NUMBER: _ClassVar[int]
    code: ErrorCode
    def __init__(self, code: _Optional[_Union[ErrorCode, str]] = ...) -> None: ...

class CreateInternalTransferResponse(_message.Message):
    __slots__ = ("request_id", "transfer_id", "accepted_at_ts_ns", "asset_id", "asset_code", "u_asset_id", "amount_e18", "destination", "status")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    TRANSFER_ID_FIELD_NUMBER: _ClassVar[int]
    ACCEPTED_AT_TS_NS_FIELD_NUMBER: _ClassVar[int]
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    ASSET_CODE_FIELD_NUMBER: _ClassVar[int]
    U_ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_E18_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    transfer_id: str
    accepted_at_ts_ns: int
    asset_id: int
    asset_code: str
    u_asset_id: str
    amount_e18: _u128_pb2.U128
    destination: ResolvedDestination
    status: InternalTransferStatus
    def __init__(self, request_id: _Optional[str] = ..., transfer_id: _Optional[str] = ..., accepted_at_ts_ns: _Optional[int] = ..., asset_id: _Optional[int] = ..., asset_code: _Optional[str] = ..., u_asset_id: _Optional[str] = ..., amount_e18: _Optional[_Union[_u128_pb2.U128, _Mapping]] = ..., destination: _Optional[_Union[ResolvedDestination, _Mapping]] = ..., status: _Optional[_Union[InternalTransferStatus, str]] = ...) -> None: ...
