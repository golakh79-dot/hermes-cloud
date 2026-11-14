from __future__ import annotations

from polyester.codecs.proto_helpers import format_uint64_id, proto_enum_name, timestamp_to_ms
from polyester.errors import PolyesterResponseContractError
from polyester.gen.auth.v1 import address_book_pb2
from polyester.models.address_book import (
    AccountScope,
    AddressBookEntriesList,
    AddressBookEntriesView,
    AddressBookEntry,
    AddressBookRecentDestinationsView,
    AddressBooksList,
    AddressBookSummary,
    AddressBookTag,
    AddressBookTagSummary,
    AddressBookTransferDestination,
    AddressBookTransferDestinationsList,
    AddressBookView,
    ExternalAddressBookEntryView,
    ExternalRecentDestination,
    ExternalWithdrawAddress,
    InternalAddressBookEntryView,
    InternalRecentDestination,
    InternalTransferAccount,
    InternalTransferWhitelistEntriesList,
    InternalTransferWhitelistEntry,
    MirroredWithdrawWhitelistEntry,
    TransferCounterpartiesList,
    TransferCounterparty,
    WithdrawWhitelistView,
)


def account_scope_from_proto(msg: address_book_pb2.AccountScopeRef) -> AccountScope:
    return AccountScope(
        scope_type=proto_enum_name(address_book_pb2.AccountScopeType, msg.scope_type),
        root_account_id=format_uint64_id(msg.root_account_id),
        sub_account_id=format_uint64_id(msg.subaccount_id),
    )


def external_withdraw_address_from_proto(
    msg: address_book_pb2.ExternalWithdrawAddress,
) -> ExternalWithdrawAddress:
    return ExternalWithdrawAddress(
        polychain_chain_id=int(msg.polychain_chain_id),
        address=msg.address,
    )


def internal_transfer_account_from_proto(
    msg: address_book_pb2.InternalTransferAccount,
) -> InternalTransferAccount:
    return InternalTransferAccount(
        root_account_id=format_uint64_id(msg.root_account_id),
        target_account_id=format_uint64_id(msg.target_account_id),
        target_scope_type=proto_enum_name(address_book_pb2.AccountScopeType, msg.target_scope_type),
        smart_account_address=msg.smart_account_address,
        root_username=msg.root_username,
        sub_account_label=msg.subaccount_label,
    )


def address_book_tag_from_proto(msg: address_book_pb2.AddressBookTag) -> AddressBookTag:
    scope = None
    if msg.HasField("scope"):
        scope = account_scope_from_proto(msg.scope)
    return AddressBookTag(
        tag_id=format_uint64_id(msg.tag_id),
        scope=scope,
        name=msg.name,
        color=msg.color,
        created_at_ms=timestamp_to_ms(msg.created_at),
        updated_at_ms=timestamp_to_ms(msg.updated_at),
    )


def address_book_tag_summary_from_proto(
    msg: address_book_pb2.AddressBookTagSummary,
) -> AddressBookTagSummary:
    return AddressBookTagSummary(
        tag_id=format_uint64_id(msg.tag_id),
        name=msg.name,
        color=msg.color,
    )


def address_book_entry_from_proto(msg: address_book_pb2.AddressBookEntry) -> AddressBookEntry:
    scope = None
    if msg.HasField("scope"):
        scope = account_scope_from_proto(msg.scope)
    external = None
    internal = None
    if msg.HasField("external"):
        external = external_withdraw_address_from_proto(msg.external)
    if msg.HasField("internal"):
        internal = internal_transfer_account_from_proto(msg.internal)
    return AddressBookEntry(
        address_book_entry_id=format_uint64_id(msg.address_book_entry_id),
        scope=scope,
        kind=proto_enum_name(address_book_pb2.AddressBookEntryKind, msg.kind),
        label=msg.label,
        note=msg.note,
        created_at_ms=timestamp_to_ms(msg.created_at),
        updated_at_ms=timestamp_to_ms(msg.updated_at),
        external=external,
        internal=internal,
        tags=[address_book_tag_from_proto(item) for item in msg.tags],
        revision=int(msg.revision),
    )


