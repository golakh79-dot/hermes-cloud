from __future__ import annotations

from polyester.errors import PolyesterValidationError

CLIENT_ID_MAX_LEN = 36
REQUEST_ID_MAX_LEN = 64
_ALLOWED_PUNCTUATION = "._:/-"


def validate_correlation_id(value: str, field: str, max_len: int) -> str:
    trimmed = value.strip()
    if not trimmed or len(trimmed) > max_len:
        raise PolyesterValidationError(f"{field} must be 1 to {max_len} characters")
    valid_chars = (
        char.isascii() and (char.isalnum() or char in _ALLOWED_PUNCTUATION)
        for char in trimmed
    )
    if not all(valid_chars):
        raise PolyesterValidationError(
            f"{field} contains invalid characters; allowed: A-Z a-z 0-9 . _ : / -"
        )
    return trimmed


def optional_client_id(value: str | None, field: str = "client_order_id") -> str | None:
    if value is None or not value.strip():
        return None
    return validate_correlation_id(value, field, CLIENT_ID_MAX_LEN)


def required_client_id(value: str, field: str) -> str:
    return validate_correlation_id(value, field, CLIENT_ID_MAX_LEN)


def optional_request_id(value: str | None) -> str | None:
    if value is None or not value.strip():
        return None
    return validate_correlation_id(value, "request_id", REQUEST_ID_MAX_LEN)
