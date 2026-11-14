import datetime

from polyester.gen.auth.v1 import subaccounts_pb2 as _subaccounts_pb2
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

class AccountScopeType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SCOPE_UNSPECIFIED: _ClassVar[AccountScopeType]
    SCOPE_ROOT: _ClassVar[AccountScopeType]
    SCOPE_SUBACCOUNT: _ClassVar[AccountScopeType]

class AddressBookEntryKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ENTRY_KIND_UNSPECIFIED: _ClassVar[AddressBookEntryKind]
    EXTERNAL_CHAIN: _ClassVar[AddressBookEntryKind]
    INTERNAL_ACCOUNT: _ClassVar[AddressBookEntryKind]

class InternalWhitelistResolutionStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INTERNAL_WHITELIST_RESOLUTION_UNSPECIFIED: _ClassVar[InternalWhitelistResolutionStatus]
    INTERNAL_WHITELIST_RESOLVED: _ClassVar[InternalWhitelistResolutionStatus]
    INTERNAL_WHITELIST_UNRESOLVED: _ClassVar[InternalWhitelistResolutionStatus]

class DestinationWhitelistStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DESTINATION_WHITELIST_STATUS_UNSPECIFIED: _ClassVar[DestinationWhitelistStatus]
    DESTINATION_NOT_WHITELISTED: _ClassVar[DestinationWhitelistStatus]
    DESTINATION_WHITELIST_ACTIVE: _ClassVar[DestinationWhitelistStatus]
    DESTINATION_WHITELIST_UNRESOLVED: _ClassVar[DestinationWhitelistStatus]

class TransferCounterpartyDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TRANSFER_COUNTERPARTY_DIRECTION_UNSPECIFIED: _ClassVar[TransferCounterpartyDirection]
    DEPOSIT_FROM: _ClassVar[TransferCounterpartyDirection]
    WITHDRAW_TO: _ClassVar[TransferCounterpartyDirection]
    INTERNAL_TRANSFER_FROM: _ClassVar[TransferCounterpartyDirection]
    INTERNAL_TRANSFER_TO: _ClassVar[TransferCounterpartyDirection]
SCOPE_UNSPECIFIED: AccountScopeType
SCOPE_ROOT: AccountScopeType
SCOPE_SUBACCOUNT: AccountScopeType
ENTRY_KIND_UNSPECIFIED: AddressBookEntryKind
EXTERNAL_CHAIN: AddressBookEntryKind
INTERNAL_ACCOUNT: AddressBookEntryKind
INTERNAL_WHITELIST_RESOLUTION_UNSPECIFIED: InternalWhitelistResolutionStatus
INTERNAL_WHITELIST_RESOLVED: InternalWhitelistResolutionStatus
INTERNAL_WHITELIST_UNRESOLVED: InternalWhitelistResolutionStatus
DESTINATION_WHITELIST_STATUS_UNSPECIFIED: DestinationWhitelistStatus
DESTINATION_NOT_WHITELISTED: DestinationWhitelistStatus
DESTINATION_WHITELIST_ACTIVE: DestinationWhitelistStatus
DESTINATION_WHITELIST_UNRESOLVED: DestinationWhitelistStatus
TRANSFER_COUNTERPARTY_DIRECTION_UNSPECIFIED: TransferCounterpartyDirection
DEPOSIT_FROM: TransferCounterpartyDirection
WITHDRAW_TO: TransferCounterpartyDirection
INTERNAL_TRANSFER_FROM: TransferCounterpartyDirection
INTERNAL_TRANSFER_TO: TransferCounterpartyDirection

class AccountScopeRef(_message.Message):
    __slots__ = ("scope_type", "root_account_id", "subaccount_id")
    SCOPE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ROOT_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    scope_type: AccountScopeType
    root_account_id: int
    subaccount_id: int
    def __init__(self, scope_type: _Optional[_Union[AccountScopeType, str]] = ..., root_account_id: _Optional[int] = ..., subaccount_id: _Optional[int] = ...) -> None: ...