def address_book_summary_from_proto(msg: address_book_pb2.AddressBook) -> AddressBookSummary:
    scope = None
    if msg.HasField("scope"):
        scope = account_scope_from_proto(msg.scope)
    return AddressBookSummary(
        scope=scope,
        caller_role=int(msg.caller_role),
        label=msg.label,
        owner_username=msg.owner_username,
        smart_account_address=msg.smart_account_address,
    )


def list_books_from_proto(msg: address_book_pb2.ListAddressBooksResponse) -> AddressBooksList:
    return AddressBooksList(books=[address_book_summary_from_proto(item) for item in msg.books])


def list_entries_from_proto(
    msg: address_book_pb2.ListAddressBookEntriesResponse,
) -> AddressBookEntriesList:
    return AddressBookEntriesList(
        entries=[address_book_entry_from_proto(item) for item in msg.entries],
        next_page_token=msg.next_page_token,
    )


def transfer_counterparty_from_proto(
    msg: address_book_pb2.TransferCounterparty,
) -> TransferCounterparty:
    scope = None
    if msg.HasField("scope"):
        scope = account_scope_from_proto(msg.scope)
    external = None
    internal = None
    if msg.HasField("external"):
        external = external_withdraw_address_from_proto(msg.external)
    if msg.HasField("internal"):
        internal = internal_transfer_account_from_proto(msg.internal)
    return TransferCounterparty(
        counterparty_id=format_uint64_id(msg.counterparty_id),
        scope=scope,
        direction=proto_enum_name(
            address_book_pb2.TransferCounterpartyDirection,
            msg.direction,
        ),
        kind=proto_enum_name(address_book_pb2.AddressBookEntryKind, msg.kind),
        saved=bool(msg.saved),
        address_book_entry_id=format_uint64_id(msg.address_book_entry_id),
        use_count=int(msg.use_count),
        first_seen_at_ms=timestamp_to_ms(msg.first_seen_at),
        last_seen_at_ms=timestamp_to_ms(msg.last_seen_at),
        external=external,
        internal=internal,
    )


def list_counterparties_from_proto(
    msg: address_book_pb2.ListTransferCounterpartiesResponse,
) -> TransferCounterpartiesList:
    return TransferCounterpartiesList(
        counterparties=[transfer_counterparty_from_proto(item) for item in msg.counterparties],
        truncated=bool(msg.truncated),
    )


def transfer_destination_from_proto(
    msg: address_book_pb2.TransferDestination,
) -> AddressBookTransferDestination:
    scope = None
    if msg.HasField("scope"):
        scope = account_scope_from_proto(msg.scope)
    entry = None
    external = None
    internal = None
    if msg.HasField("address_book_entry"):
        entry = address_book_entry_from_proto(msg.address_book_entry)
    if msg.HasField("external"):
        external = external_withdraw_address_from_proto(msg.external)
    if msg.HasField("internal"):
        internal = internal_transfer_account_from_proto(msg.internal)
    return AddressBookTransferDestination(
        scope=scope,
        kind=proto_enum_name(address_book_pb2.AddressBookEntryKind, msg.kind),
        saved=bool(msg.saved),
        whitelisted=bool(msg.whitelisted),
        whitelist_status=proto_enum_name(
            address_book_pb2.DestinationWhitelistStatus,
            msg.whitelist_status,
        ),
        address_book_entry=entry,
        external=external,
        internal=internal,
        whitelist_updated_at_ms=timestamp_to_ms(msg.whitelist_updated_at),
    )


def list_destinations_from_proto(
    msg: address_book_pb2.ListTransferDestinationsResponse,
) -> AddressBookTransferDestinationsList:
    return AddressBookTransferDestinationsList(
        destinations=[transfer_destination_from_proto(item) for item in msg.destinations],
        next_page_token=msg.next_page_token,
    )


def internal_whitelist_entry_from_proto(
    msg: address_book_pb2.InternalTransferWhitelistEntry,
) -> InternalTransferWhitelistEntry:
    scope = None
    if msg.HasField("scope"):
        scope = account_scope_from_proto(msg.scope)
    return InternalTransferWhitelistEntry(
        entry_id=format_uint64_id(msg.entry_id),
        scope=scope,
        root_account_id=format_uint64_id(msg.root_account_id),
        target_account_id=format_uint64_id(msg.target_account_id),
        target_scope_type=proto_enum_name(
            address_book_pb2.AccountScopeType,
            msg.target_scope_type,
        ),
        smart_account_address=msg.smart_account_address,
        root_username=msg.root_username,
        sub_account_label=msg.subaccount_label,
        created_at_ms=timestamp_to_ms(msg.created_at),
        updated_at_ms=timestamp_to_ms(msg.updated_at),
        resolution_status=proto_enum_name(
            address_book_pb2.InternalWhitelistResolutionStatus,
            msg.resolution_status,
        ),
    )


