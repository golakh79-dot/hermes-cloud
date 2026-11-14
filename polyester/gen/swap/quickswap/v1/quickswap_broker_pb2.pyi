import datetime

from polyester.gen.buf.validate import validate_pb2 as _validate_pb2
from polyester.gen.gnostic.openapi.v3 import annotations_pb2 as _annotations_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from polyester.gen.polyester.api import options_pb2 as _options_pb2
from polyester.gen.swap.quickswap.v1 import quickswap_pb2 as _quickswap_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BrokerRole(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BROKER_ROLE_UNSPECIFIED: _ClassVar[BrokerRole]
    OWNER: _ClassVar[BrokerRole]
    ADMIN: _ClassVar[BrokerRole]
    FINANCE: _ClassVar[BrokerRole]
    AFFILIATE_MANAGER: _ClassVar[BrokerRole]
    VIEWER: _ClassVar[BrokerRole]

class VaultStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    VAULT_STATUS_UNSPECIFIED: _ClassVar[VaultStatus]
    VAULT_ACTIVE: _ClassVar[VaultStatus]
    VAULT_DISABLED: _ClassVar[VaultStatus]

class FeeTotalsGrouping(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GROUPING_UNSPECIFIED: _ClassVar[FeeTotalsGrouping]
    BY_VAULT: _ClassVar[FeeTotalsGrouping]
    BY_DAY: _ClassVar[FeeTotalsGrouping]
    BY_MONTH: _ClassVar[FeeTotalsGrouping]

class StatsPeriod(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PERIOD_UNSPECIFIED: _ClassVar[StatsPeriod]
    DAY: _ClassVar[StatsPeriod]
    MONTH: _ClassVar[StatsPeriod]
BROKER_ROLE_UNSPECIFIED: BrokerRole
OWNER: BrokerRole
ADMIN: BrokerRole
FINANCE: BrokerRole
AFFILIATE_MANAGER: BrokerRole
VIEWER: BrokerRole
VAULT_STATUS_UNSPECIFIED: VaultStatus
VAULT_ACTIVE: VaultStatus
VAULT_DISABLED: VaultStatus
GROUPING_UNSPECIFIED: FeeTotalsGrouping
BY_VAULT: FeeTotalsGrouping
BY_DAY: FeeTotalsGrouping
BY_MONTH: FeeTotalsGrouping
PERIOD_UNSPECIFIED: StatsPeriod
DAY: StatsPeriod
MONTH: StatsPeriod

class Broker(_message.Message):
    __slots__ = ("name", "display_name", "enabled", "root_account_id", "default_vault_account_id", "max_affiliate_vaults", "role", "quote_rps", "create_rps", "read_rps", "max_unfunded_addresses", "max_creates_per_hour")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    ROOT_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_VAULT_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    MAX_AFFILIATE_VAULTS_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    QUOTE_RPS_FIELD_NUMBER: _ClassVar[int]
    CREATE_RPS_FIELD_NUMBER: _ClassVar[int]
    READ_RPS_FIELD_NUMBER: _ClassVar[int]
    MAX_UNFUNDED_ADDRESSES_FIELD_NUMBER: _ClassVar[int]
    MAX_CREATES_PER_HOUR_FIELD_NUMBER: _ClassVar[int]
    name: str
    display_name: str
    enabled: bool
    root_account_id: int
    default_vault_account_id: int
    max_affiliate_vaults: int
    role: BrokerRole
    quote_rps: int
    create_rps: int
    read_rps: int
    max_unfunded_addresses: int
    max_creates_per_hour: int
    def __init__(self, name: _Optional[str] = ..., display_name: _Optional[str] = ..., enabled: _Optional[bool] = ..., root_account_id: _Optional[int] = ..., default_vault_account_id: _Optional[int] = ..., max_affiliate_vaults: _Optional[int] = ..., role: _Optional[_Union[BrokerRole, str]] = ..., quote_rps: _Optional[int] = ..., create_rps: _Optional[int] = ..., read_rps: _Optional[int] = ..., max_unfunded_addresses: _Optional[int] = ..., max_creates_per_hour: _Optional[int] = ...) -> None: ...

class BrokerUsage(_message.Message):
    __slots__ = ("unfunded_addresses", "creates_last_hour", "affiliate_vaults")
    UNFUNDED_ADDRESSES_FIELD_NUMBER: _ClassVar[int]
    CREATES_LAST_HOUR_FIELD_NUMBER: _ClassVar[int]
    AFFILIATE_VAULTS_FIELD_NUMBER: _ClassVar[int]
    unfunded_addresses: int
    creates_last_hour: int
    affiliate_vaults: int
    def __init__(self, unfunded_addresses: _Optional[int] = ..., creates_last_hour: _Optional[int] = ..., affiliate_vaults: _Optional[int] = ...) -> None: ...

class AffiliateVault(_message.Message):
    __slots__ = ("account_id", "label", "status", "created_at", "updated_at")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    label: str
    status: VaultStatus
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(self, account_id: _Optional[int] = ..., label: _Optional[str] = ..., status: _Optional[_Union[VaultStatus, str]] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class BrokerKey(_message.Message):
    __slots__ = ("key_id", "label", "created_at", "created_by_account_id", "rotated_from", "expires_at", "revoked_at", "active")
    KEY_ID_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ROTATED_FROM_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    REVOKED_AT_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    key_id: str
    label: str
    created_at: _timestamp_pb2.Timestamp
    created_by_account_id: int
    rotated_from: str
    expires_at: _timestamp_pb2.Timestamp
    revoked_at: _timestamp_pb2.Timestamp
    active: bool
    def __init__(self, key_id: _Optional[str] = ..., label: _Optional[str] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., created_by_account_id: _Optional[int] = ..., rotated_from: _Optional[str] = ..., expires_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., revoked_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., active: _Optional[bool] = ...) -> None: ...

class Member(_message.Message):
    __slots__ = ("account_id", "role", "since")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    SINCE_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    role: BrokerRole
    since: _timestamp_pb2.Timestamp
    def __init__(self, account_id: _Optional[int] = ..., role: _Optional[_Union[BrokerRole, str]] = ..., since: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class Invite(_message.Message):
    __slots__ = ("invite_id", "broker", "broker_display_name", "account_id", "role", "invited_by_account_id", "created_at")
    INVITE_ID_FIELD_NUMBER: _ClassVar[int]
    BROKER_FIELD_NUMBER: _ClassVar[int]
    BROKER_DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    INVITED_BY_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    invite_id: int
    broker: str
    broker_display_name: str
    account_id: int
    role: BrokerRole
    invited_by_account_id: int
    created_at: _timestamp_pb2.Timestamp
    def __init__(self, invite_id: _Optional[int] = ..., broker: _Optional[str] = ..., broker_display_name: _Optional[str] = ..., account_id: _Optional[int] = ..., role: _Optional[_Union[BrokerRole, str]] = ..., invited_by_account_id: _Optional[int] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class Membership(_message.Message):
    __slots__ = ("broker", "broker_display_name", "role")
    BROKER_FIELD_NUMBER: _ClassVar[int]
    BROKER_DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    broker: str
    broker_display_name: str
    role: BrokerRole
    def __init__(self, broker: _Optional[str] = ..., broker_display_name: _Optional[str] = ..., role: _Optional[_Union[BrokerRole, str]] = ...) -> None: ...

class GetBrokerRequest(_message.Message):
    __slots__ = ("broker",)
    BROKER_FIELD_NUMBER: _ClassVar[int]
    broker: str
    def __init__(self, broker: _Optional[str] = ...) -> None: ...

class GetBrokerResponse(_message.Message):
    __slots__ = ("broker", "usage")
    BROKER_FIELD_NUMBER: _ClassVar[int]
    USAGE_FIELD_NUMBER: _ClassVar[int]
    broker: Broker
    usage: BrokerUsage
    def __init__(self, broker: _Optional[_Union[Broker, _Mapping]] = ..., usage: _Optional[_Union[BrokerUsage, _Mapping]] = ...) -> None: ...

class ListMyBrokersRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListMyBrokersResponse(_message.Message):
    __slots__ = ("memberships", "invites")
    MEMBERSHIPS_FIELD_NUMBER: _ClassVar[int]
    INVITES_FIELD_NUMBER: _ClassVar[int]
    memberships: _containers.RepeatedCompositeFieldContainer[Membership]
    invites: _containers.RepeatedCompositeFieldContainer[Invite]
    def __init__(self, memberships: _Optional[_Iterable[_Union[Membership, _Mapping]]] = ..., invites: _Optional[_Iterable[_Union[Invite, _Mapping]]] = ...) -> None: ...

class RespondToInviteRequest(_message.Message):
    __slots__ = ("invite_id", "accept")
    INVITE_ID_FIELD_NUMBER: _ClassVar[int]
    ACCEPT_FIELD_NUMBER: _ClassVar[int]
    invite_id: int
    accept: bool
    def __init__(self, invite_id: _Optional[int] = ..., accept: _Optional[bool] = ...) -> None: ...

class RespondToInviteResponse(_message.Message):
    __slots__ = ("membership",)
    MEMBERSHIP_FIELD_NUMBER: _ClassVar[int]
    membership: Membership
    def __init__(self, membership: _Optional[_Union[Membership, _Mapping]] = ...) -> None: ...

class ListMembersRequest(_message.Message):
    __slots__ = ("broker",)
    BROKER_FIELD_NUMBER: _ClassVar[int]
    broker: str
    def __init__(self, broker: _Optional[str] = ...) -> None: ...

class ListMembersResponse(_message.Message):
    __slots__ = ("members", "invites")
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    INVITES_FIELD_NUMBER: _ClassVar[int]
    members: _containers.RepeatedCompositeFieldContainer[Member]
    invites: _containers.RepeatedCompositeFieldContainer[Invite]
    def __init__(self, members: _Optional[_Iterable[_Union[Member, _Mapping]]] = ..., invites: _Optional[_Iterable[_Union[Invite, _Mapping]]] = ...) -> None: ...

class InviteMemberRequest(_message.Message):
    __slots__ = ("broker", "account_id", "role")
    BROKER_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    broker: str
    account_id: int
    role: BrokerRole
    def __init__(self, broker: _Optional[str] = ..., account_id: _Optional[int] = ..., role: _Optional[_Union[BrokerRole, str]] = ...) -> None: ...

class InviteMemberResponse(_message.Message):
    __slots__ = ("invite",)
    INVITE_FIELD_NUMBER: _ClassVar[int]
    invite: Invite
    def __init__(self, invite: _Optional[_Union[Invite, _Mapping]] = ...) -> None: ...

class SetMemberRoleRequest(_message.Message):
    __slots__ = ("broker", "account_id", "role")
    BROKER_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    broker: str
    account_id: int
    role: BrokerRole
    def __init__(self, broker: _Optional[str] = ..., account_id: _Optional[int] = ..., role: _Optional[_Union[BrokerRole, str]] = ...) -> None: ...

class SetMemberRoleResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class RemoveMemberRequest(_message.Message):
    __slots__ = ("broker", "account_id")
    BROKER_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    broker: str
    account_id: int
    def __init__(self, broker: _Optional[str] = ..., account_id: _Optional[int] = ...) -> None: ...

class RemoveMemberResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class TransferOwnershipRequest(_message.Message):
    __slots__ = ("broker", "account_id")
    BROKER_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    broker: str
    account_id: int
    def __init__(self, broker: _Optional[str] = ..., account_id: _Optional[int] = ...) -> None: ...

class TransferOwnershipResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListKeysRequest(_message.Message):
    __slots__ = ("broker", "limit", "page_token")
    BROKER_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    broker: str
    limit: int
    page_token: str
    def __init__(self, broker: _Optional[str] = ..., limit: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class ListKeysResponse(_message.Message):
    __slots__ = ("keys", "next_page_token")
    KEYS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    keys: _containers.RepeatedCompositeFieldContainer[BrokerKey]
    next_page_token: str
    def __init__(self, keys: _Optional[_Iterable[_Union[BrokerKey, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class CreateKeyRequest(_message.Message):
    __slots__ = ("broker", "label")
    BROKER_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    broker: str
    label: str
    def __init__(self, broker: _Optional[str] = ..., label: _Optional[str] = ...) -> None: ...

class CreateKeyResponse(_message.Message):
    __slots__ = ("key", "token")
    KEY_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    key: BrokerKey
    token: str
    def __init__(self, key: _Optional[_Union[BrokerKey, _Mapping]] = ..., token: _Optional[str] = ...) -> None: ...

class RotateKeyRequest(_message.Message):
    __slots__ = ("broker", "key_id", "overlap_seconds")
    BROKER_FIELD_NUMBER: _ClassVar[int]
    KEY_ID_FIELD_NUMBER: _ClassVar[int]
    OVERLAP_SECONDS_FIELD_NUMBER: _ClassVar[int]
    broker: str
    key_id: str
    overlap_seconds: int
    def __init__(self, broker: _Optional[str] = ..., key_id: _Optional[str] = ..., overlap_seconds: _Optional[int] = ...) -> None: ...

class RotateKeyResponse(_message.Message):
    __slots__ = ("key", "token", "previous_key")
    KEY_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_KEY_FIELD_NUMBER: _ClassVar[int]
    key: BrokerKey
    token: str
    previous_key: BrokerKey
    def __init__(self, key: _Optional[_Union[BrokerKey, _Mapping]] = ..., token: _Optional[str] = ..., previous_key: _Optional[_Union[BrokerKey, _Mapping]] = ...) -> None: ...

class RevokeKeyRequest(_message.Message):
    __slots__ = ("broker", "key_id")
    BROKER_FIELD_NUMBER: _ClassVar[int]
    KEY_ID_FIELD_NUMBER: _ClassVar[int]
    broker: str
    key_id: str
    def __init__(self, broker: _Optional[str] = ..., key_id: _Optional[str] = ...) -> None: ...

class RevokeKeyResponse(_message.Message):
    __slots__ = ("key",)
    KEY_FIELD_NUMBER: _ClassVar[int]
    key: BrokerKey
    def __init__(self, key: _Optional[_Union[BrokerKey, _Mapping]] = ...) -> None: ...

class CreateAffiliateVaultRequest(_message.Message):
    __slots__ = ("broker", "label")
    BROKER_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    broker: str
    label: str
    def __init__(self, broker: _Optional[str] = ..., label: _Optional[str] = ...) -> None: ...

class CreateAffiliateVaultResponse(_message.Message):
    __slots__ = ("vault", "created")
    VAULT_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    vault: AffiliateVault
    created: bool
    def __init__(self, vault: _Optional[_Union[AffiliateVault, _Mapping]] = ..., created: _Optional[bool] = ...) -> None: ...

class ListVaultsRequest(_message.Message):
    __slots__ = ("broker", "limit", "page_token")
    BROKER_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    broker: str
    limit: int
    page_token: str
    def __init__(self, broker: _Optional[str] = ..., limit: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class ListVaultsResponse(_message.Message):
    __slots__ = ("vaults", "next_page_token")
    VAULTS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    vaults: _containers.RepeatedCompositeFieldContainer[AffiliateVault]
    next_page_token: str
    def __init__(self, vaults: _Optional[_Iterable[_Union[AffiliateVault, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class GetVaultRequest(_message.Message):
    __slots__ = ("broker", "account_id")
    BROKER_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    broker: str
    account_id: int
    def __init__(self, broker: _Optional[str] = ..., account_id: _Optional[int] = ...) -> None: ...

class GetVaultResponse(_message.Message):
    __slots__ = ("vault",)
    VAULT_FIELD_NUMBER: _ClassVar[int]
    vault: AffiliateVault
    def __init__(self, vault: _Optional[_Union[AffiliateVault, _Mapping]] = ...) -> None: ...

class SetVaultStatusRequest(_message.Message):
    __slots__ = ("broker", "account_id", "status")
    BROKER_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    broker: str
    account_id: int
    status: VaultStatus
    def __init__(self, broker: _Optional[str] = ..., account_id: _Optional[int] = ..., status: _Optional[_Union[VaultStatus, str]] = ...) -> None: ...

class SetVaultStatusResponse(_message.Message):
    __slots__ = ("vault",)
    VAULT_FIELD_NUMBER: _ClassVar[int]
    vault: AffiliateVault
    def __init__(self, vault: _Optional[_Union[AffiliateVault, _Mapping]] = ...) -> None: ...

class QuickSwapSummary(_message.Message):
    __slots__ = ("swap_id", "idempotency_key", "status", "reason", "is_terminal", "terms", "fees", "charged_fees", "created_at", "updated_at")
    SWAP_ID_FIELD_NUMBER: _ClassVar[int]
    IDEMPOTENCY_KEY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    IS_TERMINAL_FIELD_NUMBER: _ClassVar[int]
    TERMS_FIELD_NUMBER: _ClassVar[int]
    FEES_FIELD_NUMBER: _ClassVar[int]
    CHARGED_FEES_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    swap_id: int
    idempotency_key: str
    status: _quickswap_pb2.QuickSwapStatus
    reason: _quickswap_pb2.QuickSwapReason
    is_terminal: bool
    terms: _quickswap_pb2.QuickSwapTerms
    fees: _quickswap_pb2.RequestedFees
    charged_fees: _containers.RepeatedCompositeFieldContainer[_quickswap_pb2.ChargedFee]
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(self, swap_id: _Optional[int] = ..., idempotency_key: _Optional[str] = ..., status: _Optional[_Union[_quickswap_pb2.QuickSwapStatus, str]] = ..., reason: _Optional[_Union[_quickswap_pb2.QuickSwapReason, str]] = ..., is_terminal: _Optional[bool] = ..., terms: _Optional[_Union[_quickswap_pb2.QuickSwapTerms, _Mapping]] = ..., fees: _Optional[_Union[_quickswap_pb2.RequestedFees, _Mapping]] = ..., charged_fees: _Optional[_Iterable[_Union[_quickswap_pb2.ChargedFee, _Mapping]]] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class QuickSwapBrokerServiceGetQuickSwapRequest(_message.Message):
    __slots__ = ("broker", "swap_id")
    BROKER_FIELD_NUMBER: _ClassVar[int]
    SWAP_ID_FIELD_NUMBER: _ClassVar[int]
    broker: str
    swap_id: int
    def __init__(self, broker: _Optional[str] = ..., swap_id: _Optional[int] = ...) -> None: ...

class QuickSwapBrokerServiceGetQuickSwapResponse(_message.Message):
    __slots__ = ("quick_swap",)
    QUICK_SWAP_FIELD_NUMBER: _ClassVar[int]
    quick_swap: _quickswap_pb2.QuickSwap
    def __init__(self, quick_swap: _Optional[_Union[_quickswap_pb2.QuickSwap, _Mapping]] = ...) -> None: ...

class ListQuickSwapsRequest(_message.Message):
    __slots__ = ("broker", "vault_account_id", "statuses", "start_time", "end_time", "limit", "page_token")
    BROKER_FIELD_NUMBER: _ClassVar[int]
    VAULT_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    STATUSES_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    broker: str
    vault_account_id: int
    statuses: _containers.RepeatedScalarFieldContainer[_quickswap_pb2.QuickSwapStatus]
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    limit: int
    page_token: str
    def __init__(self, broker: _Optional[str] = ..., vault_account_id: _Optional[int] = ..., statuses: _Optional[_Iterable[_Union[_quickswap_pb2.QuickSwapStatus, str]]] = ..., start_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., limit: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class ListQuickSwapsResponse(_message.Message):
    __slots__ = ("quick_swaps", "next_page_token")
    QUICK_SWAPS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    quick_swaps: _containers.RepeatedCompositeFieldContainer[QuickSwapSummary]
    next_page_token: str
    def __init__(self, quick_swaps: _Optional[_Iterable[_Union[QuickSwapSummary, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class GetFeeTotalsRequest(_message.Message):
    __slots__ = ("broker", "group_by", "start_time", "end_time", "vault_account_id")
    BROKER_FIELD_NUMBER: _ClassVar[int]
    GROUP_BY_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    VAULT_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    broker: str
    group_by: FeeTotalsGrouping
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    vault_account_id: int
    def __init__(self, broker: _Optional[str] = ..., group_by: _Optional[_Union[FeeTotalsGrouping, str]] = ..., start_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., vault_account_id: _Optional[int] = ...) -> None: ...

class FeeTotal(_message.Message):
    __slots__ = ("vault_account_id", "period_start", "asset_id", "amount", "swap_count")
    VAULT_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    PERIOD_START_FIELD_NUMBER: _ClassVar[int]
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    SWAP_COUNT_FIELD_NUMBER: _ClassVar[int]
    vault_account_id: int
    period_start: _timestamp_pb2.Timestamp
    asset_id: int
    amount: _quickswap_pb2.TokenAmount
    swap_count: int
    def __init__(self, vault_account_id: _Optional[int] = ..., period_start: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., asset_id: _Optional[int] = ..., amount: _Optional[_Union[_quickswap_pb2.TokenAmount, _Mapping]] = ..., swap_count: _Optional[int] = ...) -> None: ...

class GetFeeTotalsResponse(_message.Message):
    __slots__ = ("totals",)
    TOTALS_FIELD_NUMBER: _ClassVar[int]
    totals: _containers.RepeatedCompositeFieldContainer[FeeTotal]
    def __init__(self, totals: _Optional[_Iterable[_Union[FeeTotal, _Mapping]]] = ...) -> None: ...

class GetBrokerStatsRequest(_message.Message):
    __slots__ = ("broker", "group_by", "start_time", "end_time")
    BROKER_FIELD_NUMBER: _ClassVar[int]
    GROUP_BY_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    broker: str
    group_by: StatsPeriod
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    def __init__(self, broker: _Optional[str] = ..., group_by: _Optional[_Union[StatsPeriod, str]] = ..., start_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class StatusCount(_message.Message):
    __slots__ = ("status", "count")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    status: _quickswap_pb2.QuickSwapStatus
    count: int
    def __init__(self, status: _Optional[_Union[_quickswap_pb2.QuickSwapStatus, str]] = ..., count: _Optional[int] = ...) -> None: ...

class AssetVolume(_message.Message):
    __slots__ = ("asset_id", "amount")
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    asset_id: int
    amount: _quickswap_pb2.TokenAmount
    def __init__(self, asset_id: _Optional[int] = ..., amount: _Optional[_Union[_quickswap_pb2.TokenAmount, _Mapping]] = ...) -> None: ...

class FeeSplit(_message.Message):
    __slots__ = ("asset_id", "service_fee", "broker_fee", "affiliate_fee")
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    SERVICE_FEE_FIELD_NUMBER: _ClassVar[int]
    BROKER_FEE_FIELD_NUMBER: _ClassVar[int]
    AFFILIATE_FEE_FIELD_NUMBER: _ClassVar[int]
    asset_id: int
    service_fee: _quickswap_pb2.TokenAmount
    broker_fee: _quickswap_pb2.TokenAmount
    affiliate_fee: _quickswap_pb2.TokenAmount
    def __init__(self, asset_id: _Optional[int] = ..., service_fee: _Optional[_Union[_quickswap_pb2.TokenAmount, _Mapping]] = ..., broker_fee: _Optional[_Union[_quickswap_pb2.TokenAmount, _Mapping]] = ..., affiliate_fee: _Optional[_Union[_quickswap_pb2.TokenAmount, _Mapping]] = ...) -> None: ...

class BrokerStatsPeriod(_message.Message):
    __slots__ = ("period_start", "created_count", "statuses", "deposited", "delivered", "fees")
    PERIOD_START_FIELD_NUMBER: _ClassVar[int]
    CREATED_COUNT_FIELD_NUMBER: _ClassVar[int]
    STATUSES_FIELD_NUMBER: _ClassVar[int]
    DEPOSITED_FIELD_NUMBER: _ClassVar[int]
    DELIVERED_FIELD_NUMBER: _ClassVar[int]
    FEES_FIELD_NUMBER: _ClassVar[int]
    period_start: _timestamp_pb2.Timestamp
    created_count: int
    statuses: _containers.RepeatedCompositeFieldContainer[StatusCount]
    deposited: _containers.RepeatedCompositeFieldContainer[AssetVolume]
    delivered: _containers.RepeatedCompositeFieldContainer[AssetVolume]
    fees: _containers.RepeatedCompositeFieldContainer[FeeSplit]
    def __init__(self, period_start: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., created_count: _Optional[int] = ..., statuses: _Optional[_Iterable[_Union[StatusCount, _Mapping]]] = ..., deposited: _Optional[_Iterable[_Union[AssetVolume, _Mapping]]] = ..., delivered: _Optional[_Iterable[_Union[AssetVolume, _Mapping]]] = ..., fees: _Optional[_Iterable[_Union[FeeSplit, _Mapping]]] = ...) -> None: ...

class GetBrokerStatsResponse(_message.Message):
    __slots__ = ("periods",)
    PERIODS_FIELD_NUMBER: _ClassVar[int]
    periods: _containers.RepeatedCompositeFieldContainer[BrokerStatsPeriod]
    def __init__(self, periods: _Optional[_Iterable[_Union[BrokerStatsPeriod, _Mapping]]] = ...) -> None: ...
