"""Withdraw destination encoding (TS destination-encoding parity)."""

from __future__ import annotations

from polyester.errors import PolyesterValidationError


def encode_withdraw_destination(*, address: str, is_case_sensitive: bool) -> bytes:
    """UTF-8 bytes of the normalized address (TS ``encodeWithdrawDestination``).

    For case-insensitive chains the address is lowercased before encoding.
    """
    normalized = address if is_case_sensitive else address.lower()
    if not normalized.strip():
        raise PolyesterValidationError("address must not be empty")
    return normalized.encode("utf-8")


def encode_withdraw_destination_hex(*, address: str, is_case_sensitive: bool) -> str:
    """0x-prefixed hex of UTF-8 destination bytes (TS ``evmUtf8ToHex``)."""
    return (
        "0x"
        + encode_withdraw_destination(
            address=address,
            is_case_sensitive=is_case_sensitive,
        ).hex()
    )
