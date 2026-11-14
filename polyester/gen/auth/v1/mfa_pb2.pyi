import datetime

from polyester.gen.buf.validate import validate_pb2 as _validate_pb2
from polyester.gen.gnostic.openapi.v3 import annotations_pb2 as _annotations_pb2
from polyester.gen.google.api import annotations_pb2 as _annotations_pb2_1
from polyester.gen.google.api import field_behavior_pb2 as _field_behavior_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from polyester.gen.polyester.api import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SessionLevel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SESSION_LEVEL_UNSPECIFIED: _ClassVar[SessionLevel]
    PRIMARY_AUTHENTICATED: _ClassVar[SessionLevel]
    MFA_ELEVATED: _ClassVar[SessionLevel]
    FRESH_STEP_UP: _ClassVar[SessionLevel]

class MFAFactorType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MFA_FACTOR_TYPE_UNSPECIFIED: _ClassVar[MFAFactorType]
    MFA_FACTOR_TYPE_TOTP: _ClassVar[MFAFactorType]
    MFA_FACTOR_TYPE_PASSKEY: _ClassVar[MFAFactorType]
    MFA_FACTOR_TYPE_RECOVERY_CODE: _ClassVar[MFAFactorType]

class MFAChallengePurpose(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MFA_CHALLENGE_PURPOSE_UNSPECIFIED: _ClassVar[MFAChallengePurpose]
    MFA_CHALLENGE_PURPOSE_SESSION_ELEVATION: _ClassVar[MFAChallengePurpose]
    MFA_CHALLENGE_PURPOSE_FRESH_STEP_UP: _ClassVar[MFAChallengePurpose]
SESSION_LEVEL_UNSPECIFIED: SessionLevel
PRIMARY_AUTHENTICATED: SessionLevel
MFA_ELEVATED: SessionLevel
FRESH_STEP_UP: SessionLevel
MFA_FACTOR_TYPE_UNSPECIFIED: MFAFactorType
MFA_FACTOR_TYPE_TOTP: MFAFactorType
MFA_FACTOR_TYPE_PASSKEY: MFAFactorType
MFA_FACTOR_TYPE_RECOVERY_CODE: MFAFactorType
MFA_CHALLENGE_PURPOSE_UNSPECIFIED: MFAChallengePurpose
MFA_CHALLENGE_PURPOSE_SESSION_ELEVATION: MFAChallengePurpose
MFA_CHALLENGE_PURPOSE_FRESH_STEP_UP: MFAChallengePurpose

class SessionInfo(_message.Message):
    __slots__ = ("session_id", "session_level", "authentication_methods", "auth_time")
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    SESSION_LEVEL_FIELD_NUMBER: _ClassVar[int]
    AUTHENTICATION_METHODS_FIELD_NUMBER: _ClassVar[int]
    AUTH_TIME_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    session_level: SessionLevel
    authentication_methods: _containers.RepeatedScalarFieldContainer[str]
    auth_time: _timestamp_pb2.Timestamp
    def __init__(self, session_id: _Optional[str] = ..., session_level: _Optional[_Union[SessionLevel, str]] = ..., authentication_methods: _Optional[_Iterable[str]] = ..., auth_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class MFAFactor(_message.Message):
    __slots__ = ("factor_id", "factor_type", "label", "created_at", "last_used_at")
    FACTOR_ID_FIELD_NUMBER: _ClassVar[int]
    FACTOR_TYPE_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    LAST_USED_AT_FIELD_NUMBER: _ClassVar[int]
    factor_id: str
    factor_type: MFAFactorType
    label: str
    created_at: _timestamp_pb2.Timestamp
    last_used_at: _timestamp_pb2.Timestamp
    def __init__(self, factor_id: _Optional[str] = ..., factor_type: _Optional[_Union[MFAFactorType, str]] = ..., label: _Optional[str] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., last_used_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ListMFAFactorsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListMFAFactorsResponse(_message.Message):
    __slots__ = ("factors", "has_recovery_codes")
    FACTORS_FIELD_NUMBER: _ClassVar[int]
    HAS_RECOVERY_CODES_FIELD_NUMBER: _ClassVar[int]
    factors: _containers.RepeatedCompositeFieldContainer[MFAFactor]
    has_recovery_codes: bool
    def __init__(self, factors: _Optional[_Iterable[_Union[MFAFactor, _Mapping]]] = ..., has_recovery_codes: _Optional[bool] = ...) -> None: ...

class BeginTOTPEnrollmentRequest(_message.Message):
    __slots__ = ("label",)
    LABEL_FIELD_NUMBER: _ClassVar[int]
    label: str
    def __init__(self, label: _Optional[str] = ...) -> None: ...

class BeginTOTPEnrollmentResponse(_message.Message):
    __slots__ = ("enrollment_id", "secret", "otpauth_uri", "expires_at")
    ENROLLMENT_ID_FIELD_NUMBER: _ClassVar[int]
    SECRET_FIELD_NUMBER: _ClassVar[int]
    OTPAUTH_URI_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    enrollment_id: str
    secret: str
    otpauth_uri: str
    expires_at: _timestamp_pb2.Timestamp
    def __init__(self, enrollment_id: _Optional[str] = ..., secret: _Optional[str] = ..., otpauth_uri: _Optional[str] = ..., expires_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class FinishTOTPEnrollmentRequest(_message.Message):
    __slots__ = ("enrollment_id", "code")
    ENROLLMENT_ID_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    enrollment_id: str
    code: str
    def __init__(self, enrollment_id: _Optional[str] = ..., code: _Optional[str] = ...) -> None: ...

class FinishTOTPEnrollmentResponse(_message.Message):
    __slots__ = ("factor", "recovery_codes", "session", "access_token", "access_token_expires_at")
    FACTOR_FIELD_NUMBER: _ClassVar[int]
    RECOVERY_CODES_FIELD_NUMBER: _ClassVar[int]
    SESSION_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    factor: MFAFactor
    recovery_codes: _containers.RepeatedScalarFieldContainer[str]
    session: SessionInfo
    access_token: str
    access_token_expires_at: _timestamp_pb2.Timestamp
    def __init__(self, factor: _Optional[_Union[MFAFactor, _Mapping]] = ..., recovery_codes: _Optional[_Iterable[str]] = ..., session: _Optional[_Union[SessionInfo, _Mapping]] = ..., access_token: _Optional[str] = ..., access_token_expires_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class BeginPasskeyEnrollmentRequest(_message.Message):
    __slots__ = ("label",)
    LABEL_FIELD_NUMBER: _ClassVar[int]
    label: str
    def __init__(self, label: _Optional[str] = ...) -> None: ...

class BeginPasskeyEnrollmentResponse(_message.Message):
    __slots__ = ("enrollment_id", "public_key", "expires_at")
    ENROLLMENT_ID_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_KEY_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    enrollment_id: str
    public_key: _struct_pb2.Struct
    expires_at: _timestamp_pb2.Timestamp
    def __init__(self, enrollment_id: _Optional[str] = ..., public_key: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., expires_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class FinishPasskeyEnrollmentRequest(_message.Message):
    __slots__ = ("enrollment_id", "credential")
    ENROLLMENT_ID_FIELD_NUMBER: _ClassVar[int]
    CREDENTIAL_FIELD_NUMBER: _ClassVar[int]
    enrollment_id: str
    credential: _struct_pb2.Struct
    def __init__(self, enrollment_id: _Optional[str] = ..., credential: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class FinishPasskeyEnrollmentResponse(_message.Message):
    __slots__ = ("factor", "recovery_codes", "session", "access_token", "access_token_expires_at")
    FACTOR_FIELD_NUMBER: _ClassVar[int]
    RECOVERY_CODES_FIELD_NUMBER: _ClassVar[int]
    SESSION_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    factor: MFAFactor
    recovery_codes: _containers.RepeatedScalarFieldContainer[str]
    session: SessionInfo
    access_token: str
    access_token_expires_at: _timestamp_pb2.Timestamp
    def __init__(self, factor: _Optional[_Union[MFAFactor, _Mapping]] = ..., recovery_codes: _Optional[_Iterable[str]] = ..., session: _Optional[_Union[SessionInfo, _Mapping]] = ..., access_token: _Optional[str] = ..., access_token_expires_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class BeginMFAChallengeRequest(_message.Message):
    __slots__ = ("purpose",)
    PURPOSE_FIELD_NUMBER: _ClassVar[int]
    purpose: MFAChallengePurpose
    def __init__(self, purpose: _Optional[_Union[MFAChallengePurpose, str]] = ...) -> None: ...

class BeginMFAChallengeResponse(_message.Message):
    __slots__ = ("challenge_id", "allowed_factor_types", "public_key", "expires_at")
    CHALLENGE_ID_FIELD_NUMBER: _ClassVar[int]
    ALLOWED_FACTOR_TYPES_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_KEY_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    challenge_id: str
    allowed_factor_types: _containers.RepeatedScalarFieldContainer[MFAFactorType]
    public_key: _struct_pb2.Struct
    expires_at: _timestamp_pb2.Timestamp
    def __init__(self, challenge_id: _Optional[str] = ..., allowed_factor_types: _Optional[_Iterable[_Union[MFAFactorType, str]]] = ..., public_key: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., expires_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class VerifyTOTPChallengeRequest(_message.Message):
    __slots__ = ("challenge_id", "code")
    CHALLENGE_ID_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    challenge_id: str
    code: str
    def __init__(self, challenge_id: _Optional[str] = ..., code: _Optional[str] = ...) -> None: ...

class FinishPasskeyChallengeRequest(_message.Message):
    __slots__ = ("challenge_id", "credential")
    CHALLENGE_ID_FIELD_NUMBER: _ClassVar[int]
    CREDENTIAL_FIELD_NUMBER: _ClassVar[int]
    challenge_id: str
    credential: _struct_pb2.Struct
    def __init__(self, challenge_id: _Optional[str] = ..., credential: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class VerifyRecoveryCodeChallengeRequest(_message.Message):
    __slots__ = ("challenge_id", "recovery_code")
    CHALLENGE_ID_FIELD_NUMBER: _ClassVar[int]
    RECOVERY_CODE_FIELD_NUMBER: _ClassVar[int]
    challenge_id: str
    recovery_code: str
    def __init__(self, challenge_id: _Optional[str] = ..., recovery_code: _Optional[str] = ...) -> None: ...

class CompleteMFAChallengeResponse(_message.Message):
    __slots__ = ("session", "access_token", "access_token_expires_at", "step_up_token", "step_up_expires_at")
    SESSION_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    STEP_UP_TOKEN_FIELD_NUMBER: _ClassVar[int]
    STEP_UP_EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    session: SessionInfo
    access_token: str
    access_token_expires_at: _timestamp_pb2.Timestamp
    step_up_token: str
    step_up_expires_at: _timestamp_pb2.Timestamp
    def __init__(self, session: _Optional[_Union[SessionInfo, _Mapping]] = ..., access_token: _Optional[str] = ..., access_token_expires_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., step_up_token: _Optional[str] = ..., step_up_expires_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ClaimFreshStepUpRequest(_message.Message):
    __slots__ = ("request_id", "action_type", "subject")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    ACTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    action_type: str
    subject: str
    def __init__(self, request_id: _Optional[str] = ..., action_type: _Optional[str] = ..., subject: _Optional[str] = ...) -> None: ...

class ClaimFreshStepUpResponse(_message.Message):
    __slots__ = ("step_up_id", "claim_nonce", "claim_expires_at")
    STEP_UP_ID_FIELD_NUMBER: _ClassVar[int]
    CLAIM_NONCE_FIELD_NUMBER: _ClassVar[int]
    CLAIM_EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    step_up_id: str
    claim_nonce: str
    claim_expires_at: _timestamp_pb2.Timestamp
    def __init__(self, step_up_id: _Optional[str] = ..., claim_nonce: _Optional[str] = ..., claim_expires_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ConsumeFreshStepUpRequest(_message.Message):
    __slots__ = ("step_up_id", "request_id", "action_type", "subject", "claim_nonce")
    STEP_UP_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    ACTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    CLAIM_NONCE_FIELD_NUMBER: _ClassVar[int]
    step_up_id: str
    request_id: str
    action_type: str
    subject: str
    claim_nonce: str
    def __init__(self, step_up_id: _Optional[str] = ..., request_id: _Optional[str] = ..., action_type: _Optional[str] = ..., subject: _Optional[str] = ..., claim_nonce: _Optional[str] = ...) -> None: ...

class ConsumeFreshStepUpResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ReleaseFreshStepUpRequest(_message.Message):
    __slots__ = ("step_up_id", "request_id", "action_type", "subject", "claim_nonce", "reason")
    STEP_UP_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    ACTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    CLAIM_NONCE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    step_up_id: str
    request_id: str
    action_type: str
    subject: str
    claim_nonce: str
    reason: str
    def __init__(self, step_up_id: _Optional[str] = ..., request_id: _Optional[str] = ..., action_type: _Optional[str] = ..., subject: _Optional[str] = ..., claim_nonce: _Optional[str] = ..., reason: _Optional[str] = ...) -> None: ...

class ReleaseFreshStepUpResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class UpdateMFAFactorRequest(_message.Message):
    __slots__ = ("factor_id", "label")
    FACTOR_ID_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    factor_id: str
    label: str
    def __init__(self, factor_id: _Optional[str] = ..., label: _Optional[str] = ...) -> None: ...

class UpdateMFAFactorResponse(_message.Message):
    __slots__ = ("factor",)
    FACTOR_FIELD_NUMBER: _ClassVar[int]
    factor: MFAFactor
    def __init__(self, factor: _Optional[_Union[MFAFactor, _Mapping]] = ...) -> None: ...

class DeleteMFAFactorRequest(_message.Message):
    __slots__ = ("factor_id",)
    FACTOR_ID_FIELD_NUMBER: _ClassVar[int]
    factor_id: str
    def __init__(self, factor_id: _Optional[str] = ...) -> None: ...

class DeleteMFAFactorResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class RegenerateRecoveryCodesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class RegenerateRecoveryCodesResponse(_message.Message):
    __slots__ = ("recovery_codes",)
    RECOVERY_CODES_FIELD_NUMBER: _ClassVar[int]
    recovery_codes: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, recovery_codes: _Optional[_Iterable[str]] = ...) -> None: ...
