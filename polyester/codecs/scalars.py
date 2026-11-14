from __future__ import annotations

import re
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

import base58

from polyester.errors import PolyesterValidationError

UINT64_MAX = 2**64 - 1
UINT32_MAX = 2**32 - 1
INT64_MAX = 2**63 - 1
INT64_MIN = -(2**63)
PRICE_TICK_SCALE = 9
# Maximum accepted quantity/ledger scale for public formatters and catalog hydration.
# Values above this are rejected instead of allocating pathological padding (scale ≥ 65535).
MAX_PROTOCOL_SCALE = 36

# Strict non-negative decimal: digits with optional fractional part (TS-aligned).
_STRICT_DECIMAL = re.compile(r"^\d+(?:\.\d+)?$")


def validate_protocol_scale(scale: int, *, field_name: str = "scale") -> int:
    """Reject scales that would panic or allocate pathological padding."""
    if isinstance(scale, bool) or not isinstance(scale, int):
        raise PolyesterValidationError(f"{field_name} must be an int")
    if scale < 0:
        raise PolyesterValidationError(f"{field_name} must be non-negative")
    if scale > MAX_PROTOCOL_SCALE:
        raise PolyesterValidationError(
            f"{field_name} {scale} exceeds maximum protocol scale {MAX_PROTOCOL_SCALE}"
        )
    return scale


def _decimal_string_from_input(raw: str | Decimal, field_name: str) -> str:
    if isinstance(raw, (bool, float)):
        raise PolyesterValidationError(f"{field_name} must be a decimal string or Decimal")
    if isinstance(raw, Decimal):
        if not raw.is_finite():
            raise PolyesterValidationError(f"{field_name} must be a finite decimal")
        if raw < 0:
            raise PolyesterValidationError(f"{field_name} must be non-negative")
        text = format(raw, "f")
        if "." in text:
            text = text.rstrip("0").rstrip(".")
        return text or "0"
    if not isinstance(raw, str):
        raise PolyesterValidationError(f"{field_name} must be a decimal string or Decimal")
    text = raw.strip()
    if not text or not _STRICT_DECIMAL.match(text):
        raise PolyesterValidationError(f"{field_name} must be a valid decimal string")
    return text


def _trim_trailing_frac_zeros(raw: str) -> str:
    """Drop insignificant trailing zeros so formatters like toFixed() survive scale checks."""
    if "." not in raw:
        return raw
    int_part, frac_part = raw.split(".", 1)
    frac_part = frac_part.rstrip("0")
    if not frac_part:
        return int_part or "0"
    return f"{int_part}.{frac_part}"


def try_decimal_to_scaled(decimal: str, scale: int) -> tuple[bool, int | None, str | None]:
    """Strict decimal→scaled. Returns (ok, scaled, failure_reason). Never rounds."""
    if scale < 0 or scale > MAX_PROTOCOL_SCALE:
        return False, None, "scale"
    raw = decimal.strip()
    if not _STRICT_DECIMAL.match(raw):
        return False, None, "invalid"
    raw = _trim_trailing_frac_zeros(raw)
    int_part, _, frac_part = raw.partition(".")
    if len(frac_part) > scale:
        return False, None, "precision"
    digits = int_part + frac_part + ("0" * (scale - len(frac_part)))
    if not digits:
        digits = "0"
    try:
        scaled = int(digits)
    except ValueError:
        return False, None, "invalid"
    return True, scaled, None


def decimal_to_scaled(raw: str | Decimal, scale: int, field_name: str) -> int:
    validate_protocol_scale(scale, field_name=f"{field_name} scale")
    text = _decimal_string_from_input(raw, field_name)
    ok, scaled, reason = try_decimal_to_scaled(text, scale)
    if not ok or scaled is None:
        if reason == "precision":
            raise PolyesterValidationError(
                f"{field_name} supports at most {scale} decimal places: {text}"
            )
        if reason == "scale":
            raise PolyesterValidationError(
                f"{field_name} scale {scale} exceeds maximum protocol scale {MAX_PROTOCOL_SCALE}"
            )
        raise PolyesterValidationError(f"{field_name} must be a valid decimal string")
    return scaled


def tick_count(value: object, field_name: str, *, allow_zero: bool = False) -> int:
    """Validate a caller-supplied integer tick count for an int64 wire field.

    Accepts an ``int`` or a base-10 integer string; rejects booleans, values
    below 1 (below 0 with ``allow_zero``, where zero clears a cap) and values
    above ``INT64_MAX``.
    """
    if isinstance(value, bool) or not isinstance(value, (int, str)):
        raise PolyesterValidationError(f"{field_name} must be an integer")
    try:
        parsed = int(value)
    except ValueError as exc:
        raise PolyesterValidationError(f"{field_name} must be an integer") from exc
    if parsed < 0 or (parsed == 0 and not allow_zero):
        qualifier = "non-negative" if allow_zero else "positive"
        raise PolyesterValidationError(f"{field_name} must be {qualifier}")
    if parsed > INT64_MAX:
        raise PolyesterValidationError(f"{field_name} exceeds int64 range")
    return parsed


