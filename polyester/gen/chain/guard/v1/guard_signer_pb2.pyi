from polyester.gen.buf.validate import validate_pb2 as _validate_pb2
from polyester.gen.gnostic.openapi.v3 import annotations_pb2 as _annotations_pb2
from polyester.gen.polyester.api import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ProtectedAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PROTECTED_ACTION_UNSPECIFIED: _ClassVar[ProtectedAction]
    PROTECTED_ACTION_FUNDING_SET_EXTERNAL_WHITELIST_REQUIRED: _ClassVar[ProtectedAction]
    PROTECTED_ACTION_FUNDING_ADD_EXTERNAL_WHITELIST: _ClassVar[ProtectedAction]
    PROTECTED_ACTION_FUNDING_REMOVE_EXTERNAL_WHITELIST: _ClassVar[ProtectedAction]
    PROTECTED_ACTION_FUNDING_ADD_INTERNAL_WHITELIST: _ClassVar[ProtectedAction]
    PROTECTED_ACTION_FUNDING_REMOVE_INTERNAL_WHITELIST: _ClassVar[ProtectedAction]
    PROTECTED_ACTION_FUNDING_SET_INTERNAL_WHITELIST_REQUIRED: _ClassVar[ProtectedAction]
PROTECTED_ACTION_UNSPECIFIED: ProtectedAction
PROTECTED_ACTION_FUNDING_SET_EXTERNAL_WHITELIST_REQUIRED: ProtectedAction
PROTECTED_ACTION_FUNDING_ADD_EXTERNAL_WHITELIST: ProtectedAction
PROTECTED_ACTION_FUNDING_REMOVE_EXTERNAL_WHITELIST: ProtectedAction
PROTECTED_ACTION_FUNDING_ADD_INTERNAL_WHITELIST: ProtectedAction
PROTECTED_ACTION_FUNDING_REMOVE_INTERNAL_WHITELIST: ProtectedAction
PROTECTED_ACTION_FUNDING_SET_INTERNAL_WHITELIST_REQUIRED: ProtectedAction

class GuardSignerStatus(_message.Message):
    __slots__ = ("signer_address", "onchain_signer_address", "initialized", "nonce", "nonce_space")
    SIGNER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    ONCHAIN_SIGNER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    INITIALIZED_FIELD_NUMBER: _ClassVar[int]
    NONCE_FIELD_NUMBER: _ClassVar[int]
    NONCE_SPACE_FIELD_NUMBER: _ClassVar[int]
    signer_address: str
    onchain_signer_address: str
    initialized: bool
    nonce: str
    nonce_space: int
    def __init__(self, signer_address: _Optional[str] = ..., onchain_signer_address: _Optional[str] = ..., initialized: _Optional[bool] = ..., nonce: _Optional[str] = ..., nonce_space: _Optional[int] = ...) -> None: ...

class GuardApproval(_message.Message):
    __slots__ = ("nonce_space", "deadline_unix", "signature")
    NONCE_SPACE_FIELD_NUMBER: _ClassVar[int]
    DEADLINE_UNIX_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    nonce_space: int
    deadline_unix: int
    signature: bytes
    def __init__(self, nonce_space: _Optional[int] = ..., deadline_unix: _Optional[int] = ..., signature: _Optional[bytes] = ...) -> None: ...

class ExternalWhitelistArgs(_message.Message):
    __slots__ = ("polychain_chain_id", "addresses")
    POLYCHAIN_CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    ADDRESSES_FIELD_NUMBER: _ClassVar[int]
    polychain_chain_id: int
    addresses: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, polychain_chain_id: _Optional[int] = ..., addresses: _Optional[_Iterable[str]] = ...) -> None: ...

class InternalWhitelistArgs(_message.Message):
    __slots__ = ("addresses",)
    ADDRESSES_FIELD_NUMBER: _ClassVar[int]
    addresses: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, addresses: _Optional[_Iterable[str]] = ...) -> None: ...

class WhitelistRequirementArgs(_message.Message):
    __slots__ = ("required",)
    REQUIRED_FIELD_NUMBER: _ClassVar[int]
    required: bool
    def __init__(self, required: _Optional[bool] = ...) -> None: ...

