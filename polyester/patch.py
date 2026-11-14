from __future__ import annotations

from typing import Any

from google.protobuf.field_mask_pb2 import FieldMask

from polyester.errors import PolyesterValidationError

UNSET: Any = object()


def is_set(value: object) -> bool:
    return value is not UNSET


def require_positive_revision(expected_revision: int) -> None:
    if expected_revision <= 0:
        raise PolyesterValidationError("expected_revision must be positive")


def field_mask(paths: list[str]) -> FieldMask:
    if not paths:
        raise PolyesterValidationError("update_mask must be non-empty")
    return FieldMask(paths=paths)
