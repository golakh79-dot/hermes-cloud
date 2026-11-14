from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FailureReason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    REASON_UNSPECIFIED: _ClassVar[FailureReason]
    QUOTA_EXCEEDED: _ClassVar[FailureReason]
    AUTHORITY_UNAVAILABLE: _ClassVar[FailureReason]

class PolicyClass(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CLASS_UNSPECIFIED: _ClassVar[PolicyClass]
    AUTH_PUBLIC: _ClassVar[PolicyClass]
    TRADING_PLACE: _ClassVar[PolicyClass]
    TRADING_CANCEL: _ClassVar[PolicyClass]
    TRADING_READ: _ClassVar[PolicyClass]
    ACCOUNT_ADMIN: _ClassVar[PolicyClass]
    PUBLIC_READ: _ClassVar[PolicyClass]
    ACCOUNT_SECURITY: _ClassVar[PolicyClass]
    DEPOSIT_CREATE: _ClassVar[PolicyClass]
    INTERNAL_TRANSFER: _ClassVar[PolicyClass]
    WITHDRAW_SUBMIT: _ClassVar[PolicyClass]
    WITHDRAW_VALIDATE: _ClassVar[PolicyClass]
    GUARD_SIGN: _ClassVar[PolicyClass]
    SOCIAL_PROVIDER: _ClassVar[PolicyClass]

class LimiterScope(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SCOPE_UNSPECIFIED: _ClassVar[LimiterScope]
    CLIENT_IP: _ClassVar[LimiterScope]
    API_KEY: _ClassVar[LimiterScope]
    ACCOUNT: _ClassVar[LimiterScope]
    SUBACCOUNT: _ClassVar[LimiterScope]
    CONNECTION: _ClassVar[LimiterScope]
    SERVICE: _ClassVar[LimiterScope]
    REGION: _ClassVar[LimiterScope]
    SYMBOL: _ClassVar[LimiterScope]
    AUTH_SUBJECT: _ClassVar[LimiterScope]

class RefillModel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    REFILL_UNSPECIFIED: _ClassVar[RefillModel]
    CONTINUOUS: _ClassVar[RefillModel]
    FIXED_WINDOW: _ClassVar[RefillModel]
    ROLLING_WINDOW: _ClassVar[RefillModel]
REASON_UNSPECIFIED: FailureReason
QUOTA_EXCEEDED: FailureReason
AUTHORITY_UNAVAILABLE: FailureReason
CLASS_UNSPECIFIED: PolicyClass
AUTH_PUBLIC: PolicyClass
TRADING_PLACE: PolicyClass
TRADING_CANCEL: PolicyClass
TRADING_READ: PolicyClass
ACCOUNT_ADMIN: PolicyClass
PUBLIC_READ: PolicyClass
ACCOUNT_SECURITY: PolicyClass
DEPOSIT_CREATE: PolicyClass
INTERNAL_TRANSFER: PolicyClass
WITHDRAW_SUBMIT: PolicyClass
WITHDRAW_VALIDATE: PolicyClass
GUARD_SIGN: PolicyClass
SOCIAL_PROVIDER: PolicyClass
SCOPE_UNSPECIFIED: LimiterScope
CLIENT_IP: LimiterScope
API_KEY: LimiterScope
ACCOUNT: LimiterScope
SUBACCOUNT: LimiterScope
CONNECTION: LimiterScope
SERVICE: LimiterScope
REGION: LimiterScope
SYMBOL: LimiterScope
AUTH_SUBJECT: LimiterScope
REFILL_UNSPECIFIED: RefillModel
CONTINUOUS: RefillModel
FIXED_WINDOW: RefillModel
ROLLING_WINDOW: RefillModel

class RateLimitDetail(_message.Message):
    __slots__ = ("reason", "limit", "remaining", "retry_after_ms", "policy_version", "operation_id", "policy_class", "scope", "refill_model")
    REASON_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    REMAINING_FIELD_NUMBER: _ClassVar[int]
    RETRY_AFTER_MS_FIELD_NUMBER: _ClassVar[int]
    POLICY_VERSION_FIELD_NUMBER: _ClassVar[int]
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    POLICY_CLASS_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    REFILL_MODEL_FIELD_NUMBER: _ClassVar[int]
    reason: FailureReason
    limit: int
    remaining: int
    retry_after_ms: int
    policy_version: int
    operation_id: str
    policy_class: PolicyClass
    scope: LimiterScope
    refill_model: RefillModel
    def __init__(self, reason: _Optional[_Union[FailureReason, str]] = ..., limit: _Optional[int] = ..., remaining: _Optional[int] = ..., retry_after_ms: _Optional[int] = ..., policy_version: _Optional[int] = ..., operation_id: _Optional[str] = ..., policy_class: _Optional[_Union[PolicyClass, str]] = ..., scope: _Optional[_Union[LimiterScope, str]] = ..., refill_model: _Optional[_Union[RefillModel, str]] = ...) -> None: ...
