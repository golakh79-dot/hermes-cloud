import datetime

from polyester.gen.auth.v1 import api_keys_pb2 as _api_keys_pb2
from polyester.gen.auth.v1 import policies_pb2 as _policies_pb2
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

class SubaccountStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SUBACCOUNT_STATUS_UNSPECIFIED: _ClassVar[SubaccountStatus]
    SUBACCOUNT_STATUS_ACTIVE: _ClassVar[SubaccountStatus]
    SUBACCOUNT_STATUS_DISABLED: _ClassVar[SubaccountStatus]

class SubaccountRole(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SUBACCOUNT_ROLE_UNSPECIFIED: _ClassVar[SubaccountRole]
    VIEWER: _ClassVar[SubaccountRole]
    TRADER: _ClassVar[SubaccountRole]
    LEVERAGED_TRADER: _ClassVar[SubaccountRole]
    TREASURY: _ClassVar[SubaccountRole]
    ADMIN: _ClassVar[SubaccountRole]
    OWNER: _ClassVar[SubaccountRole]

class SubaccountPermission(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SUBACCOUNT_PERMISSION_UNSPECIFIED: _ClassVar[SubaccountPermission]
    SUBACCOUNT_PERMISSION_READ_SUBACCOUNT: _ClassVar[SubaccountPermission]
    SUBACCOUNT_PERMISSION_UPDATE_SUBACCOUNT: _ClassVar[SubaccountPermission]
    SUBACCOUNT_PERMISSION_READ_BALANCES: _ClassVar[SubaccountPermission]
    SUBACCOUNT_PERMISSION_READ_SPOT: _ClassVar[SubaccountPermission]
    SUBACCOUNT_PERMISSION_TRADE_SPOT: _ClassVar[SubaccountPermission]
    SUBACCOUNT_PERMISSION_READ_INTERNAL_TRANSFERS: _ClassVar[SubaccountPermission]
    SUBACCOUNT_PERMISSION_INTERNAL_TRANSFER: _ClassVar[SubaccountPermission]
    SUBACCOUNT_PERMISSION_EXTERNAL_WITHDRAW: _ClassVar[SubaccountPermission]
    SUBACCOUNT_PERMISSION_READ_ADDRESS_BOOK: _ClassVar[SubaccountPermission]
    SUBACCOUNT_PERMISSION_MANAGE_ADDRESS_BOOK: _ClassVar[SubaccountPermission]
    SUBACCOUNT_PERMISSION_READ_MEMBERS: _ClassVar[SubaccountPermission]
    SUBACCOUNT_PERMISSION_MANAGE_MEMBERS: _ClassVar[SubaccountPermission]
    SUBACCOUNT_PERMISSION_READ_INVITES: _ClassVar[SubaccountPermission]
    SUBACCOUNT_PERMISSION_MANAGE_INVITES: _ClassVar[SubaccountPermission]
    SUBACCOUNT_PERMISSION_READ_API_KEYS: _ClassVar[SubaccountPermission]
    SUBACCOUNT_PERMISSION_MANAGE_API_KEYS: _ClassVar[SubaccountPermission]
    SUBACCOUNT_PERMISSION_READ_SUBACCOUNT_POLICY: _ClassVar[SubaccountPermission]
    SUBACCOUNT_PERMISSION_MANAGE_SUBACCOUNT_POLICY: _ClassVar[SubaccountPermission]
    SUBACCOUNT_PERMISSION_READ_ACTIVITY: _ClassVar[SubaccountPermission]
    SUBACCOUNT_PERMISSION_READ_ACTIVITY_SECURITY_DETAILS: _ClassVar[SubaccountPermission]
    SUBACCOUNT_PERMISSION_MANAGE_MEMBER_MFA_REQUIREMENT: _ClassVar[SubaccountPermission]
    SUBACCOUNT_PERMISSION_CREATE_DEPOSIT_ADDRESS: _ClassVar[SubaccountPermission]
    SUBACCOUNT_PERMISSION_READ_DEPOSIT_ADDRESSES: _ClassVar[SubaccountPermission]
    SUBACCOUNT_PERMISSION_READ_GUARD_SIGNER_STATUS: _ClassVar[SubaccountPermission]
    SUBACCOUNT_PERMISSION_MANAGE_GUARD_SIGNER: _ClassVar[SubaccountPermission]
    SUBACCOUNT_PERMISSION_READ_AUTO_WITHDRAW: _ClassVar[SubaccountPermission]
    SUBACCOUNT_PERMISSION_MANAGE_AUTO_WITHDRAW: _ClassVar[SubaccountPermission]
    SUBACCOUNT_PERMISSION_SWAP: _ClassVar[SubaccountPermission]

class SubaccountInviteStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SUBACCOUNT_INVITE_STATUS_UNSPECIFIED: _ClassVar[SubaccountInviteStatus]
    SUBACCOUNT_INVITE_STATUS_PENDING: _ClassVar[SubaccountInviteStatus]
    SUBACCOUNT_INVITE_STATUS_ACCEPTED: _ClassVar[SubaccountInviteStatus]
    SUBACCOUNT_INVITE_STATUS_DECLINED: _ClassVar[SubaccountInviteStatus]
    SUBACCOUNT_INVITE_STATUS_CANCELLED: _ClassVar[SubaccountInviteStatus]

class SubaccountInviteDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DIRECTION_UNSPECIFIED: _ClassVar[SubaccountInviteDirection]
    INCOMING: _ClassVar[SubaccountInviteDirection]
    OUTGOING: _ClassVar[SubaccountInviteDirection]

class SubaccountInviteAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SUBACCOUNT_INVITE_ACTION_UNSPECIFIED: _ClassVar[SubaccountInviteAction]
    SUBACCOUNT_INVITE_ACTION_ACCEPT: _ClassVar[SubaccountInviteAction]
    SUBACCOUNT_INVITE_ACTION_DECLINE: _ClassVar[SubaccountInviteAction]
    SUBACCOUNT_INVITE_ACTION_CANCEL: _ClassVar[SubaccountInviteAction]

class ActivityEntityKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ACTIVITY_ENTITY_UNSPECIFIED: _ClassVar[ActivityEntityKind]
    ACTIVITY_ENTITY_ACCOUNT: _ClassVar[ActivityEntityKind]
    ACTIVITY_ENTITY_SESSION: _ClassVar[ActivityEntityKind]
    ACTIVITY_ENTITY_API_KEY: _ClassVar[ActivityEntityKind]
    ACTIVITY_ENTITY_SUBACCOUNT: _ClassVar[ActivityEntityKind]
    ACTIVITY_ENTITY_MEMBER: _ClassVar[ActivityEntityKind]
    ACTIVITY_ENTITY_POLICY: _ClassVar[ActivityEntityKind]
    ACTIVITY_ENTITY_INVITE: _ClassVar[ActivityEntityKind]
    ACTIVITY_ENTITY_SECURITY: _ClassVar[ActivityEntityKind]
    ACTIVITY_ENTITY_DESTINATION: _ClassVar[ActivityEntityKind]

class ActivityEventAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ACTIVITY_ACTION_UNSPECIFIED: _ClassVar[ActivityEventAction]
    ACTIVITY_ACTION_CREATED: _ClassVar[ActivityEventAction]
    ACTIVITY_ACTION_UPDATED: _ClassVar[ActivityEventAction]
    ACTIVITY_ACTION_DELETED: _ClassVar[ActivityEventAction]
    ACTIVITY_ACTION_ENABLED: _ClassVar[ActivityEventAction]
    ACTIVITY_ACTION_DISABLED: _ClassVar[ActivityEventAction]
    ACTIVITY_ACTION_REMOVED: _ClassVar[ActivityEventAction]
    ACTIVITY_ACTION_ROLE_SET: _ClassVar[ActivityEventAction]
    ACTIVITY_ACTION_RECEIVED: _ClassVar[ActivityEventAction]
    ACTIVITY_ACTION_REPLIED: _ClassVar[ActivityEventAction]
    ACTIVITY_ACTION_FAILED: _ClassVar[ActivityEventAction]
    ACTIVITY_ACTION_REVOKED: _ClassVar[ActivityEventAction]
    ACTIVITY_ACTION_BLOCKED: _ClassVar[ActivityEventAction]
    ACTIVITY_ACTION_HOLD_PLACED: _ClassVar[ActivityEventAction]
    ACTIVITY_ACTION_HOLD_RELEASED: _ClassVar[ActivityEventAction]

class ActivityEventSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ACTIVITY_SOURCE_UNSPECIFIED: _ClassVar[ActivityEventSource]
    ACTIVITY_SOURCE_WEB: _ClassVar[ActivityEventSource]
    ACTIVITY_SOURCE_MOBILE: _ClassVar[ActivityEventSource]
    ACTIVITY_SOURCE_API: _ClassVar[ActivityEventSource]
SUBACCOUNT_STATUS_UNSPECIFIED: SubaccountStatus
SUBACCOUNT_STATUS_ACTIVE: SubaccountStatus
SUBACCOUNT_STATUS_DISABLED: SubaccountStatus
SUBACCOUNT_ROLE_UNSPECIFIED: SubaccountRole
VIEWER: SubaccountRole
TRADER: SubaccountRole
LEVERAGED_TRADER: SubaccountRole
TREASURY: SubaccountRole
ADMIN: SubaccountRole
OWNER: SubaccountRole
SUBACCOUNT_PERMISSION_UNSPECIFIED: SubaccountPermission
SUBACCOUNT_PERMISSION_READ_SUBACCOUNT: SubaccountPermission
SUBACCOUNT_PERMISSION_UPDATE_SUBACCOUNT: SubaccountPermission
SUBACCOUNT_PERMISSION_READ_BALANCES: SubaccountPermission
SUBACCOUNT_PERMISSION_READ_SPOT: SubaccountPermission
SUBACCOUNT_PERMISSION_TRADE_SPOT: SubaccountPermission
SUBACCOUNT_PERMISSION_READ_INTERNAL_TRANSFERS: SubaccountPermission
SUBACCOUNT_PERMISSION_INTERNAL_TRANSFER: SubaccountPermission
SUBACCOUNT_PERMISSION_EXTERNAL_WITHDRAW: SubaccountPermission
SUBACCOUNT_PERMISSION_READ_ADDRESS_BOOK: SubaccountPermission
SUBACCOUNT_PERMISSION_MANAGE_ADDRESS_BOOK: SubaccountPermission
SUBACCOUNT_PERMISSION_READ_MEMBERS: SubaccountPermission
SUBACCOUNT_PERMISSION_MANAGE_MEMBERS: SubaccountPermission
SUBACCOUNT_PERMISSION_READ_INVITES: SubaccountPermission
SUBACCOUNT_PERMISSION_MANAGE_INVITES: SubaccountPermission
SUBACCOUNT_PERMISSION_READ_API_KEYS: SubaccountPermission
SUBACCOUNT_PERMISSION_MANAGE_API_KEYS: SubaccountPermission
SUBACCOUNT_PERMISSION_READ_SUBACCOUNT_POLICY: SubaccountPermission
SUBACCOUNT_PERMISSION_MANAGE_SUBACCOUNT_POLICY: SubaccountPermission
SUBACCOUNT_PERMISSION_READ_ACTIVITY: SubaccountPermission
SUBACCOUNT_PERMISSION_READ_ACTIVITY_SECURITY_DETAILS: SubaccountPermission
SUBACCOUNT_PERMISSION_MANAGE_MEMBER_MFA_REQUIREMENT: SubaccountPermission
SUBACCOUNT_PERMISSION_CREATE_DEPOSIT_ADDRESS: SubaccountPermission
SUBACCOUNT_PERMISSION_READ_DEPOSIT_ADDRESSES: SubaccountPermission
SUBACCOUNT_PERMISSION_READ_GUARD_SIGNER_STATUS: SubaccountPermission
SUBACCOUNT_PERMISSION_MANAGE_GUARD_SIGNER: SubaccountPermission
SUBACCOUNT_PERMISSION_READ_AUTO_WITHDRAW: SubaccountPermission
SUBACCOUNT_PERMISSION_MANAGE_AUTO_WITHDRAW: SubaccountPermission
SUBACCOUNT_PERMISSION_SWAP: SubaccountPermission
SUBACCOUNT_INVITE_STATUS_UNSPECIFIED: SubaccountInviteStatus
SUBACCOUNT_INVITE_STATUS_PENDING: SubaccountInviteStatus
SUBACCOUNT_INVITE_STATUS_ACCEPTED: SubaccountInviteStatus
SUBACCOUNT_INVITE_STATUS_DECLINED: SubaccountInviteStatus
SUBACCOUNT_INVITE_STATUS_CANCELLED: SubaccountInviteStatus
DIRECTION_UNSPECIFIED: SubaccountInviteDirection
INCOMING: SubaccountInviteDirection
OUTGOING: SubaccountInviteDirection
SUBACCOUNT_INVITE_ACTION_UNSPECIFIED: SubaccountInviteAction
SUBACCOUNT_INVITE_ACTION_ACCEPT: SubaccountInviteAction
SUBACCOUNT_INVITE_ACTION_DECLINE: SubaccountInviteAction
SUBACCOUNT_INVITE_ACTION_CANCEL: SubaccountInviteAction
ACTIVITY_ENTITY_UNSPECIFIED: ActivityEntityKind
ACTIVITY_ENTITY_ACCOUNT: ActivityEntityKind
ACTIVITY_ENTITY_SESSION: ActivityEntityKind
ACTIVITY_ENTITY_API_KEY: ActivityEntityKind
ACTIVITY_ENTITY_SUBACCOUNT: ActivityEntityKind
ACTIVITY_ENTITY_MEMBER: ActivityEntityKind
ACTIVITY_ENTITY_POLICY: ActivityEntityKind
ACTIVITY_ENTITY_INVITE: ActivityEntityKind
ACTIVITY_ENTITY_SECURITY: ActivityEntityKind
ACTIVITY_ENTITY_DESTINATION: ActivityEntityKind
ACTIVITY_ACTION_UNSPECIFIED: ActivityEventAction
ACTIVITY_ACTION_CREATED: ActivityEventAction
ACTIVITY_ACTION_UPDATED: ActivityEventAction
ACTIVITY_ACTION_DELETED: ActivityEventAction
ACTIVITY_ACTION_ENABLED: ActivityEventAction
ACTIVITY_ACTION_DISABLED: ActivityEventAction
ACTIVITY_ACTION_REMOVED: ActivityEventAction
ACTIVITY_ACTION_ROLE_SET: ActivityEventAction
ACTIVITY_ACTION_RECEIVED: ActivityEventAction
ACTIVITY_ACTION_REPLIED: ActivityEventAction
ACTIVITY_ACTION_FAILED: ActivityEventAction
ACTIVITY_ACTION_REVOKED: ActivityEventAction
ACTIVITY_ACTION_BLOCKED: ActivityEventAction
ACTIVITY_ACTION_HOLD_PLACED: ActivityEventAction
ACTIVITY_ACTION_HOLD_RELEASED: ActivityEventAction
ACTIVITY_SOURCE_UNSPECIFIED: ActivityEventSource
ACTIVITY_SOURCE_WEB: ActivityEventSource
ACTIVITY_SOURCE_MOBILE: ActivityEventSource
ACTIVITY_SOURCE_API: ActivityEventSource

class SubaccountPermissionDefinition(_message.Message):
    __slots__ = ("permission", "display_name", "description", "policy_action")
    PERMISSION_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    POLICY_ACTION_FIELD_NUMBER: _ClassVar[int]
    permission: SubaccountPermission
    display_name: str
    description: str
    policy_action: _policies_pb2.PolicyAction
    def __init__(self, permission: _Optional[_Union[SubaccountPermission, str]] = ..., display_name: _Optional[str] = ..., description: _Optional[str] = ..., policy_action: _Optional[_Union[_policies_pb2.PolicyAction, str]] = ...) -> None: ...

class SubaccountRoleDefinition(_message.Message):
    __slots__ = ("role", "display_name", "description", "assignable", "permissions")
    ROLE_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ASSIGNABLE_FIELD_NUMBER: _ClassVar[int]
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    role: SubaccountRole
    display_name: str
    description: str
    assignable: bool
    permissions: _containers.RepeatedScalarFieldContainer[SubaccountPermission]
    def __init__(self, role: _Optional[_Union[SubaccountRole, str]] = ..., display_name: _Optional[str] = ..., description: _Optional[str] = ..., assignable: _Optional[bool] = ..., permissions: _Optional[_Iterable[_Union[SubaccountPermission, str]]] = ...) -> None: ...

class ListSubaccountRolesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListSubaccountRolesResponse(_message.Message):
    __slots__ = ("permissions", "roles")
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    ROLES_FIELD_NUMBER: _ClassVar[int]
    permissions: _containers.RepeatedCompositeFieldContainer[SubaccountPermissionDefinition]
    roles: _containers.RepeatedCompositeFieldContainer[SubaccountRoleDefinition]
    def __init__(self, permissions: _Optional[_Iterable[_Union[SubaccountPermissionDefinition, _Mapping]]] = ..., roles: _Optional[_Iterable[_Union[SubaccountRoleDefinition, _Mapping]]] = ...) -> None: ...

class GetEffectiveSubaccountPermissionsRequest(_message.Message):
    __slots__ = ("subaccount_id",)
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    def __init__(self, subaccount_id: _Optional[int] = ...) -> None: ...

class GetEffectiveSubaccountPermissionsResponse(_message.Message):
    __slots__ = ("role", "permissions", "subaccount_policy_id")
    ROLE_FIELD_NUMBER: _ClassVar[int]
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    SUBACCOUNT_POLICY_ID_FIELD_NUMBER: _ClassVar[int]
    role: SubaccountRole
    permissions: _containers.RepeatedScalarFieldContainer[SubaccountPermission]
    subaccount_policy_id: int
    def __init__(self, role: _Optional[_Union[SubaccountRole, str]] = ..., permissions: _Optional[_Iterable[_Union[SubaccountPermission, str]]] = ..., subaccount_policy_id: _Optional[int] = ...) -> None: ...

class SubaccountRoleView(_message.Message):
    __slots__ = ("subaccount_id", "role")
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    role: SubaccountRole
    def __init__(self, subaccount_id: _Optional[int] = ..., role: _Optional[_Union[SubaccountRole, str]] = ...) -> None: ...

class Subaccount(_message.Message):
    __slots__ = ("id", "role", "label", "icon", "color", "status", "smart_account_address", "owner_username", "owner_avatar_url", "owner_root_smart_account_address", "subaccount_policy_id", "require_member_mfa", "smart_account_salt_nonce", "updated_at", "revision", "removed")
    ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    ICON_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SMART_ACCOUNT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    OWNER_USERNAME_FIELD_NUMBER: _ClassVar[int]
    OWNER_AVATAR_URL_FIELD_NUMBER: _ClassVar[int]
    OWNER_ROOT_SMART_ACCOUNT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    SUBACCOUNT_POLICY_ID_FIELD_NUMBER: _ClassVar[int]
    REQUIRE_MEMBER_MFA_FIELD_NUMBER: _ClassVar[int]
    SMART_ACCOUNT_SALT_NONCE_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    REVISION_FIELD_NUMBER: _ClassVar[int]
    REMOVED_FIELD_NUMBER: _ClassVar[int]
    id: int
    role: SubaccountRole
    label: str
    icon: str
    color: str
    status: SubaccountStatus
    smart_account_address: str
    owner_username: str
    owner_avatar_url: str
    owner_root_smart_account_address: str
    subaccount_policy_id: int
    require_member_mfa: bool
    smart_account_salt_nonce: int
    updated_at: _timestamp_pb2.Timestamp
    revision: int
    removed: bool
    def __init__(self, id: _Optional[int] = ..., role: _Optional[_Union[SubaccountRole, str]] = ..., label: _Optional[str] = ..., icon: _Optional[str] = ..., color: _Optional[str] = ..., status: _Optional[_Union[SubaccountStatus, str]] = ..., smart_account_address: _Optional[str] = ..., owner_username: _Optional[str] = ..., owner_avatar_url: _Optional[str] = ..., owner_root_smart_account_address: _Optional[str] = ..., subaccount_policy_id: _Optional[int] = ..., require_member_mfa: _Optional[bool] = ..., smart_account_salt_nonce: _Optional[int] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., revision: _Optional[int] = ..., removed: _Optional[bool] = ...) -> None: ...

class ListSubaccountsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListSubaccountsResponse(_message.Message):
    __slots__ = ("subaccounts", "total_created")
    SUBACCOUNTS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_CREATED_FIELD_NUMBER: _ClassVar[int]
    subaccounts: _containers.RepeatedCompositeFieldContainer[Subaccount]
    total_created: int
    def __init__(self, subaccounts: _Optional[_Iterable[_Union[Subaccount, _Mapping]]] = ..., total_created: _Optional[int] = ...) -> None: ...

class CreateSubaccountChallengeRequest(_message.Message):
    __slots__ = ("owner_address", "uri")
    OWNER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    URI_FIELD_NUMBER: _ClassVar[int]
    owner_address: str
    uri: str
    def __init__(self, owner_address: _Optional[str] = ..., uri: _Optional[str] = ...) -> None: ...

class CreateSubaccountChallengeResponse(_message.Message):
    __slots__ = ("message", "smart_account_address", "smart_account_salt_nonce", "expires_at", "polyester_chain_id")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SMART_ACCOUNT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    SMART_ACCOUNT_SALT_NONCE_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    POLYESTER_CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    message: str
    smart_account_address: str
    smart_account_salt_nonce: int
    expires_at: _timestamp_pb2.Timestamp
    polyester_chain_id: int
    def __init__(self, message: _Optional[str] = ..., smart_account_address: _Optional[str] = ..., smart_account_salt_nonce: _Optional[int] = ..., expires_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., polyester_chain_id: _Optional[int] = ...) -> None: ...

class CreateSubaccountRequest(_message.Message):
    __slots__ = ("label", "icon", "color", "smart_account_address", "message", "signature")
    LABEL_FIELD_NUMBER: _ClassVar[int]
    ICON_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    SMART_ACCOUNT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    label: str
    icon: str
    color: str
    smart_account_address: str
    message: str
    signature: str
    def __init__(self, label: _Optional[str] = ..., icon: _Optional[str] = ..., color: _Optional[str] = ..., smart_account_address: _Optional[str] = ..., message: _Optional[str] = ..., signature: _Optional[str] = ...) -> None: ...

class CreateSubaccountResponse(_message.Message):
    __slots__ = ("subaccount_id", "total_created", "smart_account_salt_nonce", "revision")
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    TOTAL_CREATED_FIELD_NUMBER: _ClassVar[int]
    SMART_ACCOUNT_SALT_NONCE_FIELD_NUMBER: _ClassVar[int]
    REVISION_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    total_created: int
    smart_account_salt_nonce: int
    revision: int
    def __init__(self, subaccount_id: _Optional[int] = ..., total_created: _Optional[int] = ..., smart_account_salt_nonce: _Optional[int] = ..., revision: _Optional[int] = ...) -> None: ...

class SubaccountUpdateSpec(_message.Message):
    __slots__ = ("label", "icon", "color", "status")
    LABEL_FIELD_NUMBER: _ClassVar[int]
    ICON_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    label: str
    icon: str
    color: str
    status: SubaccountStatus
    def __init__(self, label: _Optional[str] = ..., icon: _Optional[str] = ..., color: _Optional[str] = ..., status: _Optional[_Union[SubaccountStatus, str]] = ...) -> None: ...

class UpdateSubaccountRequest(_message.Message):
    __slots__ = ("subaccount_id", "subaccount", "update_mask", "expected_revision")
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    SUBACCOUNT_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_REVISION_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    subaccount: SubaccountUpdateSpec
    update_mask: _field_mask_pb2.FieldMask
    expected_revision: int
    def __init__(self, subaccount_id: _Optional[int] = ..., subaccount: _Optional[_Union[SubaccountUpdateSpec, _Mapping]] = ..., update_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ..., expected_revision: _Optional[int] = ...) -> None: ...

class UpdateSubaccountResponse(_message.Message):
    __slots__ = ("subaccount",)
    SUBACCOUNT_FIELD_NUMBER: _ClassVar[int]
    subaccount: Subaccount
    def __init__(self, subaccount: _Optional[_Union[Subaccount, _Mapping]] = ...) -> None: ...

class SetSubaccountMemberMFARequirementRequest(_message.Message):
    __slots__ = ("subaccount_id", "require_member_mfa")
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    REQUIRE_MEMBER_MFA_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    require_member_mfa: bool
    def __init__(self, subaccount_id: _Optional[int] = ..., require_member_mfa: _Optional[bool] = ...) -> None: ...

class SetSubaccountMemberMFARequirementResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SubaccountMemberView(_message.Message):
    __slots__ = ("account_id", "role", "username", "smart_account_address", "avatar_url", "mfa_enrolled")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    SMART_ACCOUNT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    AVATAR_URL_FIELD_NUMBER: _ClassVar[int]
    MFA_ENROLLED_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    role: SubaccountRole
    username: str
    smart_account_address: str
    avatar_url: str
    mfa_enrolled: bool
    def __init__(self, account_id: _Optional[int] = ..., role: _Optional[_Union[SubaccountRole, str]] = ..., username: _Optional[str] = ..., smart_account_address: _Optional[str] = ..., avatar_url: _Optional[str] = ..., mfa_enrolled: _Optional[bool] = ...) -> None: ...

class ListSubaccountMembersRequest(_message.Message):
    __slots__ = ("subaccount_id",)
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    def __init__(self, subaccount_id: _Optional[int] = ...) -> None: ...

class ListSubaccountMembersResponse(_message.Message):
    __slots__ = ("members",)
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    members: _containers.RepeatedCompositeFieldContainer[SubaccountMemberView]
    def __init__(self, members: _Optional[_Iterable[_Union[SubaccountMemberView, _Mapping]]] = ...) -> None: ...

class RemoveSubaccountMemberRequest(_message.Message):
    __slots__ = ("subaccount_id", "grantee_account_id")
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    GRANTEE_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    grantee_account_id: int
    def __init__(self, subaccount_id: _Optional[int] = ..., grantee_account_id: _Optional[int] = ...) -> None: ...

class RemoveSubaccountMemberResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class UpdateSubaccountMemberRoleRequest(_message.Message):
    __slots__ = ("subaccount_id", "grantee_account_id", "role")
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    GRANTEE_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    grantee_account_id: int
    role: SubaccountRole
    def __init__(self, subaccount_id: _Optional[int] = ..., grantee_account_id: _Optional[int] = ..., role: _Optional[_Union[SubaccountRole, str]] = ...) -> None: ...

class UpdateSubaccountMemberRoleResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SubaccountInvite(_message.Message):
    __slots__ = ("id", "subaccount_id", "grantee_account_id", "inviter_account_id", "role", "status", "created_at", "responded_at", "grantee_username", "inviter_username", "subaccount_label", "inviter_root_smart_account_address", "grantee_root_smart_account_address", "require_member_mfa")
    ID_FIELD_NUMBER: _ClassVar[int]
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    GRANTEE_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    INVITER_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    RESPONDED_AT_FIELD_NUMBER: _ClassVar[int]
    GRANTEE_USERNAME_FIELD_NUMBER: _ClassVar[int]
    INVITER_USERNAME_FIELD_NUMBER: _ClassVar[int]
    SUBACCOUNT_LABEL_FIELD_NUMBER: _ClassVar[int]
    INVITER_ROOT_SMART_ACCOUNT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    GRANTEE_ROOT_SMART_ACCOUNT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    REQUIRE_MEMBER_MFA_FIELD_NUMBER: _ClassVar[int]
    id: int
    subaccount_id: int
    grantee_account_id: int
    inviter_account_id: int
    role: SubaccountRole
    status: SubaccountInviteStatus
    created_at: _timestamp_pb2.Timestamp
    responded_at: _timestamp_pb2.Timestamp
    grantee_username: str
    inviter_username: str
    subaccount_label: str
    inviter_root_smart_account_address: str
    grantee_root_smart_account_address: str
    require_member_mfa: bool
    def __init__(self, id: _Optional[int] = ..., subaccount_id: _Optional[int] = ..., grantee_account_id: _Optional[int] = ..., inviter_account_id: _Optional[int] = ..., role: _Optional[_Union[SubaccountRole, str]] = ..., status: _Optional[_Union[SubaccountInviteStatus, str]] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., responded_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., grantee_username: _Optional[str] = ..., inviter_username: _Optional[str] = ..., subaccount_label: _Optional[str] = ..., inviter_root_smart_account_address: _Optional[str] = ..., grantee_root_smart_account_address: _Optional[str] = ..., require_member_mfa: _Optional[bool] = ...) -> None: ...

class InviteSubaccountMemberRequest(_message.Message):
    __slots__ = ("subaccount_id", "grantee_account_id", "role")
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    GRANTEE_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    grantee_account_id: int
    role: SubaccountRole
    def __init__(self, subaccount_id: _Optional[int] = ..., grantee_account_id: _Optional[int] = ..., role: _Optional[_Union[SubaccountRole, str]] = ...) -> None: ...

class InviteSubaccountMemberResponse(_message.Message):
    __slots__ = ("invite",)
    INVITE_FIELD_NUMBER: _ClassVar[int]
    invite: SubaccountInvite
    def __init__(self, invite: _Optional[_Union[SubaccountInvite, _Mapping]] = ...) -> None: ...

class ListSubaccountInvitesRequest(_message.Message):
    __slots__ = ("direction",)
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    direction: SubaccountInviteDirection
    def __init__(self, direction: _Optional[_Union[SubaccountInviteDirection, str]] = ...) -> None: ...

class ListSubaccountInvitesResponse(_message.Message):
    __slots__ = ("invites",)
    INVITES_FIELD_NUMBER: _ClassVar[int]
    invites: _containers.RepeatedCompositeFieldContainer[SubaccountInvite]
    def __init__(self, invites: _Optional[_Iterable[_Union[SubaccountInvite, _Mapping]]] = ...) -> None: ...

class RespondSubaccountInviteRequest(_message.Message):
    __slots__ = ("invite_id", "action")
    INVITE_ID_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    invite_id: int
    action: SubaccountInviteAction
    def __init__(self, invite_id: _Optional[int] = ..., action: _Optional[_Union[SubaccountInviteAction, str]] = ...) -> None: ...

class RespondSubaccountInviteResponse(_message.Message):
    __slots__ = ("invite",)
    INVITE_FIELD_NUMBER: _ClassVar[int]
    invite: SubaccountInvite
    def __init__(self, invite: _Optional[_Union[SubaccountInvite, _Mapping]] = ...) -> None: ...

class GetSubaccountRequest(_message.Message):
    __slots__ = ("subaccount_id", "include_api_keys", "include_members", "include_invites", "include_policy", "invites_direction")
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_API_KEYS_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_MEMBERS_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_INVITES_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_POLICY_FIELD_NUMBER: _ClassVar[int]
    INVITES_DIRECTION_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    include_api_keys: bool
    include_members: bool
    include_invites: bool
    include_policy: bool
    invites_direction: SubaccountInviteDirection
    def __init__(self, subaccount_id: _Optional[int] = ..., include_api_keys: _Optional[bool] = ..., include_members: _Optional[bool] = ..., include_invites: _Optional[bool] = ..., include_policy: _Optional[bool] = ..., invites_direction: _Optional[_Union[SubaccountInviteDirection, str]] = ...) -> None: ...

class GetSubaccountResponse(_message.Message):
    __slots__ = ("subaccount", "api_keys", "members", "invites", "policy")
    SUBACCOUNT_FIELD_NUMBER: _ClassVar[int]
    API_KEYS_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    INVITES_FIELD_NUMBER: _ClassVar[int]
    POLICY_FIELD_NUMBER: _ClassVar[int]
    subaccount: Subaccount
    api_keys: _containers.RepeatedCompositeFieldContainer[_api_keys_pb2.ApiKey]
    members: _containers.RepeatedCompositeFieldContainer[SubaccountMemberView]
    invites: _containers.RepeatedCompositeFieldContainer[SubaccountInvite]
    policy: _policies_pb2.SubaccountPolicyView
    def __init__(self, subaccount: _Optional[_Union[Subaccount, _Mapping]] = ..., api_keys: _Optional[_Iterable[_Union[_api_keys_pb2.ApiKey, _Mapping]]] = ..., members: _Optional[_Iterable[_Union[SubaccountMemberView, _Mapping]]] = ..., invites: _Optional[_Iterable[_Union[SubaccountInvite, _Mapping]]] = ..., policy: _Optional[_Union[_policies_pb2.SubaccountPolicyView, _Mapping]] = ...) -> None: ...

class ActivityEvent(_message.Message):
    __slots__ = ("created_at", "entity_kind", "event_action", "source", "ip", "user_agent", "actor_account_id", "payload_json")
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    ENTITY_KIND_FIELD_NUMBER: _ClassVar[int]
    EVENT_ACTION_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    IP_FIELD_NUMBER: _ClassVar[int]
    USER_AGENT_FIELD_NUMBER: _ClassVar[int]
    ACTOR_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_JSON_FIELD_NUMBER: _ClassVar[int]
    created_at: _timestamp_pb2.Timestamp
    entity_kind: ActivityEntityKind
    event_action: ActivityEventAction
    source: ActivityEventSource
    ip: str
    user_agent: str
    actor_account_id: int
    payload_json: str
    def __init__(self, created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., entity_kind: _Optional[_Union[ActivityEntityKind, str]] = ..., event_action: _Optional[_Union[ActivityEventAction, str]] = ..., source: _Optional[_Union[ActivityEventSource, str]] = ..., ip: _Optional[str] = ..., user_agent: _Optional[str] = ..., actor_account_id: _Optional[int] = ..., payload_json: _Optional[str] = ...) -> None: ...

class ListSubaccountEventsRequest(_message.Message):
    __slots__ = ("subaccount_id", "limit", "page_token")
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    limit: int
    page_token: str
    def __init__(self, subaccount_id: _Optional[int] = ..., limit: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class ListSubaccountEventsResponse(_message.Message):
    __slots__ = ("events", "next_page_token")
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    events: _containers.RepeatedCompositeFieldContainer[ActivityEvent]
    next_page_token: str
    def __init__(self, events: _Optional[_Iterable[_Union[ActivityEvent, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...
