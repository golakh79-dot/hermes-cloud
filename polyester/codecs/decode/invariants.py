from __future__ import annotations

from typing import Any

from polyester.errors import PolyesterResponseContractError


def ts_ns_from_response(
    value: Any,
    *,
    context: str,
    field_name: str = "ts_ns",
) -> int:
    """Decode an epoch timestamp field as a non-negative integer.

    Does not guess units (ns vs ms); callers treat the value as epoch nanoseconds
    per the API contract, and the backend owns unit correctness.
    """
    try:
        parsed = int(value)
    except (TypeError, ValueError) as exc:
        raise PolyesterResponseContractError(
            context, f"{field_name} must be an unsigned epoch-nanosecond integer"
        ) from exc
    if parsed < 0:
        raise PolyesterResponseContractError(
            context, f"{field_name} must be an unsigned epoch-nanosecond integer"
        )
    return parsed


def ts_ns_string_from_response(
    value: Any,
    *,
    context: str,
    field_name: str = "ts_ns",
    empty_when_zero: bool = False,
) -> str:
    parsed = ts_ns_from_response(value, context=context, field_name=field_name)
    if parsed == 0 and empty_when_zero:
        return ""
    return str(parsed)
