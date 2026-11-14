import datetime

from polyester.gen.auth.v1 import auth_pb2 as _auth_pb2
from polyester.gen.buf.validate import validate_pb2 as _validate_pb2
from polyester.gen.gnostic.openapi.v3 import annotations_pb2 as _annotations_pb2
from polyester.gen.google.api import annotations_pb2 as _annotations_pb2_1
from polyester.gen.google.api import field_behavior_pb2 as _field_behavior_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from polyester.gen.polyester.api import options_pb2 as _options_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SocialProvider(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PROVIDER_UNSPECIFIED: _ClassVar[SocialProvider]
    TWITTER: _ClassVar[SocialProvider]
    DISCORD: _ClassVar[SocialProvider]

class SocialVerificationStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STATUS_UNSPECIFIED: _ClassVar[SocialVerificationStatus]
    STATUS_PENDING_USER_ACTION: _ClassVar[SocialVerificationStatus]
    STATUS_QUEUED: _ClassVar[SocialVerificationStatus]
    STATUS_IN_PROGRESS: _ClassVar[SocialVerificationStatus]
    STATUS_VERIFIED: _ClassVar[SocialVerificationStatus]
    STATUS_FAILED: _ClassVar[SocialVerificationStatus]
    STATUS_EXPIRED: _ClassVar[SocialVerificationStatus]
    STATUS_CANCELLED: _ClassVar[SocialVerificationStatus]

class SocialVerificationMethod(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    METHOD_UNSPECIFIED: _ClassVar[SocialVerificationMethod]
    METHOD_PROFILE: _ClassVar[SocialVerificationMethod]
    METHOD_CHANNEL: _ClassVar[SocialVerificationMethod]
    METHOD_DM: _ClassVar[SocialVerificationMethod]
PROVIDER_UNSPECIFIED: SocialProvider
TWITTER: SocialProvider
DISCORD: SocialProvider
STATUS_UNSPECIFIED: SocialVerificationStatus
STATUS_PENDING_USER_ACTION: SocialVerificationStatus
STATUS_QUEUED: SocialVerificationStatus
STATUS_IN_PROGRESS: SocialVerificationStatus
STATUS_VERIFIED: SocialVerificationStatus
STATUS_FAILED: SocialVerificationStatus
STATUS_EXPIRED: SocialVerificationStatus
STATUS_CANCELLED: SocialVerificationStatus
METHOD_UNSPECIFIED: SocialVerificationMethod
METHOD_PROFILE: SocialVerificationMethod
METHOD_CHANNEL: SocialVerificationMethod
METHOD_DM: SocialVerificationMethod

class SocialVerification(_message.Message):
    __slots__ = ("id", "provider", "method", "handle", "provider_user_id", "challenge_code", "status", "requested_at", "expires_at", "verified_at", "attempts", "last_error", "error_code", "updated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    METHOD_FIELD_NUMBER: _ClassVar[int]
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_USER_ID_FIELD_NUMBER: _ClassVar[int]
    CHALLENGE_CODE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    REQUESTED_AT_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    VERIFIED_AT_FIELD_NUMBER: _ClassVar[int]
    ATTEMPTS_FIELD_NUMBER: _ClassVar[int]
    LAST_ERROR_FIELD_NUMBER: _ClassVar[int]
    ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: int
    provider: SocialProvider
    method: SocialVerificationMethod
    handle: str
    provider_user_id: str
    challenge_code: str
    status: SocialVerificationStatus
    requested_at: _timestamp_pb2.Timestamp
    expires_at: _timestamp_pb2.Timestamp
    verified_at: _timestamp_pb2.Timestamp
    attempts: int
    last_error: str
    error_code: _auth_pb2.AuthErrorCode
    updated_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[int] = ..., provider: _Optional[_Union[SocialProvider, str]] = ..., method: _Optional[_Union[SocialVerificationMethod, str]] = ..., handle: _Optional[str] = ..., provider_user_id: _Optional[str] = ..., challenge_code: _Optional[str] = ..., status: _Optional[_Union[SocialVerificationStatus, str]] = ..., requested_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., expires_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., verified_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., attempts: _Optional[int] = ..., last_error: _Optional[str] = ..., error_code: _Optional[_Union[_auth_pb2.AuthErrorCode, str]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class StartSocialVerificationRequest(_message.Message):
    __slots__ = ("provider", "method", "handle")
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    METHOD_FIELD_NUMBER: _ClassVar[int]
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    provider: SocialProvider
    method: SocialVerificationMethod
    handle: str
    def __init__(self, provider: _Optional[_Union[SocialProvider, str]] = ..., method: _Optional[_Union[SocialVerificationMethod, str]] = ..., handle: _Optional[str] = ...) -> None: ...

class StartSocialVerificationResponse(_message.Message):
    __slots__ = ("challenge_code", "expires_at", "verification")
    CHALLENGE_CODE_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    VERIFICATION_FIELD_NUMBER: _ClassVar[int]
    challenge_code: str
    expires_at: _timestamp_pb2.Timestamp
    verification: SocialVerification
    def __init__(self, challenge_code: _Optional[str] = ..., expires_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., verification: _Optional[_Union[SocialVerification, _Mapping]] = ...) -> None: ...

class SocialVerificationReadyRequest(_message.Message):
    __slots__ = ("provider",)
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    provider: SocialProvider
    def __init__(self, provider: _Optional[_Union[SocialProvider, str]] = ...) -> None: ...

class SocialVerificationReadyResponse(_message.Message):
    __slots__ = ("verification",)
    VERIFICATION_FIELD_NUMBER: _ClassVar[int]
    verification: SocialVerification
    def __init__(self, verification: _Optional[_Union[SocialVerification, _Mapping]] = ...) -> None: ...

class GetSocialVerificationRequest(_message.Message):
    __slots__ = ("provider",)
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    provider: SocialProvider
    def __init__(self, provider: _Optional[_Union[SocialProvider, str]] = ...) -> None: ...

class GetSocialVerificationResponse(_message.Message):
    __slots__ = ("verification",)
    VERIFICATION_FIELD_NUMBER: _ClassVar[int]
    verification: SocialVerification
    def __init__(self, verification: _Optional[_Union[SocialVerification, _Mapping]] = ...) -> None: ...
