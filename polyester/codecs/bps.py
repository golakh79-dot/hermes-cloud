from __future__ import annotations

from polyester.errors import PolyesterValidationError

MAX_BPS = 10_000
# A slippage cap on anything that sells, and on every trailing stop, stops
# short of 100%, which would leave no positive price to sell at.
MAX_SELL_SLIPPAGE_BPS = MAX_BPS - 1


def validate_bps(
    value: object,
    field_name: str,
    *,
    allow_clear: bool = False,
    max_value: int = MAX_BPS,
) -> int:
    """Validate a basis-point field before assigning it to protobuf."""
    if isinstance(value, bool) or not isinstance(value, (int, str)):
        raise PolyesterValidationError(f"{field_name} must be an integer")
    try:
        parsed = int(value)
    except ValueError as exc:
        raise PolyesterValidationError(f"{field_name} must be an integer") from exc
    if allow_clear and parsed == 0:
        return parsed
    if parsed < 1 or parsed > max_value:
        raise PolyesterValidationError(f"{field_name} must be between 1 and {max_value}")
    return parsed


def max_slippage_bps_for_side(side: str) -> int:
    """Largest market slippage cap for an execution on ``side``: 10000 bps to
    buy, 9999 to sell."""
    return MAX_SELL_SLIPPAGE_BPS if side == "sell" else MAX_BPS