class ProtectedActionArgs(_message.Message):
    __slots__ = ("external_whitelist", "internal_whitelist", "whitelist_requirement")
    EXTERNAL_WHITELIST_FIELD_NUMBER: _ClassVar[int]
    INTERNAL_WHITELIST_FIELD_NUMBER: _ClassVar[int]
    WHITELIST_REQUIREMENT_FIELD_NUMBER: _ClassVar[int]
    external_whitelist: ExternalWhitelistArgs
    internal_whitelist: InternalWhitelistArgs
    whitelist_requirement: WhitelistRequirementArgs
    def __init__(self, external_whitelist: _Optional[_Union[ExternalWhitelistArgs, _Mapping]] = ..., internal_whitelist: _Optional[_Union[InternalWhitelistArgs, _Mapping]] = ..., whitelist_requirement: _Optional[_Union[WhitelistRequirementArgs, _Mapping]] = ...) -> None: ...

class CreateGuardSignerWalletRequest(_message.Message):
    __slots__ = ("subaccount_id",)
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    def __init__(self, subaccount_id: _Optional[int] = ...) -> None: ...

class CreateGuardSignerWalletResponse(_message.Message):
    __slots__ = ("signer_address",)
    SIGNER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    signer_address: str
    def __init__(self, signer_address: _Optional[str] = ...) -> None: ...

class GetGuardSignerStatusRequest(_message.Message):
    __slots__ = ("subaccount_id",)
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    def __init__(self, subaccount_id: _Optional[int] = ...) -> None: ...

class GetGuardSignerStatusResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: GuardSignerStatus
    def __init__(self, status: _Optional[_Union[GuardSignerStatus, _Mapping]] = ...) -> None: ...

class SignProtectedActionRequest(_message.Message):
    __slots__ = ("subaccount_id", "action", "args")
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    action: ProtectedAction
    args: ProtectedActionArgs
    def __init__(self, subaccount_id: _Optional[int] = ..., action: _Optional[_Union[ProtectedAction, str]] = ..., args: _Optional[_Union[ProtectedActionArgs, _Mapping]] = ...) -> None: ...

class SignProtectedActionResponse(_message.Message):
    __slots__ = ("approval",)
    APPROVAL_FIELD_NUMBER: _ClassVar[int]
    approval: GuardApproval
    def __init__(self, approval: _Optional[_Union[GuardApproval, _Mapping]] = ...) -> None: ...

class BatchSignProtectedActionItem(_message.Message):
    __slots__ = ("action", "args")
    ACTION_FIELD_NUMBER: _ClassVar[int]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    action: ProtectedAction
    args: ProtectedActionArgs
    def __init__(self, action: _Optional[_Union[ProtectedAction, str]] = ..., args: _Optional[_Union[ProtectedActionArgs, _Mapping]] = ...) -> None: ...

class BatchSignProtectedActionsRequest(_message.Message):
    __slots__ = ("subaccount_id", "actions")
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ACTIONS_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    actions: _containers.RepeatedCompositeFieldContainer[BatchSignProtectedActionItem]
    def __init__(self, subaccount_id: _Optional[int] = ..., actions: _Optional[_Iterable[_Union[BatchSignProtectedActionItem, _Mapping]]] = ...) -> None: ...

class BatchSignProtectedActionsResponse(_message.Message):
    __slots__ = ("approvals",)
    APPROVALS_FIELD_NUMBER: _ClassVar[int]
    approvals: _containers.RepeatedCompositeFieldContainer[GuardApproval]
    def __init__(self, approvals: _Optional[_Iterable[_Union[GuardApproval, _Mapping]]] = ...) -> None: ...

class RotateGuardSignerWalletRequest(_message.Message):
    __slots__ = ("subaccount_id",)
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    def __init__(self, subaccount_id: _Optional[int] = ...) -> None: ...

class RotateGuardSignerWalletResponse(_message.Message):
    __slots__ = ("new_signer_address", "approval")
    NEW_SIGNER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    APPROVAL_FIELD_NUMBER: _ClassVar[int]
    new_signer_address: str
    approval: GuardApproval
    def __init__(self, new_signer_address: _Optional[str] = ..., approval: _Optional[_Union[GuardApproval, _Mapping]] = ...) -> None: ...

class ExportGuardSignerWalletRequest(_message.Message):
    __slots__ = ("subaccount_id",)
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    def __init__(self, subaccount_id: _Optional[int] = ...) -> None: ...

class ExportGuardSignerWalletResponse(_message.Message):
    __slots__ = ("private_key",)
    PRIVATE_KEY_FIELD_NUMBER: _ClassVar[int]
    private_key: str
    def __init__(self, private_key: _Optional[str] = ...) -> None: ...
