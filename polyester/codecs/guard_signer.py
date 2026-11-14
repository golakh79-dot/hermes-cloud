from __future__ import annotations

from typing import Any

from polyester.errors import PolyesterValidationError
from polyester.gen.chain.guard.v1 import guard_signer_pb2


def protected_action_from_label(action: str) -> Any:
    aliases = {
        "funding_set_external_whitelist_required": (
            guard_signer_pb2.PROTECTED_ACTION_FUNDING_SET_EXTERNAL_WHITELIST_REQUIRED
        ),
        "funding_add_external_whitelist": (
            guard_signer_pb2.PROTECTED_ACTION_FUNDING_ADD_EXTERNAL_WHITELIST
        ),
        "funding_remove_external_whitelist": (
            guard_signer_pb2.PROTECTED_ACTION_FUNDING_REMOVE_EXTERNAL_WHITELIST
        ),
        "funding_add_internal_whitelist": (
            guard_signer_pb2.PROTECTED_ACTION_FUNDING_ADD_INTERNAL_WHITELIST
        ),
        "funding_remove_internal_whitelist": (
            guard_signer_pb2.PROTECTED_ACTION_FUNDING_REMOVE_INTERNAL_WHITELIST
        ),
        "funding_set_internal_whitelist_required": (
            guard_signer_pb2.PROTECTED_ACTION_FUNDING_SET_INTERNAL_WHITELIST_REQUIRED
        ),
    }
    key = action.lower().replace("-", "_")
    if key in aliases:
        return aliases[key]
    enum_name = key.upper()
    if not enum_name.startswith("PROTECTED_ACTION_"):
        enum_name = f"PROTECTED_ACTION_{enum_name}"
    value = getattr(guard_signer_pb2, enum_name, None)
    if value is None:
        raise PolyesterValidationError(f"Unknown protected action: {action}")
    return value


def protected_action_args_to_proto(
    *,
    external_polychain_chain_id: int | None = None,
    external_addresses: list[str] | None = None,
    internal_addresses: list[str] | None = None,
    whitelist_required: bool | None = None,
) -> guard_signer_pb2.ProtectedActionArgs:
    args = guard_signer_pb2.ProtectedActionArgs()
    if external_polychain_chain_id is not None and external_addresses:
        args.external_whitelist.polychain_chain_id = external_polychain_chain_id
        args.external_whitelist.addresses.extend(external_addresses)
    elif internal_addresses:
        args.internal_whitelist.addresses.extend(internal_addresses)
    elif whitelist_required is not None:
        args.whitelist_requirement.required = whitelist_required
    return args