class AddressBook(_message.Message):
    __slots__ = ("scope", "caller_role", "label", "owner_username", "smart_account_address")
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    CALLER_ROLE_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    OWNER_USERNAME_FIELD_NUMBER: _ClassVar[int]
    SMART_ACCOUNT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    scope: AccountScopeRef
    caller_role: _subaccounts_pb2.SubaccountRole
    label: str
    owner_username: str
    smart_account_address: str
    def __init__(self, scope: _Optional[_Union[AccountScopeRef, _Mapping]] = ..., caller_role: _Optional[_Union[_subaccounts_pb2.SubaccountRole, str]] = ..., label: _Optional[str] = ..., owner_username: _Optional[str] = ..., smart_account_address: _Optional[str] = ...) -> None: ...

class ExternalWithdrawAddress(_message.Message):
    __slots__ = ("polychain_chain_id", "address")
    POLYCHAIN_CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    polychain_chain_id: int
    address: str
    def __init__(self, polychain_chain_id: _Optional[int] = ..., address: _Optional[str] = ...) -> None: ...

class InternalTransferAccount(_message.Message):
    __slots__ = ("root_account_id", "target_account_id", "target_scope_type", "smart_account_address", "root_username", "subaccount_label")
    ROOT_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_SCOPE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SMART_ACCOUNT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    ROOT_USERNAME_FIELD_NUMBER: _ClassVar[int]
    SUBACCOUNT_LABEL_FIELD_NUMBER: _ClassVar[int]
    root_account_id: int
    target_account_id: int
    target_scope_type: AccountScopeType
    smart_account_address: str
    root_username: str
    subaccount_label: str
    def __init__(self, root_account_id: _Optional[int] = ..., target_account_id: _Optional[int] = ..., target_scope_type: _Optional[_Union[AccountScopeType, str]] = ..., smart_account_address: _Optional[str] = ..., root_username: _Optional[str] = ..., subaccount_label: _Optional[str] = ...) -> None: ...

