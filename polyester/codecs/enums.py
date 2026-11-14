from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from polyester.errors import PolyesterValidationError


def resolve_proto_enum(
    module,
    label: str,
    *,
    aliases: Mapping[str, int] | None = None,
    field_name: str = "value",
) -> Any:
    key = label.lower().replace("-", "_")
    if aliases and key in aliases:
        return aliases[key]
    candidates = [key.upper(), key]
    if not key.startswith("status_") and f"STATUS_{key.upper()}" in dir(module):
        candidates.append(f"STATUS_{key.upper()}")
    if not key.startswith("method_") and f"METHOD_{key.upper()}" in dir(module):
        candidates.append(f"METHOD_{key.upper()}")
    for candidate in candidates:
        value = getattr(module, candidate, None)
        if isinstance(value, int):
            return value
    raise PolyesterValidationError(f"unknown {field_name}: {label}")