def list_internal_whitelist_from_proto(
    msg: address_book_pb2.ListInternalTransferWhitelistEntriesResponse,
) -> InternalTransferWhitelistEntriesList:
    return InternalTransferWhitelistEntriesList(
        entries=[internal_whitelist_entry_from_proto(item) for item in msg.entries],
        next_page_token=msg.next_page_token,
    )


def mirrored_whitelist_entry_from_proto(
    msg: address_book_pb2.MirroredWithdrawWhitelistEntry,
) -> MirroredWithdrawWhitelistEntry:
    return MirroredWithdrawWhitelistEntry(
        canonical_address=msg.canonical_address,
        raw_address_hex=msg.raw_address_hex,
        updated_at_ms=timestamp_to_ms(msg.updated_at),
        polychain_chain_id=int(msg.polychain_chain_id),
    )


def withdraw_whitelist_view_from_proto(
    msg: address_book_pb2.WithdrawWhitelistView,
) -> WithdrawWhitelistView:
    scope = None
    if msg.HasField("scope"):
        scope = account_scope_from_proto(msg.scope)
    return WithdrawWhitelistView(
        scope=scope,
        external_whitelist_required=bool(msg.external_whitelist_required),
        internal_whitelist_required=bool(msg.internal_whitelist_required),
        active_entries=[mirrored_whitelist_entry_from_proto(item) for item in msg.active_entries],
    )


def withdraw_whitelist_view_from_get_proto(
    msg: address_book_pb2.GetWithdrawWhitelistViewResponse,
) -> WithdrawWhitelistView | None:
    if msg.HasField("view"):
        return withdraw_whitelist_view_from_proto(msg.view)
    return None


def external_entry_view_from_proto(
    msg: address_book_pb2.ExternalAddressBookEntry,
) -> ExternalAddressBookEntryView:
    scope = None
    if msg.HasField("scope"):
        scope = account_scope_from_proto(msg.scope)
    return ExternalAddressBookEntryView(
        address_book_entry_id=format_uint64_id(msg.address_book_entry_id),
        scope=scope,
        label=msg.label,
        note=msg.note,
        tag_ids=[format_uint64_id(item) for item in msg.tag_ids],
        whitelist_status=proto_enum_name(
            address_book_pb2.DestinationWhitelistStatus,
            msg.whitelist_status,
        ),
        polychain_chain_id=int(msg.polychain_chain_id),
        address=msg.address,
        created_at_ms=timestamp_to_ms(msg.created_at),
        updated_at_ms=timestamp_to_ms(msg.updated_at),
    )


def internal_entry_view_from_proto(
    msg: address_book_pb2.InternalAddressBookEntry,
) -> InternalAddressBookEntryView:
    scope = None
    if msg.HasField("scope"):
        scope = account_scope_from_proto(msg.scope)
    return InternalAddressBookEntryView(
        address_book_entry_id=format_uint64_id(msg.address_book_entry_id),
        scope=scope,
        label=msg.label,
        note=msg.note,
        tag_ids=[format_uint64_id(item) for item in msg.tag_ids],
        whitelist_status=proto_enum_name(
            address_book_pb2.DestinationWhitelistStatus,
            msg.whitelist_status,
        ),
        root_account_id=format_uint64_id(msg.root_account_id),
        target_account_id=format_uint64_id(msg.target_account_id),
        target_scope_type=proto_enum_name(
            address_book_pb2.AccountScopeType,
            msg.target_scope_type,
        ),
        smart_account_address=msg.smart_account_address,
        root_username=msg.root_username,
        sub_account_label=msg.subaccount_label,
        created_at_ms=timestamp_to_ms(msg.created_at),
        updated_at_ms=timestamp_to_ms(msg.updated_at),
    )


def entries_view_from_proto(msg: address_book_pb2.AddressBookEntriesView) -> AddressBookEntriesView:
    return AddressBookEntriesView(
        external=[external_entry_view_from_proto(item) for item in msg.external],
        internal=[internal_entry_view_from_proto(item) for item in msg.internal],
    )


