from __future__ import annotations

from google.protobuf.internal.enum_type_wrapper import EnumTypeWrapper
from google.protobuf.message import Message

from polyester.codecs.scalars import format_id

_ENUM_PREFIXES = (
    "SIDE_",
    "ORDER_TYPE_",
    "ORDER_STATUS_",
    "TIF_",
    "FLOW_STEP_",
    "FLOW_KIND_",
    "KIND_",
    "MODIFY_ACTION_",
    "API_KEY_STATUS_",
    "TRIGGER_TYPE_",
    "TRIGGER_STATUS_",
    "TRIGGER_EVENT_TYPE_",
    "TRIGGER_CANCEL_REASON_",
    "TRIGGER_FAILURE_REASON_",
    "STATUS_",
    "EVENT_",
    "TIME_IN_FORCE_",
    "SELF_TRADE_PREVENTION_MODE_",
    "BALANCE_RANGE_",
    "PROTECTED_ACTION_",
    "SCOPE_",
    "ENTRY_KIND_",
    "DESTINATION_",
    "INTERNAL_WHITELIST_",
    "TRANSFER_COUNTERPARTY_",
    "SUBACCOUNT_STATUS_",
)


def format_uint64_id(value: int) -> str:
    if value == 0:
        return "0"
    return format_id(value)


def u128_to_str(hi: int, lo: int) -> str:
    return str((int(hi) << 64) + int(lo))


def proto_enum_name(enum_type: EnumTypeWrapper, value: int) -> str:
    if value == 0:
        return ""
    try:
        name = enum_type.Name(value)
    except (ValueError, TypeError):
        return str(value)
    if isinstance(name, str):
        for prefix in _ENUM_PREFIXES:
            if name.startswith(prefix):
                return name[len(prefix) :].lower()
        return name.lower()
    return str(value)


def error_code_name(enum_type: EnumTypeWrapper, value: int) -> str:
    """Name of a server error code, or ``UNKNOWN_ERROR_CODE(n)`` for a number
    this SDK's generated enum does not define yet."""
    try:
        return enum_type.Name(value)
    except (ValueError, TypeError):
        return f"UNKNOWN_ERROR_CODE({value})"


def has_field(message: Message, field_name: str) -> bool:
    try:
        return message.HasField(field_name)
    except ValueError:
        return False


def timestamp_to_ms(msg: Message | None) -> int:
    if msg is None:
        return 0
    seconds = int(getattr(msg, "seconds", 0) or 0)
    nanos = int(getattr(msg, "nanos", 0) or 0)
    if seconds == 0 and nanos == 0:
        return 0
    return seconds * 1000 + nanos // 1_000_000


def timestamp_to_rfc3339(msg: Message | None) -> str | None:
    """Encode a proto Timestamp as RFC3339 UTC, or None when unset/zero."""
    if msg is None:
        return None
    seconds = int(getattr(msg, "seconds", 0) or 0)
    nanos = int(getattr(msg, "nanos", 0) or 0)
    if seconds == 0 and nanos == 0:
        return None
    from datetime import UTC, datetime

    dt = datetime.fromtimestamp(seconds + nanos / 1_000_000_000, tz=UTC)
    if nanos == 0:
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    return dt.strftime("%Y-%m-%dT%H:%M:%S.") + f"{nanos:09d}Z"


def bytes_to_hex(value: bytes | None) -> str:
    if not value:
        return ""
    return f"0x{value.hex()}"
