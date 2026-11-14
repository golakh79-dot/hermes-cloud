import datetime

from polyester.gen.buf.validate import validate_pb2 as _validate_pb2
from polyester.gen.gnostic.openapi.v3 import annotations_pb2 as _annotations_pb2
from polyester.gen.google.api import annotations_pb2 as _annotations_pb2_1
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

class ErrorCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ERROR_CODE_UNSPECIFIED: _ClassVar[ErrorCode]
    ERROR_CODE_CLAIM_TEMPORARILY_UNAVAILABLE: _ClassVar[ErrorCode]
    ERROR_CODE_UNAUTHENTICATED: _ClassVar[ErrorCode]
    ERROR_CODE_RATE_LIMIT_EXCEEDED: _ClassVar[ErrorCode]
    ERROR_CODE_CLAIM_UNAVAILABLE: _ClassVar[ErrorCode]
    ERROR_CODE_CONFLICT: _ClassVar[ErrorCode]
    ERROR_CODE_INVALID_REQUEST: _ClassVar[ErrorCode]
    ERROR_CODE_REQUEST_TOO_LARGE: _ClassVar[ErrorCode]
    ERROR_CODE_SERVICE_UNAVAILABLE: _ClassVar[ErrorCode]
    ERROR_CODE_INTERNAL_ERROR: _ClassVar[ErrorCode]
    ERROR_CODE_PERMISSION_DENIED: _ClassVar[ErrorCode]
    ERROR_CODE_FAILED_PRECONDITION: _ClassVar[ErrorCode]
    ERROR_CODE_SOCIAL_VERIFICATION_REQUIRED: _ClassVar[ErrorCode]
    ERROR_CODE_SUBACCOUNT_NOT_FOUND: _ClassVar[ErrorCode]
    ERROR_CODE_SUBACCOUNT_INACTIVE: _ClassVar[ErrorCode]
    ERROR_CODE_CLAIM_PAYOUT_UNAVAILABLE: _ClassVar[ErrorCode]

