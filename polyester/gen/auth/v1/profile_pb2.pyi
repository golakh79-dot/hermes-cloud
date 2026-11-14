import datetime

from polyester.gen.buf.validate import validate_pb2 as _validate_pb2
from polyester.gen.gnostic.openapi.v3 import annotations_pb2 as _annotations_pb2
from polyester.gen.google.api import annotations_pb2 as _annotations_pb2_1
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from polyester.gen.polyester.api import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ProfileErrorCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PROFILE_UNSPECIFIED: _ClassVar[ProfileErrorCode]
    PROFILE_INVALID_FIELD: _ClassVar[ProfileErrorCode]
    PROFILE_FIELD_TOO_LONG: _ClassVar[ProfileErrorCode]
    PROFILE_URL_INVALID: _ClassVar[ProfileErrorCode]
    PROFILE_URL_SCHEME_INVALID: _ClassVar[ProfileErrorCode]
PROFILE_UNSPECIFIED: ProfileErrorCode
PROFILE_INVALID_FIELD: ProfileErrorCode
PROFILE_FIELD_TOO_LONG: ProfileErrorCode
PROFILE_URL_INVALID: ProfileErrorCode
PROFILE_URL_SCHEME_INVALID: ProfileErrorCode

class AccountIdentity(_message.Message):
    __slots__ = ("account_id", "username", "avatar_url", "root_smart_account_address")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    AVATAR_URL_FIELD_NUMBER: _ClassVar[int]
    ROOT_SMART_ACCOUNT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    username: str
    avatar_url: str
    root_smart_account_address: str
    def __init__(self, account_id: _Optional[int] = ..., username: _Optional[str] = ..., avatar_url: _Optional[str] = ..., root_smart_account_address: _Optional[str] = ...) -> None: ...

class UserProfile(_message.Message):
    __slots__ = ("username", "bio", "website", "twitter", "twitter_verified", "discord", "discord_verified", "avatar_url", "created_at", "next_username_change_at", "vip_tier", "username_unlocked", "current_terms_accepted")
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    BIO_FIELD_NUMBER: _ClassVar[int]
    WEBSITE_FIELD_NUMBER: _ClassVar[int]
    TWITTER_FIELD_NUMBER: _ClassVar[int]
    TWITTER_VERIFIED_FIELD_NUMBER: _ClassVar[int]
    DISCORD_FIELD_NUMBER: _ClassVar[int]
    DISCORD_VERIFIED_FIELD_NUMBER: _ClassVar[int]
    AVATAR_URL_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    NEXT_USERNAME_CHANGE_AT_FIELD_NUMBER: _ClassVar[int]
    VIP_TIER_FIELD_NUMBER: _ClassVar[int]
    USERNAME_UNLOCKED_FIELD_NUMBER: _ClassVar[int]
    CURRENT_TERMS_ACCEPTED_FIELD_NUMBER: _ClassVar[int]
    username: str
    bio: str
    website: str
    twitter: str
    twitter_verified: bool
    discord: str
    discord_verified: bool
    avatar_url: str
    created_at: _timestamp_pb2.Timestamp
    next_username_change_at: _timestamp_pb2.Timestamp
    vip_tier: int
    username_unlocked: bool
    current_terms_accepted: bool
    def __init__(self, username: _Optional[str] = ..., bio: _Optional[str] = ..., website: _Optional[str] = ..., twitter: _Optional[str] = ..., twitter_verified: _Optional[bool] = ..., discord: _Optional[str] = ..., discord_verified: _Optional[bool] = ..., avatar_url: _Optional[str] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., next_username_change_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., vip_tier: _Optional[int] = ..., username_unlocked: _Optional[bool] = ..., current_terms_accepted: _Optional[bool] = ...) -> None: ...

class UserProfilePatch(_message.Message):
    __slots__ = ("username", "bio", "website", "twitter", "avatar_url")
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    BIO_FIELD_NUMBER: _ClassVar[int]
    WEBSITE_FIELD_NUMBER: _ClassVar[int]
    TWITTER_FIELD_NUMBER: _ClassVar[int]
    AVATAR_URL_FIELD_NUMBER: _ClassVar[int]
    username: str
    bio: str
    website: str
    twitter: str
    avatar_url: str
    def __init__(self, username: _Optional[str] = ..., bio: _Optional[str] = ..., website: _Optional[str] = ..., twitter: _Optional[str] = ..., avatar_url: _Optional[str] = ...) -> None: ...

class GetProfileRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ProfileErrorDetail(_message.Message):
    __slots__ = ("code", "field", "message")
    CODE_FIELD_NUMBER: _ClassVar[int]
    FIELD_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    code: ProfileErrorCode
    field: str
    message: str
    def __init__(self, code: _Optional[_Union[ProfileErrorCode, str]] = ..., field: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class UsernameHistoryEntry(_message.Message):
    __slots__ = ("username", "set_at")
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    SET_AT_FIELD_NUMBER: _ClassVar[int]
    username: str
    set_at: _timestamp_pb2.Timestamp
    def __init__(self, username: _Optional[str] = ..., set_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class GetUsernameHistoryRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetUsernameHistoryResponse(_message.Message):
    __slots__ = ("history",)
    HISTORY_FIELD_NUMBER: _ClassVar[int]
    history: _containers.RepeatedCompositeFieldContainer[UsernameHistoryEntry]
    def __init__(self, history: _Optional[_Iterable[_Union[UsernameHistoryEntry, _Mapping]]] = ...) -> None: ...

class GenerateUsernameOptionsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GenerateUsernameOptionsResponse(_message.Message):
    __slots__ = ("usernames", "offer_token", "expires_at")
    USERNAMES_FIELD_NUMBER: _ClassVar[int]
    OFFER_TOKEN_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    usernames: _containers.RepeatedScalarFieldContainer[str]
    offer_token: str
    expires_at: _timestamp_pb2.Timestamp
    def __init__(self, usernames: _Optional[_Iterable[str]] = ..., offer_token: _Optional[str] = ..., expires_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ClaimGeneratedUsernameRequest(_message.Message):
    __slots__ = ("offer_token", "option_index")
    OFFER_TOKEN_FIELD_NUMBER: _ClassVar[int]
    OPTION_INDEX_FIELD_NUMBER: _ClassVar[int]
    offer_token: str
    option_index: int
    def __init__(self, offer_token: _Optional[str] = ..., option_index: _Optional[int] = ...) -> None: ...
