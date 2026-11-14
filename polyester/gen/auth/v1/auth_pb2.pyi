import datetime

from polyester.gen.auth.v1 import mfa_pb2 as _mfa_pb2
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

class WalletChallengePurpose(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WALLET_PROOF_UNSPECIFIED: _ClassVar[WalletChallengePurpose]
    LOGIN: _ClassVar[WalletChallengePurpose]

class AuthErrorCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AUTH_UNSPECIFIED: _ClassVar[AuthErrorCode]
    AUTH_USERNAME_INVALID: _ClassVar[AuthErrorCode]
    AUTH_USERNAME_TAKEN: _ClassVar[AuthErrorCode]
    AUTH_USERNAME_COOLDOWN: _ClassVar[AuthErrorCode]
    AUTH_USERNAME_FEATURE_LOCKED: _ClassVar[AuthErrorCode]
    AUTH_USERNAME_RESERVED: _ClassVar[AuthErrorCode]
    AUTH_INVALID_REQUEST: _ClassVar[AuthErrorCode]
    AUTH_AUTHENTICATION_REQUIRED: _ClassVar[AuthErrorCode]
    AUTH_SESSION_KIND_NOT_ALLOWED: _ClassVar[AuthErrorCode]
    AUTH_WALLET_LOGIN_FAILED: _ClassVar[AuthErrorCode]
    AUTH_RESOURCE_NOT_FOUND: _ClassVar[AuthErrorCode]
    AUTH_SUBACCOUNT_ACCESS_DENIED: _ClassVar[AuthErrorCode]
    AUTH_API_KEY_ACCESS_DENIED: _ClassVar[AuthErrorCode]
    AUTH_API_KEY_INVALID_STATUS_TRANSITION: _ClassVar[AuthErrorCode]
    AUTH_POLICY_INVALID: _ClassVar[AuthErrorCode]
    AUTH_SMART_ACCOUNT_ALREADY_LINKED: _ClassVar[AuthErrorCode]
    AUTH_INVITE_ACCESS_DENIED: _ClassVar[AuthErrorCode]
    AUTH_INVITE_INVALID_STATE: _ClassVar[AuthErrorCode]
    AUTH_MFA_DISABLED: _ClassVar[AuthErrorCode]
    AUTH_MFA_NOT_ENROLLED: _ClassVar[AuthErrorCode]
    AUTH_MFA_SESSION_INVALID: _ClassVar[AuthErrorCode]
    AUTH_MFA_CHALLENGE_NOT_FOUND: _ClassVar[AuthErrorCode]
    AUTH_MFA_CHALLENGE_INVALID: _ClassVar[AuthErrorCode]
    AUTH_MFA_CHALLENGE_LOCKED: _ClassVar[AuthErrorCode]
    AUTH_MFA_OTP_INVALID: _ClassVar[AuthErrorCode]
    AUTH_MFA_RECOVERY_INVALID: _ClassVar[AuthErrorCode]
    AUTH_MFA_PASSKEY_NOT_AVAILABLE: _ClassVar[AuthErrorCode]
    AUTH_MFA_PASSKEY_CREDENTIAL_INVALID: _ClassVar[AuthErrorCode]
    AUTH_MFA_PASSKEY_VERIFY_FAILED: _ClassVar[AuthErrorCode]
    AUTH_MFA_ENROLLMENT_BINDING_INVALID: _ClassVar[AuthErrorCode]
    AUTH_STEP_UP_REQUIRED: _ClassVar[AuthErrorCode]
    AUTH_STEP_UP_PROOF_UNAVAILABLE: _ClassVar[AuthErrorCode]
    AUTH_STEP_UP_ALREADY_CLAIMED: _ClassVar[AuthErrorCode]
    AUTH_POLICY_IN_USE: _ClassVar[AuthErrorCode]
    AUTH_POLICY_LOCKED: _ClassVar[AuthErrorCode]
    AUTH_POLICY_SCOPE_MISMATCH: _ClassVar[AuthErrorCode]
    AUTH_REVISION_CONFLICT: _ClassVar[AuthErrorCode]
    AUTH_MFA_ELEVATION_REQUIRED: _ClassVar[AuthErrorCode]
    AUTH_MFA_LAST_FACTOR_REQUIRED: _ClassVar[AuthErrorCode]
    AUTH_INTERNAL_ERROR: _ClassVar[AuthErrorCode]
    AUTH_TERMS_NOT_ACCEPTED: _ClassVar[AuthErrorCode]
    AUTH_SOCIAL_VERIFICATION_EXPIRED: _ClassVar[AuthErrorCode]
    AUTH_SOCIAL_VERIFICATION_INVALID_STATE: _ClassVar[AuthErrorCode]
    AUTH_SUBACCOUNT_CHALLENGE_INVALID: _ClassVar[AuthErrorCode]
    AUTH_SOCIAL_ACCOUNT_ALREADY_LINKED: _ClassVar[AuthErrorCode]
    AUTH_TEMPORARILY_UNAVAILABLE: _ClassVar[AuthErrorCode]
    AUTH_SUBACCOUNT_OWNER_ROLE_LOCKED: _ClassVar[AuthErrorCode]
WALLET_PROOF_UNSPECIFIED: WalletChallengePurpose
LOGIN: WalletChallengePurpose
AUTH_UNSPECIFIED: AuthErrorCode
AUTH_USERNAME_INVALID: AuthErrorCode
AUTH_USERNAME_TAKEN: AuthErrorCode
AUTH_USERNAME_COOLDOWN: AuthErrorCode
AUTH_USERNAME_FEATURE_LOCKED: AuthErrorCode
AUTH_USERNAME_RESERVED: AuthErrorCode
AUTH_INVALID_REQUEST: AuthErrorCode
AUTH_AUTHENTICATION_REQUIRED: AuthErrorCode
AUTH_SESSION_KIND_NOT_ALLOWED: AuthErrorCode
AUTH_WALLET_LOGIN_FAILED: AuthErrorCode
AUTH_RESOURCE_NOT_FOUND: AuthErrorCode
AUTH_SUBACCOUNT_ACCESS_DENIED: AuthErrorCode
AUTH_API_KEY_ACCESS_DENIED: AuthErrorCode
AUTH_API_KEY_INVALID_STATUS_TRANSITION: AuthErrorCode
AUTH_POLICY_INVALID: AuthErrorCode
AUTH_SMART_ACCOUNT_ALREADY_LINKED: AuthErrorCode
AUTH_INVITE_ACCESS_DENIED: AuthErrorCode
AUTH_INVITE_INVALID_STATE: AuthErrorCode
AUTH_MFA_DISABLED: AuthErrorCode
AUTH_MFA_NOT_ENROLLED: AuthErrorCode
AUTH_MFA_SESSION_INVALID: AuthErrorCode
AUTH_MFA_CHALLENGE_NOT_FOUND: AuthErrorCode
AUTH_MFA_CHALLENGE_INVALID: AuthErrorCode
AUTH_MFA_CHALLENGE_LOCKED: AuthErrorCode
AUTH_MFA_OTP_INVALID: AuthErrorCode
AUTH_MFA_RECOVERY_INVALID: AuthErrorCode
AUTH_MFA_PASSKEY_NOT_AVAILABLE: AuthErrorCode
AUTH_MFA_PASSKEY_CREDENTIAL_INVALID: AuthErrorCode
AUTH_MFA_PASSKEY_VERIFY_FAILED: AuthErrorCode
AUTH_MFA_ENROLLMENT_BINDING_INVALID: AuthErrorCode
AUTH_STEP_UP_REQUIRED: AuthErrorCode
AUTH_STEP_UP_PROOF_UNAVAILABLE: AuthErrorCode
AUTH_STEP_UP_ALREADY_CLAIMED: AuthErrorCode
AUTH_POLICY_IN_USE: AuthErrorCode
AUTH_POLICY_LOCKED: AuthErrorCode
AUTH_POLICY_SCOPE_MISMATCH: AuthErrorCode
AUTH_REVISION_CONFLICT: AuthErrorCode
AUTH_MFA_ELEVATION_REQUIRED: AuthErrorCode
AUTH_MFA_LAST_FACTOR_REQUIRED: AuthErrorCode
AUTH_INTERNAL_ERROR: AuthErrorCode
AUTH_TERMS_NOT_ACCEPTED: AuthErrorCode
AUTH_SOCIAL_VERIFICATION_EXPIRED: AuthErrorCode
AUTH_SOCIAL_VERIFICATION_INVALID_STATE: AuthErrorCode
AUTH_SUBACCOUNT_CHALLENGE_INVALID: AuthErrorCode
AUTH_SOCIAL_ACCOUNT_ALREADY_LINKED: AuthErrorCode
AUTH_TEMPORARILY_UNAVAILABLE: AuthErrorCode
AUTH_SUBACCOUNT_OWNER_ROLE_LOCKED: AuthErrorCode

class CreateWalletChallengeRequest(_message.Message):
    __slots__ = ("smart_account_address", "signer_address", "uri", "purpose")
    SMART_ACCOUNT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    SIGNER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    URI_FIELD_NUMBER: _ClassVar[int]
    PURPOSE_FIELD_NUMBER: _ClassVar[int]
    smart_account_address: str
    signer_address: str
    uri: str
    purpose: WalletChallengePurpose
    def __init__(self, smart_account_address: _Optional[str] = ..., signer_address: _Optional[str] = ..., uri: _Optional[str] = ..., purpose: _Optional[_Union[WalletChallengePurpose, str]] = ...) -> None: ...

class CreateWalletChallengeResponse(_message.Message):
    __slots__ = ("message", "expires_at")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    message: str
    expires_at: _timestamp_pb2.Timestamp
    def __init__(self, message: _Optional[str] = ..., expires_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class LoginWithWalletRequest(_message.Message):
    __slots__ = ("smart_account_address", "signature", "user_agent", "ip", "wallet_provider", "message")
    SMART_ACCOUNT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    USER_AGENT_FIELD_NUMBER: _ClassVar[int]
    IP_FIELD_NUMBER: _ClassVar[int]
    WALLET_PROVIDER_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    smart_account_address: str
    signature: str
    user_agent: str
    ip: str
    wallet_provider: str
    message: str
    def __init__(self, smart_account_address: _Optional[str] = ..., signature: _Optional[str] = ..., user_agent: _Optional[str] = ..., ip: _Optional[str] = ..., wallet_provider: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class LoginWithWalletResponse(_message.Message):
    __slots__ = ("access_token", "expires_at", "account_id", "username", "session")
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    SESSION_FIELD_NUMBER: _ClassVar[int]
    access_token: str
    expires_at: _timestamp_pb2.Timestamp
    account_id: int
    username: str
    session: _mfa_pb2.SessionInfo
    def __init__(self, access_token: _Optional[str] = ..., expires_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., account_id: _Optional[int] = ..., username: _Optional[str] = ..., session: _Optional[_Union[_mfa_pb2.SessionInfo, _Mapping]] = ...) -> None: ...

class MeRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MeResponse(_message.Message):
    __slots__ = ("account_id", "api_key_id", "username", "root_smart_account_address", "session")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    API_KEY_ID_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    ROOT_SMART_ACCOUNT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    SESSION_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    api_key_id: str
    username: str
    root_smart_account_address: str
    session: _mfa_pb2.SessionInfo
    def __init__(self, account_id: _Optional[int] = ..., api_key_id: _Optional[str] = ..., username: _Optional[str] = ..., root_smart_account_address: _Optional[str] = ..., session: _Optional[_Union[_mfa_pb2.SessionInfo, _Mapping]] = ...) -> None: ...

class AuthErrorDetail(_message.Message):
    __slots__ = ("code", "message")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    code: AuthErrorCode
    message: str
    def __init__(self, code: _Optional[_Union[AuthErrorCode, str]] = ..., message: _Optional[str] = ...) -> None: ...

class AcceptTermsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class AcceptTermsResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