class ClaimPolicy(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    POLICY_UNSPECIFIED: _ClassVar[ClaimPolicy]
    UTC_DAILY: _ClassVar[ClaimPolicy]

class DailyClaimState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CLAIM_UNSPECIFIED: _ClassVar[DailyClaimState]
    CLAIM_AVAILABLE: _ClassVar[DailyClaimState]
    CLAIM_PROCESSING: _ClassVar[DailyClaimState]
    CLAIM_CLAIMED: _ClassVar[DailyClaimState]
    CLAIM_UNAVAILABLE: _ClassVar[DailyClaimState]
    CLAIM_PAYOUT_DELAYED: _ClassVar[DailyClaimState]
ERROR_CODE_UNSPECIFIED: ErrorCode
ERROR_CODE_CLAIM_TEMPORARILY_UNAVAILABLE: ErrorCode
ERROR_CODE_UNAUTHENTICATED: ErrorCode
ERROR_CODE_RATE_LIMIT_EXCEEDED: ErrorCode
ERROR_CODE_CLAIM_UNAVAILABLE: ErrorCode
ERROR_CODE_CONFLICT: ErrorCode
ERROR_CODE_INVALID_REQUEST: ErrorCode
ERROR_CODE_REQUEST_TOO_LARGE: ErrorCode
ERROR_CODE_SERVICE_UNAVAILABLE: ErrorCode
ERROR_CODE_INTERNAL_ERROR: ErrorCode
ERROR_CODE_PERMISSION_DENIED: ErrorCode
ERROR_CODE_FAILED_PRECONDITION: ErrorCode
ERROR_CODE_SOCIAL_VERIFICATION_REQUIRED: ErrorCode
ERROR_CODE_SUBACCOUNT_NOT_FOUND: ErrorCode
ERROR_CODE_SUBACCOUNT_INACTIVE: ErrorCode
ERROR_CODE_CLAIM_PAYOUT_UNAVAILABLE: ErrorCode
POLICY_UNSPECIFIED: ClaimPolicy
UTC_DAILY: ClaimPolicy
CLAIM_UNSPECIFIED: DailyClaimState
CLAIM_AVAILABLE: DailyClaimState
CLAIM_PROCESSING: DailyClaimState
CLAIM_CLAIMED: DailyClaimState
CLAIM_UNAVAILABLE: DailyClaimState
CLAIM_PAYOUT_DELAYED: DailyClaimState

class ErrorDetail(_message.Message):
    __slots__ = ("code",)
    CODE_FIELD_NUMBER: _ClassVar[int]
    code: ErrorCode
    def __init__(self, code: _Optional[_Union[ErrorCode, str]] = ...) -> None: ...

class ClaimCampaign(_message.Message):
    __slots__ = ("campaign_id", "name", "description", "claim_policy")
    CAMPAIGN_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CLAIM_POLICY_FIELD_NUMBER: _ClassVar[int]
    campaign_id: str
    name: str
    description: str
    claim_policy: ClaimPolicy
    def __init__(self, campaign_id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., claim_policy: _Optional[_Union[ClaimPolicy, str]] = ...) -> None: ...

class DailyClaimReward(_message.Message):
    __slots__ = ("asset_id", "asset_code", "amount_e18")
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    ASSET_CODE_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_E18_FIELD_NUMBER: _ClassVar[int]
    asset_id: int
    asset_code: str
    amount_e18: _u128_pb2.U128
    def __init__(self, asset_id: _Optional[int] = ..., asset_code: _Optional[str] = ..., amount_e18: _Optional[_Union[_u128_pb2.U128, _Mapping]] = ...) -> None: ...

class GetDailyClaimStatusRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetDailyClaimStatusResponse(_message.Message):
    __slots__ = ("state", "reset_at", "rewards", "claim_id", "campaign", "subaccount_id", "payout_delay_reason")
    STATE_FIELD_NUMBER: _ClassVar[int]
    RESET_AT_FIELD_NUMBER: _ClassVar[int]
    REWARDS_FIELD_NUMBER: _ClassVar[int]
    CLAIM_ID_FIELD_NUMBER: _ClassVar[int]
    CAMPAIGN_FIELD_NUMBER: _ClassVar[int]
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    PAYOUT_DELAY_REASON_FIELD_NUMBER: _ClassVar[int]
    state: DailyClaimState
    reset_at: _timestamp_pb2.Timestamp
    rewards: _containers.RepeatedCompositeFieldContainer[DailyClaimReward]
    claim_id: str
    campaign: ClaimCampaign
    subaccount_id: int
    payout_delay_reason: ErrorCode
    def __init__(self, state: _Optional[_Union[DailyClaimState, str]] = ..., reset_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., rewards: _Optional[_Iterable[_Union[DailyClaimReward, _Mapping]]] = ..., claim_id: _Optional[str] = ..., campaign: _Optional[_Union[ClaimCampaign, _Mapping]] = ..., subaccount_id: _Optional[int] = ..., payout_delay_reason: _Optional[_Union[ErrorCode, str]] = ...) -> None: ...

class ClaimDailyRewardRequest(_message.Message):
    __slots__ = ("subaccount_id",)
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    def __init__(self, subaccount_id: _Optional[int] = ...) -> None: ...

class DailyClaimTransfer(_message.Message):
    __slots__ = ("asset_id", "transfer_id")
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    TRANSFER_ID_FIELD_NUMBER: _ClassVar[int]
    asset_id: int
    transfer_id: str
    def __init__(self, asset_id: _Optional[int] = ..., transfer_id: _Optional[str] = ...) -> None: ...

class ClaimDailyRewardResponse(_message.Message):
    __slots__ = ("claim_id", "state", "claimed_at", "rewards", "transfers", "reset_at", "campaign", "subaccount_id")
    CLAIM_ID_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    CLAIMED_AT_FIELD_NUMBER: _ClassVar[int]
    REWARDS_FIELD_NUMBER: _ClassVar[int]
    TRANSFERS_FIELD_NUMBER: _ClassVar[int]
    RESET_AT_FIELD_NUMBER: _ClassVar[int]
    CAMPAIGN_FIELD_NUMBER: _ClassVar[int]
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    claim_id: str
    state: DailyClaimState
    claimed_at: _timestamp_pb2.Timestamp
    rewards: _containers.RepeatedCompositeFieldContainer[DailyClaimReward]
    transfers: _containers.RepeatedCompositeFieldContainer[DailyClaimTransfer]
    reset_at: _timestamp_pb2.Timestamp
    campaign: ClaimCampaign
    subaccount_id: int
    def __init__(self, claim_id: _Optional[str] = ..., state: _Optional[_Union[DailyClaimState, str]] = ..., claimed_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., rewards: _Optional[_Iterable[_Union[DailyClaimReward, _Mapping]]] = ..., transfers: _Optional[_Iterable[_Union[DailyClaimTransfer, _Mapping]]] = ..., reset_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., campaign: _Optional[_Union[ClaimCampaign, _Mapping]] = ..., subaccount_id: _Optional[int] = ...) -> None: ...
