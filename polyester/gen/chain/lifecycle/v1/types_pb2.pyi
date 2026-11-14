from polyester.gen.polyester.type.v1 import u128_pb2 as _u128_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RequestFeeStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    REQUEST_FEE_STATUS_UNSPECIFIED: _ClassVar[RequestFeeStatus]
    REQUEST_FEE_STATUS_LOCKED: _ClassVar[RequestFeeStatus]
    REQUEST_FEE_STATUS_SETTLED: _ClassVar[RequestFeeStatus]

class LifecycleReason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    REASON_UNSPECIFIED: _ClassVar[LifecycleReason]
    ZIPPER_VALIDATION_REJECTED: _ClassVar[LifecycleReason]
    ZIPPER_EXECUTION_REJECTED: _ClassVar[LifecycleReason]
    ZIPPER_WITHDRAW_EXECUTION_FAILED: _ClassVar[LifecycleReason]
    ZIPPER_DEPOSIT_REFUND_FAILED: _ClassVar[LifecycleReason]
    LEDGER_MIRROR_REJECTED: _ClassVar[LifecycleReason]
    LEDGER_MIRROR_TRANSFER_EXCEEDS_CREDITS: _ClassVar[LifecycleReason]
    LEDGER_MIRROR_TRANSFER_EXISTS: _ClassVar[LifecycleReason]
    LEDGER_MIRROR_PENDING_TRANSFER_NOT_FOUND: _ClassVar[LifecycleReason]
    LEDGER_MIRROR_TRANSFER_ID_ALREADY_FAILED: _ClassVar[LifecycleReason]
    TRADING_WITHDRAW_POLICY_DENIED: _ClassVar[LifecycleReason]
    TRADING_WITHDRAW_CONTRACT_REVERTED: _ClassVar[LifecycleReason]
    TRADING_WITHDRAW_EXECUTION_FAILED: _ClassVar[LifecycleReason]
    DEPOSIT_SOURCE_NOT_CONFIRMED: _ClassVar[LifecycleReason]

class FlowKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    KIND_UNSPECIFIED: _ClassVar[FlowKind]
    KIND_DEPOSIT: _ClassVar[FlowKind]
    KIND_WITHDRAW: _ClassVar[FlowKind]
    KIND_TRANSFER: _ClassVar[FlowKind]

class FlowDomain(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DOMAIN_UNSPECIFIED: _ClassVar[FlowDomain]
    DOMAIN_EXTERNAL_CHAIN: _ClassVar[FlowDomain]
    DOMAIN_ZIPPER: _ClassVar[FlowDomain]
    DOMAIN_FUNDING: _ClassVar[FlowDomain]
    DOMAIN_TRADING: _ClassVar[FlowDomain]
    DOMAIN_LENDING: _ClassVar[FlowDomain]

class LifecycleSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SOURCE_UNSPECIFIED: _ClassVar[LifecycleSource]
    SOURCE_RELAYER: _ClassVar[LifecycleSource]
    SOURCE_POLYESTER_CHAIN: _ClassVar[LifecycleSource]
    SOURCE_EXECUTOR: _ClassVar[LifecycleSource]
    SOURCE_LEDGER: _ClassVar[LifecycleSource]
    SOURCE_LIFECYCLE: _ClassVar[LifecycleSource]

class FlowState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STATE_UNSPECIFIED: _ClassVar[FlowState]
    STATE_PENDING_SOURCE: _ClassVar[FlowState]
    STATE_PENDING_POLYESTER_CHAIN: _ClassVar[FlowState]
    STATE_PENDING_LEDGER: _ClassVar[FlowState]
    STATE_COMPLETED: _ClassVar[FlowState]
    STATE_FAILED: _ClassVar[FlowState]
    STATE_DROPPED: _ClassVar[FlowState]
    STATE_REFUNDED: _ClassVar[FlowState]
REQUEST_FEE_STATUS_UNSPECIFIED: RequestFeeStatus
REQUEST_FEE_STATUS_LOCKED: RequestFeeStatus
REQUEST_FEE_STATUS_SETTLED: RequestFeeStatus
REASON_UNSPECIFIED: LifecycleReason
ZIPPER_VALIDATION_REJECTED: LifecycleReason
ZIPPER_EXECUTION_REJECTED: LifecycleReason
ZIPPER_WITHDRAW_EXECUTION_FAILED: LifecycleReason
ZIPPER_DEPOSIT_REFUND_FAILED: LifecycleReason
LEDGER_MIRROR_REJECTED: LifecycleReason
LEDGER_MIRROR_TRANSFER_EXCEEDS_CREDITS: LifecycleReason
LEDGER_MIRROR_TRANSFER_EXISTS: LifecycleReason
LEDGER_MIRROR_PENDING_TRANSFER_NOT_FOUND: LifecycleReason
LEDGER_MIRROR_TRANSFER_ID_ALREADY_FAILED: LifecycleReason
TRADING_WITHDRAW_POLICY_DENIED: LifecycleReason
TRADING_WITHDRAW_CONTRACT_REVERTED: LifecycleReason
TRADING_WITHDRAW_EXECUTION_FAILED: LifecycleReason
DEPOSIT_SOURCE_NOT_CONFIRMED: LifecycleReason
KIND_UNSPECIFIED: FlowKind
KIND_DEPOSIT: FlowKind
KIND_WITHDRAW: FlowKind
KIND_TRANSFER: FlowKind
DOMAIN_UNSPECIFIED: FlowDomain
DOMAIN_EXTERNAL_CHAIN: FlowDomain
DOMAIN_ZIPPER: FlowDomain
DOMAIN_FUNDING: FlowDomain
DOMAIN_TRADING: FlowDomain
DOMAIN_LENDING: FlowDomain
SOURCE_UNSPECIFIED: LifecycleSource
SOURCE_RELAYER: LifecycleSource
SOURCE_POLYESTER_CHAIN: LifecycleSource
SOURCE_EXECUTOR: LifecycleSource
SOURCE_LEDGER: LifecycleSource
SOURCE_LIFECYCLE: LifecycleSource
STATE_UNSPECIFIED: FlowState
STATE_PENDING_SOURCE: FlowState
STATE_PENDING_POLYESTER_CHAIN: FlowState
STATE_PENDING_LEDGER: FlowState
STATE_COMPLETED: FlowState
STATE_FAILED: FlowState
STATE_DROPPED: FlowState
STATE_REFUNDED: FlowState

class AssetIds(_message.Message):
    __slots__ = ("zipped_asset_id", "unified_asset_id")
    ZIPPED_ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    UNIFIED_ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    zipped_asset_id: int
    unified_asset_id: int
    def __init__(self, zipped_asset_id: _Optional[int] = ..., unified_asset_id: _Optional[int] = ...) -> None: ...

class RequestFee(_message.Message):
    __slots__ = ("asset_ids", "amount_e18", "recipient_address", "status")
    ASSET_IDS_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_E18_FIELD_NUMBER: _ClassVar[int]
    RECIPIENT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    asset_ids: AssetIds
    amount_e18: _u128_pb2.U128
    recipient_address: str
    status: RequestFeeStatus
    def __init__(self, asset_ids: _Optional[_Union[AssetIds, _Mapping]] = ..., amount_e18: _Optional[_Union[_u128_pb2.U128, _Mapping]] = ..., recipient_address: _Optional[str] = ..., status: _Optional[_Union[RequestFeeStatus, str]] = ...) -> None: ...