def external_recent_from_proto(
    msg: address_book_pb2.ExternalRecentDestination,
) -> ExternalRecentDestination:
    scope = None
    if msg.HasField("scope"):
        scope = account_scope_from_proto(msg.scope)
    return ExternalRecentDestination(
        scope=scope,
        last_direction=proto_enum_name(
            address_book_pb2.TransferCounterpartyDirection,
            msg.last_direction,
        ),
        saved=bool(msg.saved),
        address_book_entry_id=format_uint64_id(msg.address_book_entry_id),
        use_count=int(msg.use_count),
        last_seen_at_ms=timestamp_to_ms(msg.last_seen_at),
        polychain_chain_id=int(msg.polychain_chain_id),
        address=msg.address,
    )


def internal_recent_from_proto(
    msg: address_book_pb2.InternalRecentDestination,
) -> InternalRecentDestination:
    scope = None
    if msg.HasField("scope"):
        scope = account_scope_from_proto(msg.scope)
    return InternalRecentDestination(
        scope=scope,
        last_direction=proto_enum_name(
            address_book_pb2.TransferCounterpartyDirection,
            msg.last_direction,
        ),
        saved=bool(msg.saved),
        address_book_entry_id=format_uint64_id(msg.address_book_entry_id),
        use_count=int(msg.use_count),
        last_seen_at_ms=timestamp_to_ms(msg.last_seen_at),
        root_account_id=format_uint64_id(msg.root_account_id),
        target_account_id=format_uint64_id(msg.target_account_id),
        target_scope_type=proto_enum_name(
            address_book_pb2.AccountScopeType,
            msg.target_scope_type,
        ),
        smart_account_address=msg.smart_account_address,
        root_username=msg.root_username,
        sub_account_label=msg.subaccount_label,
    )


def recent_destinations_view_from_proto(
    msg: address_book_pb2.AddressBookRecentDestinationsView,
) -> AddressBookRecentDestinationsView:
    return AddressBookRecentDestinationsView(
        external=[external_recent_from_proto(item) for item in msg.external],
        internal=[internal_recent_from_proto(item) for item in msg.internal],
    )


def address_book_view_from_proto(
    msg: address_book_pb2.GetAddressBookViewResponse,
) -> AddressBookView:
    entries = None
    recent = None
    withdraw = None
    if msg.HasField("entries"):
        entries = entries_view_from_proto(msg.entries)
    if msg.HasField("recent_destinations"):
        recent = recent_destinations_view_from_proto(msg.recent_destinations)
    if msg.HasField("withdraw_whitelist"):
        withdraw = withdraw_whitelist_view_from_proto(msg.withdraw_whitelist)
    return AddressBookView(
        books=[address_book_summary_from_proto(item) for item in msg.books],
        entries=entries,
        recent_destinations=recent,
        tags=[address_book_tag_summary_from_proto(item) for item in msg.tags],
        withdraw_whitelist=withdraw,
        recent_destinations_truncated=bool(msg.recent_destinations_truncated),
        view_revision=int(msg.view_revision),
    )


def entry_from_create_proto(
    msg: address_book_pb2.CreateAddressBookEntryResponse,
) -> AddressBookEntry:
    if not msg.HasField("entry"):
        raise PolyesterResponseContractError("CreateAddressBookEntry", "missing entry")
    return address_book_entry_from_proto(msg.entry)


def entry_from_update_proto(
    msg: address_book_pb2.UpdateAddressBookEntryResponse,
) -> AddressBookEntry:
    if not msg.HasField("entry"):
        raise PolyesterResponseContractError("UpdateAddressBookEntry", "missing entry")
    return address_book_entry_from_proto(msg.entry)


def tag_from_create_proto(msg: address_book_pb2.CreateAddressBookTagResponse) -> AddressBookTag:
    if not msg.HasField("tag"):
        raise PolyesterResponseContractError("CreateAddressBookTag", "missing tag")
    return address_book_tag_from_proto(msg.tag)


def tag_from_update_proto(msg: address_book_pb2.UpdateAddressBookTagResponse) -> AddressBookTag:
    if not msg.HasField("tag"):
        raise PolyesterResponseContractError("UpdateAddressBookTag", "missing tag")
    return address_book_tag_from_proto(msg.tag)
