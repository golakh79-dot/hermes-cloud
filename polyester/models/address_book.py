from __future__ import annotations

import msgspec


class AccountScope(msgspec.Struct, kw_only=True, omit_defaults=True):
    scope_type: str = ""
    root_account_id: str = ""
    sub_account_id: str = ""


class AddressBookSummary(msgspec.Struct, kw_only=True, omit_defaults=True):
    scope: AccountScope | None = None
    caller_role: int = 0
    label: str = ""
    owner_username: str = ""
    smart_account_address: str = ""


class ExternalWithdrawAddress(msgspec.Struct, kw_only=True, omit_defaults=True):
    polychain_chain_id: int = 0
    address: str = ""


class InternalTransferAccount(msgspec.Struct, kw_only=True, omit_defaults=True):
    root_account_id: str = ""
    target_account_id: str = ""
    target_scope_type: str = ""
    smart_account_address: str = ""
    root_username: str = ""
    sub_account_label: str = ""


class AddressBookTagInput(msgspec.Struct, kw_only=True, omit_defaults=True):
    name: str
    color: str = ""


class AddressBookTagSummary(msgspec.Struct, kw_only=True, omit_defaults=True):
    tag_id: str = ""
    name: str = ""
    color: str = ""


class AddressBookTag(msgspec.Struct, kw_only=True, omit_defaults=True):
    tag_id: str = ""
    scope: AccountScope | None = None
    name: str = ""
    color: str = ""
    created_at_ms: int = 0
    updated_at_ms: int = 0


class AddressBookEntry(msgspec.Struct, kw_only=True, omit_defaults=True):
    address_book_entry_id: str = ""
    scope: AccountScope | None = None
    kind: str = ""
    label: str = ""
    note: str = ""
    created_at_ms: int = 0
    updated_at_ms: int = 0
    external: ExternalWithdrawAddress | None = None
    internal: InternalTransferAccount | None = None
    tags: list[AddressBookTag] | None = None
    revision: int = 0


class AddressBookEntriesList(msgspec.Struct, kw_only=True, omit_defaults=True):
    entries: list[AddressBookEntry]
    next_page_token: str = ""


class AddressBooksList(msgspec.Struct, kw_only=True, omit_defaults=True):
    books: list[AddressBookSummary]


class TransferCounterparty(msgspec.Struct, kw_only=True, omit_defaults=True):
    counterparty_id: str = ""
    scope: AccountScope | None = None
    direction: str = ""
    kind: str = ""
    saved: bool = False
    address_book_entry_id: str = ""
    use_count: int = 0
    first_seen_at_ms: int = 0
    last_seen_at_ms: int = 0
    external: ExternalWithdrawAddress | None = None
    internal: InternalTransferAccount | None = None


class TransferCounterpartiesList(msgspec.Struct, kw_only=True, omit_defaults=True):
    counterparties: list[TransferCounterparty]
    truncated: bool = False


class AddressBookTransferDestination(msgspec.Struct, kw_only=True, omit_defaults=True):
    scope: AccountScope | None = None
    kind: str = ""
    saved: bool = False
    whitelisted: bool = False
    whitelist_status: str = ""
    address_book_entry: AddressBookEntry | None = None
    external: ExternalWithdrawAddress | None = None
    internal: InternalTransferAccount | None = None
    whitelist_updated_at_ms: int = 0


class AddressBookTransferDestinationsList(msgspec.Struct, kw_only=True, omit_defaults=True):
    destinations: list[AddressBookTransferDestination]
    next_page_token: str = ""


class InternalTransferWhitelistEntry(msgspec.Struct, kw_only=True, omit_defaults=True):
    entry_id: str = ""
    scope: AccountScope | None = None
    root_account_id: str = ""
    target_account_id: str = ""
    target_scope_type: str = ""
    smart_account_address: str = ""
    root_username: str = ""
    sub_account_label: str = ""
    created_at_ms: int = 0
    updated_at_ms: int = 0
    resolution_status: str = ""


class InternalTransferWhitelistEntriesList(msgspec.Struct, kw_only=True, omit_defaults=True):
    entries: list[InternalTransferWhitelistEntry]
    next_page_token: str = ""


class MirroredWithdrawWhitelistEntry(msgspec.Struct, kw_only=True, omit_defaults=True):
    canonical_address: str = ""
    raw_address_hex: str = ""
    updated_at_ms: int = 0
    polychain_chain_id: int = 0


class WithdrawWhitelistView(msgspec.Struct, kw_only=True, omit_defaults=True):
    scope: AccountScope | None = None
    external_whitelist_required: bool = False
    internal_whitelist_required: bool = False
    active_entries: list[MirroredWithdrawWhitelistEntry] | None = None


class ExternalAddressBookEntryView(msgspec.Struct, kw_only=True, omit_defaults=True):
    address_book_entry_id: str = ""
    scope: AccountScope | None = None
    label: str = ""
    note: str = ""
    tag_ids: list[str] | None = None
    whitelist_status: str = ""
    polychain_chain_id: int = 0
    address: str = ""
    created_at_ms: int = 0
    updated_at_ms: int = 0


class InternalAddressBookEntryView(msgspec.Struct, kw_only=True, omit_defaults=True):
    address_book_entry_id: str = ""
    scope: AccountScope | None = None
    label: str = ""
    note: str = ""
    tag_ids: list[str] | None = None
    whitelist_status: str = ""
    root_account_id: str = ""
    target_account_id: str = ""
    target_scope_type: str = ""
    smart_account_address: str = ""
    root_username: str = ""
    sub_account_label: str = ""
    created_at_ms: int = 0
    updated_at_ms: int = 0


class AddressBookEntriesView(msgspec.Struct, kw_only=True, omit_defaults=True):
    external: list[ExternalAddressBookEntryView] | None = None
    internal: list[InternalAddressBookEntryView] | None = None


class ExternalRecentDestination(msgspec.Struct, kw_only=True, omit_defaults=True):
    scope: AccountScope | None = None
    last_direction: str = ""
    saved: bool = False
    address_book_entry_id: str = ""
    use_count: int = 0
    last_seen_at_ms: int = 0
    polychain_chain_id: int = 0
    address: str = ""


class InternalRecentDestination(msgspec.Struct, kw_only=True, omit_defaults=True):
    scope: AccountScope | None = None
    last_direction: str = ""
    saved: bool = False
    address_book_entry_id: str = ""
    use_count: int = 0
    last_seen_at_ms: int = 0
    root_account_id: str = ""
    target_account_id: str = ""
    target_scope_type: str = ""
    smart_account_address: str = ""
    root_username: str = ""
    sub_account_label: str = ""


class AddressBookRecentDestinationsView(msgspec.Struct, kw_only=True, omit_defaults=True):
    external: list[ExternalRecentDestination] | None = None
    internal: list[InternalRecentDestination] | None = None


class AddressBookView(msgspec.Struct, kw_only=True, omit_defaults=True):
    books: list[AddressBookSummary] | None = None
    entries: AddressBookEntriesView | None = None
    recent_destinations: AddressBookRecentDestinationsView | None = None
    tags: list[AddressBookTagSummary] | None = None
    withdraw_whitelist: WithdrawWhitelistView | None = None
    recent_destinations_truncated: bool = False
    view_revision: int = 0
