from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from polyester.codecs.scalars import id_to_int
from polyester.errors import PolyesterValidationError
from polyester.gen.auth.v1 import address_book_pb2
from polyester.models.address_book import AddressBookTagInput
from polyester.patch import UNSET, field_mask, is_set, require_positive_revision


def address_book_entry_kind_from_label(kind: str) -> Any:
    aliases = {
        "external": address_book_pb2.EXTERNAL_CHAIN,
        "external_chain": address_book_pb2.EXTERNAL_CHAIN,
        "internal": address_book_pb2.INTERNAL_ACCOUNT,
        "internal_account": address_book_pb2.INTERNAL_ACCOUNT,
    }
    key = kind.lower().replace("-", "_")
    if key in aliases:
        return aliases[key]
    enum_name = key.upper()
    if not enum_name.startswith("ENTRY_KIND_") and enum_name not in (
        "EXTERNAL_CHAIN",
        "INTERNAL_ACCOUNT",
    ):
        enum_name = f"ENTRY_KIND_{enum_name}" if enum_name != "EXTERNAL_CHAIN" else enum_name
    value = getattr(address_book_pb2, enum_name, None)
    if value is None and not enum_name.startswith("ENTRY_KIND_"):
        value = getattr(address_book_pb2, f"ENTRY_KIND_{enum_name}", None)
    if value is None:
        raise PolyesterValidationError("kind must be 'external' or 'internal'")
    return value


def transfer_counterparty_direction_from_label(direction: str) -> Any:
    aliases = {
        "deposit_from": address_book_pb2.DEPOSIT_FROM,
        "withdraw_to": address_book_pb2.WITHDRAW_TO,
        "internal_transfer_from": address_book_pb2.INTERNAL_TRANSFER_FROM,
        "internal_transfer_to": address_book_pb2.INTERNAL_TRANSFER_TO,
    }
    key = direction.lower().replace("-", "_")
    if key in aliases:
        return aliases[key]
    enum_name = key.upper()
    value = getattr(address_book_pb2, enum_name, None)
    if value is None:
        raise PolyesterValidationError(f"Unknown transfer counterparty direction: {direction}")
    return value


def tag_ids_from_public(values: list[str | int] | None) -> list[int]:
    if values is None:
        return []
    return [id_to_int(item, "tag_id") for item in values]


def tag_input_from_public(
    value: AddressBookTagInput | Mapping[str, Any],
) -> address_book_pb2.AddressBookTagInput:
    if isinstance(value, AddressBookTagInput):
        raw_name: object = value.name
        raw_color: object = value.color
    elif isinstance(value, Mapping):
        raw_name = value.get("name")
        raw_color = value.get("color", "")
    else:
        raise PolyesterValidationError("new_tags items must be AddressBookTagInput or objects")
    if not isinstance(raw_name, str) or not raw_name:
        raise PolyesterValidationError("tag name is required")
    if raw_color is None:
        raw_color = ""
    if not isinstance(raw_color, str):
        raise PolyesterValidationError("tag color must be a string")
    return address_book_pb2.AddressBookTagInput(name=raw_name, color=raw_color)


def tag_inputs_from_public(
    values: list[AddressBookTagInput | Mapping[str, Any]] | None,
) -> list[address_book_pb2.AddressBookTagInput]:
    if values is None:
        return []
    return [tag_input_from_public(item) for item in values]


def create_entry_to_proto(
    *,
    subaccount_id: int | None,
    label: str,
    note: str,
    address: str | None,
    polychain_chain_id: int | None,
    smart_account_address: str | None,
    tag_ids: list[str | int] | None,
    new_tags: list[AddressBookTagInput | Mapping[str, Any]] | None,
) -> address_book_pb2.CreateAddressBookEntryRequest:
    has_external = address is not None
    has_internal = smart_account_address is not None
    if has_external == has_internal:
        raise PolyesterValidationError(
            "create_entry requires exactly one of address or smart_account_address"
        )
    request = address_book_pb2.CreateAddressBookEntryRequest(
        label=label,
        note=note,
        tag_ids=tag_ids_from_public(tag_ids),
        new_tags=tag_inputs_from_public(new_tags),
    )
    if subaccount_id is not None:
        request.subaccount_id = subaccount_id
    if has_external:
        if not isinstance(address, str) or not address:
            raise PolyesterValidationError("address is required for an external entry")
        external = address_book_pb2.ExternalWithdrawAddress(address=address)
        if polychain_chain_id is not None:
            if int(polychain_chain_id) <= 0:
                raise PolyesterValidationError("polychain_chain_id must be positive")
            external.polychain_chain_id = int(polychain_chain_id)
        request.external.CopyFrom(external)
    else:
        if not isinstance(smart_account_address, str) or not smart_account_address:
            raise PolyesterValidationError(
                "smart_account_address is required for an internal entry"
            )
        request.internal.CopyFrom(
            address_book_pb2.RequestedInternalTransferAccount(
                smart_account_address=smart_account_address
            )
        )
    return request


def update_entry_to_proto(
    *,
    address_book_entry_id: str | int,
    expected_revision: int,
    label: object = UNSET,
    note: object = UNSET,
    tag_ids: object = UNSET,
    new_tags: object = UNSET,
) -> address_book_pb2.UpdateAddressBookEntryRequest:
    require_positive_revision(expected_revision)
    spec = address_book_pb2.AddressBookEntryUpdateSpec()
    paths: list[str] = []
    if is_set(label):
        if not isinstance(label, str):
            raise PolyesterValidationError("label must be a string")
        spec.label = label
        paths.append("label")
    if is_set(note):
        if not isinstance(note, str):
            raise PolyesterValidationError("note must be a string")
        spec.note = note
        paths.append("note")
    if is_set(tag_ids):
        if tag_ids is None:
            raise PolyesterValidationError("tag_ids must be a list when selected")
        if not isinstance(tag_ids, list):
            raise PolyesterValidationError("tag_ids must be a list")
        spec.tag_ids.extend(tag_ids_from_public(tag_ids))
        paths.append("tag_ids")
    if is_set(new_tags):
        if new_tags is None:
            raise PolyesterValidationError("new_tags must be a list when selected")
        if not isinstance(new_tags, list):
            raise PolyesterValidationError("new_tags must be a list")
        spec.new_tags.extend(tag_inputs_from_public(new_tags))
        paths.append("new_tags")
    return address_book_pb2.UpdateAddressBookEntryRequest(
        address_book_entry_id=id_to_int(address_book_entry_id, "address_book_entry_id"),
        entry=spec,
        update_mask=field_mask(paths),
        expected_revision=expected_revision,
    )