class AddressBookTag(_message.Message):
    __slots__ = ("tag_id", "scope", "name", "color", "created_at", "updated_at")
    TAG_ID_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    tag_id: int
    scope: AccountScopeRef
    name: str
    color: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(self, tag_id: _Optional[int] = ..., scope: _Optional[_Union[AccountScopeRef, _Mapping]] = ..., name: _Optional[str] = ..., color: _Optional[str] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class AddressBookTagSummary(_message.Message):
    __slots__ = ("tag_id", "name", "color")
    TAG_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    tag_id: int
    name: str
    color: str
    def __init__(self, tag_id: _Optional[int] = ..., name: _Optional[str] = ..., color: _Optional[str] = ...) -> None: ...

class AddressBookEntry(_message.Message):
    __slots__ = ("address_book_entry_id", "scope", "kind", "label", "note", "created_at", "updated_at", "external", "internal", "tags", "revision")
    ADDRESS_BOOK_ENTRY_ID_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    NOTE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_FIELD_NUMBER: _ClassVar[int]
    INTERNAL_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    REVISION_FIELD_NUMBER: _ClassVar[int]
    address_book_entry_id: int
    scope: AccountScopeRef
    kind: AddressBookEntryKind
    label: str
    note: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    external: ExternalWithdrawAddress
    internal: InternalTransferAccount
    tags: _containers.RepeatedCompositeFieldContainer[AddressBookTag]
    revision: int
    def __init__(self, address_book_entry_id: _Optional[int] = ..., scope: _Optional[_Union[AccountScopeRef, _Mapping]] = ..., kind: _Optional[_Union[AddressBookEntryKind, str]] = ..., label: _Optional[str] = ..., note: _Optional[str] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., external: _Optional[_Union[ExternalWithdrawAddress, _Mapping]] = ..., internal: _Optional[_Union[InternalTransferAccount, _Mapping]] = ..., tags: _Optional[_Iterable[_Union[AddressBookTag, _Mapping]]] = ..., revision: _Optional[int] = ...) -> None: ...

class AddressBookEntriesView(_message.Message):
    __slots__ = ("external", "internal")
    EXTERNAL_FIELD_NUMBER: _ClassVar[int]
    INTERNAL_FIELD_NUMBER: _ClassVar[int]
    external: _containers.RepeatedCompositeFieldContainer[ExternalAddressBookEntry]
    internal: _containers.RepeatedCompositeFieldContainer[InternalAddressBookEntry]
    def __init__(self, external: _Optional[_Iterable[_Union[ExternalAddressBookEntry, _Mapping]]] = ..., internal: _Optional[_Iterable[_Union[InternalAddressBookEntry, _Mapping]]] = ...) -> None: ...

class ExternalAddressBookEntry(_message.Message):
    __slots__ = ("address_book_entry_id", "scope", "label", "note", "tag_ids", "whitelist_status", "polychain_chain_id", "address", "created_at", "updated_at", "revision")
    ADDRESS_BOOK_ENTRY_ID_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    NOTE_FIELD_NUMBER: _ClassVar[int]
    TAG_IDS_FIELD_NUMBER: _ClassVar[int]
    WHITELIST_STATUS_FIELD_NUMBER: _ClassVar[int]
    POLYCHAIN_CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    REVISION_FIELD_NUMBER: _ClassVar[int]
    address_book_entry_id: int
    scope: AccountScopeRef
    label: str
    note: str
    tag_ids: _containers.RepeatedScalarFieldContainer[int]
    whitelist_status: DestinationWhitelistStatus
    polychain_chain_id: int
    address: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    revision: int
    def __init__(self, address_book_entry_id: _Optional[int] = ..., scope: _Optional[_Union[AccountScopeRef, _Mapping]] = ..., label: _Optional[str] = ..., note: _Optional[str] = ..., tag_ids: _Optional[_Iterable[int]] = ..., whitelist_status: _Optional[_Union[DestinationWhitelistStatus, str]] = ..., polychain_chain_id: _Optional[int] = ..., address: _Optional[str] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., revision: _Optional[int] = ...) -> None: ...

class InternalAddressBookEntry(_message.Message):
    __slots__ = ("address_book_entry_id", "scope", "label", "note", "tag_ids", "whitelist_status", "root_account_id", "target_account_id", "target_scope_type", "smart_account_address", "root_username", "subaccount_label", "created_at", "updated_at", "revision")
    ADDRESS_BOOK_ENTRY_ID_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    NOTE_FIELD_NUMBER: _ClassVar[int]
    TAG_IDS_FIELD_NUMBER: _ClassVar[int]
    WHITELIST_STATUS_FIELD_NUMBER: _ClassVar[int]
    ROOT_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_SCOPE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SMART_ACCOUNT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    ROOT_USERNAME_FIELD_NUMBER: _ClassVar[int]
    SUBACCOUNT_LABEL_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    REVISION_FIELD_NUMBER: _ClassVar[int]
    address_book_entry_id: int
    scope: AccountScopeRef
    label: str
    note: str
    tag_ids: _containers.RepeatedScalarFieldContainer[int]
    whitelist_status: DestinationWhitelistStatus
    root_account_id: int
    target_account_id: int
    target_scope_type: AccountScopeType
    smart_account_address: str
    root_username: str
    subaccount_label: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    revision: int
    def __init__(self, address_book_entry_id: _Optional[int] = ..., scope: _Optional[_Union[AccountScopeRef, _Mapping]] = ..., label: _Optional[str] = ..., note: _Optional[str] = ..., tag_ids: _Optional[_Iterable[int]] = ..., whitelist_status: _Optional[_Union[DestinationWhitelistStatus, str]] = ..., root_account_id: _Optional[int] = ..., target_account_id: _Optional[int] = ..., target_scope_type: _Optional[_Union[AccountScopeType, str]] = ..., smart_account_address: _Optional[str] = ..., root_username: _Optional[str] = ..., subaccount_label: _Optional[str] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., revision: _Optional[int] = ...) -> None: ...

class TransferCounterparty(_message.Message):
    __slots__ = ("counterparty_id", "scope", "direction", "kind", "saved", "address_book_entry_id", "use_count", "first_seen_at", "last_seen_at", "external", "internal")
    COUNTERPARTY_ID_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    SAVED_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_BOOK_ENTRY_ID_FIELD_NUMBER: _ClassVar[int]
    USE_COUNT_FIELD_NUMBER: _ClassVar[int]
    FIRST_SEEN_AT_FIELD_NUMBER: _ClassVar[int]
    LAST_SEEN_AT_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_FIELD_NUMBER: _ClassVar[int]
    INTERNAL_FIELD_NUMBER: _ClassVar[int]
    counterparty_id: int
    scope: AccountScopeRef
    direction: TransferCounterpartyDirection
    kind: AddressBookEntryKind
    saved: bool
    address_book_entry_id: int
    use_count: int
    first_seen_at: _timestamp_pb2.Timestamp
    last_seen_at: _timestamp_pb2.Timestamp
    external: ExternalWithdrawAddress
    internal: InternalTransferAccount
    def __init__(self, counterparty_id: _Optional[int] = ..., scope: _Optional[_Union[AccountScopeRef, _Mapping]] = ..., direction: _Optional[_Union[TransferCounterpartyDirection, str]] = ..., kind: _Optional[_Union[AddressBookEntryKind, str]] = ..., saved: _Optional[bool] = ..., address_book_entry_id: _Optional[int] = ..., use_count: _Optional[int] = ..., first_seen_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., last_seen_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., external: _Optional[_Union[ExternalWithdrawAddress, _Mapping]] = ..., internal: _Optional[_Union[InternalTransferAccount, _Mapping]] = ...) -> None: ...

class AddressBookRecentDestinationsView(_message.Message):
    __slots__ = ("external", "internal")
    EXTERNAL_FIELD_NUMBER: _ClassVar[int]
    INTERNAL_FIELD_NUMBER: _ClassVar[int]
    external: _containers.RepeatedCompositeFieldContainer[ExternalRecentDestination]
    internal: _containers.RepeatedCompositeFieldContainer[InternalRecentDestination]
    def __init__(self, external: _Optional[_Iterable[_Union[ExternalRecentDestination, _Mapping]]] = ..., internal: _Optional[_Iterable[_Union[InternalRecentDestination, _Mapping]]] = ...) -> None: ...

class ExternalRecentDestination(_message.Message):
    __slots__ = ("scope", "last_direction", "saved", "address_book_entry_id", "use_count", "last_seen_at", "polychain_chain_id", "address")
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    LAST_DIRECTION_FIELD_NUMBER: _ClassVar[int]
    SAVED_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_BOOK_ENTRY_ID_FIELD_NUMBER: _ClassVar[int]
    USE_COUNT_FIELD_NUMBER: _ClassVar[int]
    LAST_SEEN_AT_FIELD_NUMBER: _ClassVar[int]
    POLYCHAIN_CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    scope: AccountScopeRef
    last_direction: TransferCounterpartyDirection
    saved: bool
    address_book_entry_id: int
    use_count: int
    last_seen_at: _timestamp_pb2.Timestamp
    polychain_chain_id: int
    address: str
    def __init__(self, scope: _Optional[_Union[AccountScopeRef, _Mapping]] = ..., last_direction: _Optional[_Union[TransferCounterpartyDirection, str]] = ..., saved: _Optional[bool] = ..., address_book_entry_id: _Optional[int] = ..., use_count: _Optional[int] = ..., last_seen_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., polychain_chain_id: _Optional[int] = ..., address: _Optional[str] = ...) -> None: ...

class InternalRecentDestination(_message.Message):
    __slots__ = ("scope", "last_direction", "saved", "address_book_entry_id", "use_count", "last_seen_at", "root_account_id", "target_account_id", "target_scope_type", "smart_account_address", "root_username", "subaccount_label")
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    LAST_DIRECTION_FIELD_NUMBER: _ClassVar[int]
    SAVED_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_BOOK_ENTRY_ID_FIELD_NUMBER: _ClassVar[int]
    USE_COUNT_FIELD_NUMBER: _ClassVar[int]
    LAST_SEEN_AT_FIELD_NUMBER: _ClassVar[int]
    ROOT_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_SCOPE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SMART_ACCOUNT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    ROOT_USERNAME_FIELD_NUMBER: _ClassVar[int]
    SUBACCOUNT_LABEL_FIELD_NUMBER: _ClassVar[int]
    scope: AccountScopeRef
    last_direction: TransferCounterpartyDirection
    saved: bool
    address_book_entry_id: int
    use_count: int
    last_seen_at: _timestamp_pb2.Timestamp
    root_account_id: int
    target_account_id: int
    target_scope_type: AccountScopeType
    smart_account_address: str
    root_username: str
    subaccount_label: str
    def __init__(self, scope: _Optional[_Union[AccountScopeRef, _Mapping]] = ..., last_direction: _Optional[_Union[TransferCounterpartyDirection, str]] = ..., saved: _Optional[bool] = ..., address_book_entry_id: _Optional[int] = ..., use_count: _Optional[int] = ..., last_seen_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., root_account_id: _Optional[int] = ..., target_account_id: _Optional[int] = ..., target_scope_type: _Optional[_Union[AccountScopeType, str]] = ..., smart_account_address: _Optional[str] = ..., root_username: _Optional[str] = ..., subaccount_label: _Optional[str] = ...) -> None: ...

class InternalTransferWhitelistEntry(_message.Message):
    __slots__ = ("entry_id", "scope", "root_account_id", "target_account_id", "target_scope_type", "smart_account_address", "root_username", "subaccount_label", "created_at", "updated_at", "resolution_status")
    ENTRY_ID_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    ROOT_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_SCOPE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SMART_ACCOUNT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    ROOT_USERNAME_FIELD_NUMBER: _ClassVar[int]
    SUBACCOUNT_LABEL_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    RESOLUTION_STATUS_FIELD_NUMBER: _ClassVar[int]
    entry_id: int
    scope: AccountScopeRef
    root_account_id: int
    target_account_id: int
    target_scope_type: AccountScopeType
    smart_account_address: str
    root_username: str
    subaccount_label: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    resolution_status: InternalWhitelistResolutionStatus
    def __init__(self, entry_id: _Optional[int] = ..., scope: _Optional[_Union[AccountScopeRef, _Mapping]] = ..., root_account_id: _Optional[int] = ..., target_account_id: _Optional[int] = ..., target_scope_type: _Optional[_Union[AccountScopeType, str]] = ..., smart_account_address: _Optional[str] = ..., root_username: _Optional[str] = ..., subaccount_label: _Optional[str] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., resolution_status: _Optional[_Union[InternalWhitelistResolutionStatus, str]] = ...) -> None: ...

class MirroredWithdrawWhitelistEntry(_message.Message):
    __slots__ = ("canonical_address", "raw_address_hex", "updated_at", "polychain_chain_id")
    CANONICAL_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    RAW_ADDRESS_HEX_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    POLYCHAIN_CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    canonical_address: str
    raw_address_hex: str
    updated_at: _timestamp_pb2.Timestamp
    polychain_chain_id: int
    def __init__(self, canonical_address: _Optional[str] = ..., raw_address_hex: _Optional[str] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., polychain_chain_id: _Optional[int] = ...) -> None: ...

class WithdrawWhitelistView(_message.Message):
    __slots__ = ("scope", "external_whitelist_required", "active_entries", "internal_whitelist_required")
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_WHITELIST_REQUIRED_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_ENTRIES_FIELD_NUMBER: _ClassVar[int]
    INTERNAL_WHITELIST_REQUIRED_FIELD_NUMBER: _ClassVar[int]
    scope: AccountScopeRef
    external_whitelist_required: bool
    active_entries: _containers.RepeatedCompositeFieldContainer[MirroredWithdrawWhitelistEntry]
    internal_whitelist_required: bool
    def __init__(self, scope: _Optional[_Union[AccountScopeRef, _Mapping]] = ..., external_whitelist_required: _Optional[bool] = ..., active_entries: _Optional[_Iterable[_Union[MirroredWithdrawWhitelistEntry, _Mapping]]] = ..., internal_whitelist_required: _Optional[bool] = ...) -> None: ...

class TransferDestination(_message.Message):
    __slots__ = ("scope", "kind", "saved", "whitelisted", "whitelist_status", "address_book_entry", "external", "internal", "whitelist_updated_at")
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    SAVED_FIELD_NUMBER: _ClassVar[int]
    WHITELISTED_FIELD_NUMBER: _ClassVar[int]
    WHITELIST_STATUS_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_BOOK_ENTRY_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_FIELD_NUMBER: _ClassVar[int]
    INTERNAL_FIELD_NUMBER: _ClassVar[int]
    WHITELIST_UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    scope: AccountScopeRef
    kind: AddressBookEntryKind
    saved: bool
    whitelisted: bool
    whitelist_status: DestinationWhitelistStatus
    address_book_entry: AddressBookEntry
    external: ExternalWithdrawAddress
    internal: InternalTransferAccount
    whitelist_updated_at: _timestamp_pb2.Timestamp
    def __init__(self, scope: _Optional[_Union[AccountScopeRef, _Mapping]] = ..., kind: _Optional[_Union[AddressBookEntryKind, str]] = ..., saved: _Optional[bool] = ..., whitelisted: _Optional[bool] = ..., whitelist_status: _Optional[_Union[DestinationWhitelistStatus, str]] = ..., address_book_entry: _Optional[_Union[AddressBookEntry, _Mapping]] = ..., external: _Optional[_Union[ExternalWithdrawAddress, _Mapping]] = ..., internal: _Optional[_Union[InternalTransferAccount, _Mapping]] = ..., whitelist_updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ListAddressBooksRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListAddressBooksResponse(_message.Message):
    __slots__ = ("books",)
    BOOKS_FIELD_NUMBER: _ClassVar[int]
    books: _containers.RepeatedCompositeFieldContainer[AddressBook]
    def __init__(self, books: _Optional[_Iterable[_Union[AddressBook, _Mapping]]] = ...) -> None: ...

class ListAddressBookEntriesRequest(_message.Message):
    __slots__ = ("subaccount_id", "kind", "limit", "page_token")
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    kind: AddressBookEntryKind
    limit: int
    page_token: str
    def __init__(self, subaccount_id: _Optional[int] = ..., kind: _Optional[_Union[AddressBookEntryKind, str]] = ..., limit: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class ListAddressBookEntriesResponse(_message.Message):
    __slots__ = ("entries", "next_page_token")
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[AddressBookEntry]
    next_page_token: str
    def __init__(self, entries: _Optional[_Iterable[_Union[AddressBookEntry, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class CreateAddressBookEntryRequest(_message.Message):
    __slots__ = ("subaccount_id", "label", "note", "external", "internal", "tag_ids", "new_tags")
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    NOTE_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_FIELD_NUMBER: _ClassVar[int]
    INTERNAL_FIELD_NUMBER: _ClassVar[int]
    TAG_IDS_FIELD_NUMBER: _ClassVar[int]
    NEW_TAGS_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    label: str
    note: str
    external: ExternalWithdrawAddress
    internal: RequestedInternalTransferAccount
    tag_ids: _containers.RepeatedScalarFieldContainer[int]
    new_tags: _containers.RepeatedCompositeFieldContainer[AddressBookTagInput]
    def __init__(self, subaccount_id: _Optional[int] = ..., label: _Optional[str] = ..., note: _Optional[str] = ..., external: _Optional[_Union[ExternalWithdrawAddress, _Mapping]] = ..., internal: _Optional[_Union[RequestedInternalTransferAccount, _Mapping]] = ..., tag_ids: _Optional[_Iterable[int]] = ..., new_tags: _Optional[_Iterable[_Union[AddressBookTagInput, _Mapping]]] = ...) -> None: ...

class RequestedInternalTransferAccount(_message.Message):
    __slots__ = ("smart_account_address",)
    SMART_ACCOUNT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    smart_account_address: str
    def __init__(self, smart_account_address: _Optional[str] = ...) -> None: ...

class CreateAddressBookEntryResponse(_message.Message):
    __slots__ = ("entry",)
    ENTRY_FIELD_NUMBER: _ClassVar[int]
    entry: AddressBookEntry
    def __init__(self, entry: _Optional[_Union[AddressBookEntry, _Mapping]] = ...) -> None: ...

class AddressBookEntryUpdateSpec(_message.Message):
    __slots__ = ("label", "note", "tag_ids", "new_tags")
    LABEL_FIELD_NUMBER: _ClassVar[int]
    NOTE_FIELD_NUMBER: _ClassVar[int]
    TAG_IDS_FIELD_NUMBER: _ClassVar[int]
    NEW_TAGS_FIELD_NUMBER: _ClassVar[int]
    label: str
    note: str
    tag_ids: _containers.RepeatedScalarFieldContainer[int]
    new_tags: _containers.RepeatedCompositeFieldContainer[AddressBookTagInput]
    def __init__(self, label: _Optional[str] = ..., note: _Optional[str] = ..., tag_ids: _Optional[_Iterable[int]] = ..., new_tags: _Optional[_Iterable[_Union[AddressBookTagInput, _Mapping]]] = ...) -> None: ...

class UpdateAddressBookEntryRequest(_message.Message):
    __slots__ = ("address_book_entry_id", "entry", "update_mask", "expected_revision")
    ADDRESS_BOOK_ENTRY_ID_FIELD_NUMBER: _ClassVar[int]
    ENTRY_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_REVISION_FIELD_NUMBER: _ClassVar[int]
    address_book_entry_id: int
    entry: AddressBookEntryUpdateSpec
    update_mask: _field_mask_pb2.FieldMask
    expected_revision: int
    def __init__(self, address_book_entry_id: _Optional[int] = ..., entry: _Optional[_Union[AddressBookEntryUpdateSpec, _Mapping]] = ..., update_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ..., expected_revision: _Optional[int] = ...) -> None: ...

class UpdateAddressBookEntryResponse(_message.Message):
    __slots__ = ("entry",)
    ENTRY_FIELD_NUMBER: _ClassVar[int]
    entry: AddressBookEntry
    def __init__(self, entry: _Optional[_Union[AddressBookEntry, _Mapping]] = ...) -> None: ...

class AddressBookTagInput(_message.Message):
    __slots__ = ("name", "color")
    NAME_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    name: str
    color: str
    def __init__(self, name: _Optional[str] = ..., color: _Optional[str] = ...) -> None: ...

class DeleteAddressBookEntryRequest(_message.Message):
    __slots__ = ("address_book_entry_id",)
    ADDRESS_BOOK_ENTRY_ID_FIELD_NUMBER: _ClassVar[int]
    address_book_entry_id: int
    def __init__(self, address_book_entry_id: _Optional[int] = ...) -> None: ...

class DeleteAddressBookEntryResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CopyAddressBookEntryRequest(_message.Message):
    __slots__ = ("address_book_entry_id", "target_subaccount_id")
    ADDRESS_BOOK_ENTRY_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    address_book_entry_id: int
    target_subaccount_id: int
    def __init__(self, address_book_entry_id: _Optional[int] = ..., target_subaccount_id: _Optional[int] = ...) -> None: ...

class CopyAddressBookEntryResponse(_message.Message):
    __slots__ = ("entry",)
    ENTRY_FIELD_NUMBER: _ClassVar[int]
    entry: AddressBookEntry
    def __init__(self, entry: _Optional[_Union[AddressBookEntry, _Mapping]] = ...) -> None: ...

class CreateAddressBookTagRequest(_message.Message):
    __slots__ = ("subaccount_id", "name", "color")
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    name: str
    color: str
    def __init__(self, subaccount_id: _Optional[int] = ..., name: _Optional[str] = ..., color: _Optional[str] = ...) -> None: ...

class CreateAddressBookTagResponse(_message.Message):
    __slots__ = ("tag",)
    TAG_FIELD_NUMBER: _ClassVar[int]
    tag: AddressBookTag
    def __init__(self, tag: _Optional[_Union[AddressBookTag, _Mapping]] = ...) -> None: ...

class UpdateAddressBookTagRequest(_message.Message):
    __slots__ = ("tag_id", "name", "color")
    TAG_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    tag_id: int
    name: str
    color: str
    def __init__(self, tag_id: _Optional[int] = ..., name: _Optional[str] = ..., color: _Optional[str] = ...) -> None: ...

class UpdateAddressBookTagResponse(_message.Message):
    __slots__ = ("tag",)
    TAG_FIELD_NUMBER: _ClassVar[int]
    tag: AddressBookTag
    def __init__(self, tag: _Optional[_Union[AddressBookTag, _Mapping]] = ...) -> None: ...

class DeleteAddressBookTagRequest(_message.Message):
    __slots__ = ("tag_id",)
    TAG_ID_FIELD_NUMBER: _ClassVar[int]
    tag_id: int
    def __init__(self, tag_id: _Optional[int] = ...) -> None: ...

class DeleteAddressBookTagResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListTransferCounterpartiesRequest(_message.Message):
    __slots__ = ("subaccount_id", "direction", "kind", "limit")
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    direction: TransferCounterpartyDirection
    kind: AddressBookEntryKind
    limit: int
    def __init__(self, subaccount_id: _Optional[int] = ..., direction: _Optional[_Union[TransferCounterpartyDirection, str]] = ..., kind: _Optional[_Union[AddressBookEntryKind, str]] = ..., limit: _Optional[int] = ...) -> None: ...

class ListTransferCounterpartiesResponse(_message.Message):
    __slots__ = ("counterparties", "truncated")
    COUNTERPARTIES_FIELD_NUMBER: _ClassVar[int]
    TRUNCATED_FIELD_NUMBER: _ClassVar[int]
    counterparties: _containers.RepeatedCompositeFieldContainer[TransferCounterparty]
    truncated: bool
    def __init__(self, counterparties: _Optional[_Iterable[_Union[TransferCounterparty, _Mapping]]] = ..., truncated: _Optional[bool] = ...) -> None: ...

class ListTransferDestinationsRequest(_message.Message):
    __slots__ = ("subaccount_id", "kind", "limit", "page_token")
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    kind: AddressBookEntryKind
    limit: int
    page_token: str
    def __init__(self, subaccount_id: _Optional[int] = ..., kind: _Optional[_Union[AddressBookEntryKind, str]] = ..., limit: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class ListTransferDestinationsResponse(_message.Message):
    __slots__ = ("destinations", "next_page_token")
    DESTINATIONS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    destinations: _containers.RepeatedCompositeFieldContainer[TransferDestination]
    next_page_token: str
    def __init__(self, destinations: _Optional[_Iterable[_Union[TransferDestination, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class ListInternalTransferWhitelistEntriesRequest(_message.Message):
    __slots__ = ("subaccount_id", "limit", "page_token")
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    limit: int
    page_token: str
    def __init__(self, subaccount_id: _Optional[int] = ..., limit: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class ListInternalTransferWhitelistEntriesResponse(_message.Message):
    __slots__ = ("entries", "next_page_token")
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[InternalTransferWhitelistEntry]
    next_page_token: str
    def __init__(self, entries: _Optional[_Iterable[_Union[InternalTransferWhitelistEntry, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class GetWithdrawWhitelistViewRequest(_message.Message):
    __slots__ = ("subaccount_id",)
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    def __init__(self, subaccount_id: _Optional[int] = ...) -> None: ...

class GetWithdrawWhitelistViewResponse(_message.Message):
    __slots__ = ("view",)
    VIEW_FIELD_NUMBER: _ClassVar[int]
    view: WithdrawWhitelistView
    def __init__(self, view: _Optional[_Union[WithdrawWhitelistView, _Mapping]] = ...) -> None: ...

class GetAddressBookViewRequest(_message.Message):
    __slots__ = ("subaccount_id", "limit", "minimum_view_revision")
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    MINIMUM_VIEW_REVISION_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    limit: int
    minimum_view_revision: int
    def __init__(self, subaccount_id: _Optional[int] = ..., limit: _Optional[int] = ..., minimum_view_revision: _Optional[int] = ...) -> None: ...

class GetAddressBookViewResponse(_message.Message):
    __slots__ = ("books", "entries", "recent_destinations", "tags", "withdraw_whitelist", "recent_destinations_truncated", "view_revision")
    BOOKS_FIELD_NUMBER: _ClassVar[int]
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    RECENT_DESTINATIONS_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    WITHDRAW_WHITELIST_FIELD_NUMBER: _ClassVar[int]
    RECENT_DESTINATIONS_TRUNCATED_FIELD_NUMBER: _ClassVar[int]
    VIEW_REVISION_FIELD_NUMBER: _ClassVar[int]
    books: _containers.RepeatedCompositeFieldContainer[AddressBook]
    entries: AddressBookEntriesView
    recent_destinations: AddressBookRecentDestinationsView
    tags: _containers.RepeatedCompositeFieldContainer[AddressBookTagSummary]
    withdraw_whitelist: WithdrawWhitelistView
    recent_destinations_truncated: bool
    view_revision: int
    def __init__(self, books: _Optional[_Iterable[_Union[AddressBook, _Mapping]]] = ..., entries: _Optional[_Union[AddressBookEntriesView, _Mapping]] = ..., recent_destinations: _Optional[_Union[AddressBookRecentDestinationsView, _Mapping]] = ..., tags: _Optional[_Iterable[_Union[AddressBookTagSummary, _Mapping]]] = ..., withdraw_whitelist: _Optional[_Union[WithdrawWhitelistView, _Mapping]] = ..., recent_destinations_truncated: _Optional[bool] = ..., view_revision: _Optional[int] = ...) -> None: ...

class AddressBookViewInvalidated(_message.Message):
    __slots__ = ("scope", "invalidated_at", "view_revision")
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    INVALIDATED_AT_FIELD_NUMBER: _ClassVar[int]
    VIEW_REVISION_FIELD_NUMBER: _ClassVar[int]
    scope: AccountScopeRef
    invalidated_at: _timestamp_pb2.Timestamp
    view_revision: int
    def __init__(self, scope: _Optional[_Union[AccountScopeRef, _Mapping]] = ..., invalidated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., view_revision: _Optional[int] = ...) -> None: ...
