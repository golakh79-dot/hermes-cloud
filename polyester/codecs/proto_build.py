from __future__ import annotations

from typing import Any

from google.protobuf.json_format import ParseDict
from google.protobuf.message import Message


def message_from_mapping(
    proto_cls: type[Message],
    value: dict[str, Any] | Message | None,
) -> Message:
    if value is None:
        return proto_cls()
    if isinstance(value, Message):
        return value
    msg = proto_cls()
    ParseDict(value, msg, ignore_unknown_fields=True)
    return msg


def repeated_messages_from_mappings(
    proto_cls: type[Message],
    values: list[dict[str, Any] | Message] | None,
) -> list[Message]:
    if not values:
        return []
    return [message_from_mapping(proto_cls, item) for item in values]
