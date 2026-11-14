import datetime

from polyester.gen.buf.validate import validate_pb2 as _validate_pb2
from polyester.gen.gnostic.openapi.v3 import annotations_pb2 as _annotations_pb2
from polyester.gen.google.api import annotations_pb2 as _annotations_pb2_1
from polyester.gen.google.api import field_behavior_pb2 as _field_behavior_pb2
from google.protobuf import field_mask_pb2 as _field_mask_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from polyester.gen.polyester.api import options_pb2 as _options_pb2
from polyester.gen.polyester.api.validation.v1 import predefined_string_rules_pb2 as _predefined_string_rules_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ApiKeyStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    API_KEY_STATUS_UNSPECIFIED: _ClassVar[ApiKeyStatus]
    ACTIVE: _ClassVar[ApiKeyStatus]
    REVOKED: _ClassVar[ApiKeyStatus]
    DISABLED: _ClassVar[ApiKeyStatus]
API_KEY_STATUS_UNSPECIFIED: ApiKeyStatus
ACTIVE: ApiKeyStatus
REVOKED: ApiKeyStatus
DISABLED: ApiKeyStatus

class ApiKey(_message.Message):
    __slots__ = ("key_id", "label", "icon", "color", "ip_whitelist", "status", "subaccount_id", "policy_id", "created_at", "last_used_at", "public_key_ed25519", "expires_at", "created_by_actor", "updated_at", "revision")
    KEY_ID_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    ICON_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    IP_WHITELIST_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    POLICY_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    LAST_USED_AT_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_KEY_ED25519_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_ACTOR_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    REVISION_FIELD_NUMBER: _ClassVar[int]
    key_id: str
    label: str
    icon: str
    color: str
    ip_whitelist: _containers.RepeatedScalarFieldContainer[str]
    status: ApiKeyStatus
    subaccount_id: int
    policy_id: int
    created_at: _timestamp_pb2.Timestamp
    last_used_at: _timestamp_pb2.Timestamp
    public_key_ed25519: bytes
    expires_at: _timestamp_pb2.Timestamp
    created_by_actor: str
    updated_at: _timestamp_pb2.Timestamp
    revision: int
    def __init__(self, key_id: _Optional[str] = ..., label: _Optional[str] = ..., icon: _Optional[str] = ..., color: _Optional[str] = ..., ip_whitelist: _Optional[_Iterable[str]] = ..., status: _Optional[_Union[ApiKeyStatus, str]] = ..., subaccount_id: _Optional[int] = ..., policy_id: _Optional[int] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., last_used_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., public_key_ed25519: _Optional[bytes] = ..., expires_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., created_by_actor: _Optional[str] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., revision: _Optional[int] = ...) -> None: ...

class CreateApiKeyRequest(_message.Message):
    __slots__ = ("label", "subaccount_id", "icon", "color", "ip_whitelist", "public_key_ed25519")
    LABEL_FIELD_NUMBER: _ClassVar[int]
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ICON_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    IP_WHITELIST_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_KEY_ED25519_FIELD_NUMBER: _ClassVar[int]
    label: str
    subaccount_id: int
    icon: str
    color: str
    ip_whitelist: _containers.RepeatedScalarFieldContainer[str]
    public_key_ed25519: bytes
    def __init__(self, label: _Optional[str] = ..., subaccount_id: _Optional[int] = ..., icon: _Optional[str] = ..., color: _Optional[str] = ..., ip_whitelist: _Optional[_Iterable[str]] = ..., public_key_ed25519: _Optional[bytes] = ...) -> None: ...

class CreateApiKeyResponse(_message.Message):
    __slots__ = ("api_key",)
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    api_key: ApiKey
    def __init__(self, api_key: _Optional[_Union[ApiKey, _Mapping]] = ...) -> None: ...

class ListApiKeysRequest(_message.Message):
    __slots__ = ("subaccount_id",)
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    def __init__(self, subaccount_id: _Optional[int] = ...) -> None: ...

class ListApiKeysResponse(_message.Message):
    __slots__ = ("api_keys",)
    API_KEYS_FIELD_NUMBER: _ClassVar[int]
    api_keys: _containers.RepeatedCompositeFieldContainer[ApiKey]
    def __init__(self, api_keys: _Optional[_Iterable[_Union[ApiKey, _Mapping]]] = ...) -> None: ...

class DeleteApiKeyRequest(_message.Message):
    __slots__ = ("key_id",)
    KEY_ID_FIELD_NUMBER: _ClassVar[int]
    key_id: str
    def __init__(self, key_id: _Optional[str] = ...) -> None: ...

class DeleteApiKeyResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetApiKeyRequest(_message.Message):
    __slots__ = ("key_id",)
    KEY_ID_FIELD_NUMBER: _ClassVar[int]
    key_id: str
    def __init__(self, key_id: _Optional[str] = ...) -> None: ...

class GetApiKeyResponse(_message.Message):
    __slots__ = ("api_key",)
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    api_key: ApiKey
    def __init__(self, api_key: _Optional[_Union[ApiKey, _Mapping]] = ...) -> None: ...

class ApiKeyUpdateSpec(_message.Message):
    __slots__ = ("label", "icon", "color", "status", "ip_whitelist", "expires_at")
    LABEL_FIELD_NUMBER: _ClassVar[int]
    ICON_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    IP_WHITELIST_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    label: str
    icon: str
    color: str
    status: ApiKeyStatus
    ip_whitelist: _containers.RepeatedScalarFieldContainer[str]
    expires_at: _timestamp_pb2.Timestamp
    def __init__(self, label: _Optional[str] = ..., icon: _Optional[str] = ..., color: _Optional[str] = ..., status: _Optional[_Union[ApiKeyStatus, str]] = ..., ip_whitelist: _Optional[_Iterable[str]] = ..., expires_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class UpdateApiKeyRequest(_message.Message):
    __slots__ = ("key_id", "api_key", "update_mask", "expected_revision")
    KEY_ID_FIELD_NUMBER: _ClassVar[int]
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_REVISION_FIELD_NUMBER: _ClassVar[int]
    key_id: str
    api_key: ApiKeyUpdateSpec
    update_mask: _field_mask_pb2.FieldMask
    expected_revision: int
    def __init__(self, key_id: _Optional[str] = ..., api_key: _Optional[_Union[ApiKeyUpdateSpec, _Mapping]] = ..., update_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ..., expected_revision: _Optional[int] = ...) -> None: ...

class UpdateApiKeyResponse(_message.Message):
    __slots__ = ("api_key",)
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    api_key: ApiKey
    def __init__(self, api_key: _Optional[_Union[ApiKey, _Mapping]] = ...) -> None: ...