def parse_price_ticks(raw: str | Decimal, field_name: str = "price") -> int:
    scaled = decimal_to_scaled(raw, PRICE_TICK_SCALE, field_name)
    if scaled < 0:
        raise PolyesterValidationError(f"{field_name} must be non-negative")
    if scaled > INT64_MAX:
        raise PolyesterValidationError(f"{field_name} exceeds int64 range")
    return scaled


def format_price_ticks(ticks: int) -> str:
    """Convert Q9 price ticks to a decimal string (inverse of parse_price_ticks)."""
    neg = ticks < 0
    digits = str(abs(int(ticks)))
    padded = digits.zfill(PRICE_TICK_SCALE + 1)
    head = padded[:-PRICE_TICK_SCALE]
    tail = padded[-PRICE_TICK_SCALE:]
    raw = f"{head}.{tail}"
    trimmed = raw.rstrip("0").rstrip(".") or "0"
    return f"-{trimmed}" if neg else trimmed


def format_qty_scaled(qty_scaled: int, scale: int) -> str:
    """Convert scaled integer quantity to a decimal string.

    Raises PolyesterValidationError when ``scale`` exceeds ``MAX_PROTOCOL_SCALE``.
    """
    validate_protocol_scale(scale)
    if scale <= 0:
        return str(int(qty_scaled))
    neg = qty_scaled < 0
    digits = str(abs(int(qty_scaled)))
    padded = digits.zfill(scale + 1)
    head = padded[:-scale]
    tail = padded[-scale:]
    raw = f"{head}.{tail}"
    trimmed = raw.rstrip("0").rstrip(".") or "0"
    return f"-{trimmed}" if neg else trimmed


def align_price_ticks(price_ticks: int, tick_size: str) -> int:
    step = parse_price_ticks(tick_size, "tick_size")
    if step <= 0:
        return max(price_ticks, 1)
    aligned = (price_ticks // step) * step
    return max(aligned, step)


def parse_qty_scaled(raw: str | Decimal, scale: int, field_name: str = "qty") -> int:
    scaled = decimal_to_scaled(raw, scale, field_name)
    if scaled <= 0:
        raise PolyesterValidationError(f"{field_name} must be positive")
    # amount_e18 / ledger scale 18 may exceed int64 (U128 on the wire).
    if scale != 18 and scaled > INT64_MAX:
        raise PolyesterValidationError(f"{field_name} exceeds int64 range")
    return scaled


def parse_required_uint64_decimal(raw: str, field_name: str) -> int:
    if not raw or not raw.isdecimal():
        raise PolyesterValidationError(f"{field_name} must be a uint64 decimal string")
    value = int(raw)
    if value > UINT64_MAX:
        raise PolyesterValidationError(f"{field_name} exceeds uint64 range")
    return value


def _encode_id(parsed: int) -> str:
    """Encode a uint64 id as canonical SDK base58 (0 maps to '1')."""
    if parsed == 0:
        return "1"
    return base58.b58encode_int(parsed).decode("ascii")


def _base58_to_int(value: str) -> int:
    raw = base58.b58decode(value)
    return int.from_bytes(raw, "big") if raw else 0


def id_to_int(value: str | int, label: str = "id") -> int:
    if isinstance(value, bool):
        raise PolyesterValidationError(f"{label} must be base58 or decimal uint64")
    if isinstance(value, int):
        parsed = value
    elif isinstance(value, str):
        if not value:
            raise PolyesterValidationError(f"{label} must be base58 or decimal uint64")
        if value.isdecimal():
            # All-digit strings are ambiguous: prefer canonical SDK base58 when it
            # round-trips via format_id, otherwise treat as decimal.
            decimal_value = int(value)
            try:
                base58_value = _base58_to_int(value)
            except ValueError:
                parsed = decimal_value
            else:
                parsed = base58_value if _encode_id(base58_value) == value else decimal_value
        else:
            try:
                parsed = _base58_to_int(value)
            except ValueError as exc:
                raise PolyesterValidationError(f"{label} must be base58 or decimal uint64") from exc
    else:
        raise PolyesterValidationError(f"{label} must be base58 or decimal uint64")
    if parsed < 0 or parsed > UINT64_MAX:
        raise PolyesterValidationError(f"{label} exceeds uint64 range")
    return parsed


def format_id(value: str | int) -> str:
    return _encode_id(id_to_int(value))


def datetime_to_timestamp_dict(value: datetime) -> dict[str, int]:
    if value.tzinfo is None:
        raise PolyesterValidationError("datetime values must be timezone-aware")
    utc = value.astimezone(UTC)
    seconds = int(utc.timestamp())
    nanos = utc.microsecond * 1000
    return {"seconds": seconds, "nanos": nanos}


def timestamp_dict_to_datetime(value: Any) -> datetime | None:
    if value is None:
        return None
    seconds = getattr(value, "seconds", None)
    nanos = getattr(value, "nanos", 0)
    if isinstance(value, dict):
        seconds = value.get("seconds")
        nanos = value.get("nanos", 0)
    if seconds is None:
        return None
    return datetime.fromtimestamp(int(seconds) + int(nanos) / 1_000_000_000, tz=UTC)


def omit_none(data: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in data.items() if value is not None}
