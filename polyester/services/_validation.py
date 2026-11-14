from __future__ import annotations

from typing import Literal, overload

from polyester.errors import PolyesterValidationError


@overload
def validate_limit(
    limit: int,
    *,
    label: str = "limit",
    allow_none: Literal[False] = False,
) -> int: ...


@overload
def validate_limit(
    limit: int | None,
    *,
    label: str = "limit",
    allow_none: Literal[True],
) -> int | None: ...


def validate_limit(
    limit: int | None,
    *,
    label: str = "limit",
    allow_none: bool = False,
) -> int | None:
    """Wire-safety for pagination limits (no SDK-wide max policy).

    Rejects ``bool`` and non-integers so values cannot silently coerce on the
    wire. Endpoint/server protos remain the authority for allowed ranges.
    Optional limits omit when ``None`` so server defaults are preserved.
    """
    if limit is None:
        if allow_none:
            return None
        raise PolyesterValidationError(f"{label} must be an integer")
    if isinstance(limit, bool) or not isinstance(limit, int):
        raise PolyesterValidationError(f"{label} must be an integer")
    return limit
