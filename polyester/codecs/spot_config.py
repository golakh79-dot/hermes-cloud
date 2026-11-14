"""Typed order limits from the GetSpotConfig catalog."""

from __future__ import annotations

import re
from typing import Any

from polyester.codecs.scalars import UINT32_MAX
from polyester.errors import PolyesterValidationError
from polyester.models.common import PairOrderLimits, SpotConfig

_DECIMAL_LIMIT = re.compile(r"^\d+(?:\.\d+)?$")


def _field(row: dict[str, Any], snake: str, camel: str) -> Any:
    value = row.get(snake)
    return row.get(camel) if value is None else value


def _decimal_limit(row: dict[str, Any], snake: str, camel: str) -> str | None:
    """A decimal maximum; ``None`` when the pair has no maximum (empty or absent)."""
    value = _field(row, snake, camel)
    if value is None or value == "":
        return None
    if not isinstance(value, str) or not _DECIMAL_LIMIT.match(value):
        raise PolyesterValidationError(
            f"spot config {snake} must be a non-negative decimal string, got {value!r}"
        )
    return value


def _open_orders_limit(row: dict[str, Any], snake: str, camel: str) -> int:
    value = _field(row, snake, camel)
    if value is None or value == "":
        return 0
    if isinstance(value, bool) or not isinstance(value, (int, str)):
        raise PolyesterValidationError(f"spot config {snake} must be an integer")
    try:
        parsed = int(value)
    except ValueError as exc:
        raise PolyesterValidationError(f"spot config {snake} must be an integer") from exc
    if not 0 <= parsed <= UINT32_MAX:
        raise PolyesterValidationError(f"spot config {snake} {parsed} is outside uint32 range")
    return parsed


def pair_order_limits_from_dict(pair: dict[str, Any]) -> PairOrderLimits:
    symbol_id = _field(pair, "symbol_id", "symbolId")
    return PairOrderLimits(
        symbol=str(pair.get("symbol") or ""),
        symbol_id=int(symbol_id or 0),
        max_limit_qty_base=_decimal_limit(pair, "max_limit_qty_base", "maxLimitQtyBase"),
        max_market_qty_base=_decimal_limit(pair, "max_market_qty_base", "maxMarketQtyBase"),
        max_order_notional_quote=_decimal_limit(
            pair, "max_order_notional_quote", "maxOrderNotionalQuote"
        ),
        max_market_notional_quote=_decimal_limit(
            pair, "max_market_notional_quote", "maxMarketNotionalQuote"
        ),
        max_open_orders_per_pair=_open_orders_limit(
            pair, "max_open_orders_per_pair", "maxOpenOrdersPerPair"
        ),
    )


def max_open_orders_total_from_dict(config: dict[str, Any]) -> int:
    return _open_orders_limit(config, "max_open_orders_total", "maxOpenOrdersTotal")


def spot_config_from_dict(raw: dict[str, Any]) -> SpotConfig:
    pairs = raw.get("pairs") or []
    return SpotConfig(
        raw=raw,
        pair_order_limits=[
            pair_order_limits_from_dict(pair) for pair in pairs if isinstance(pair, dict)
        ],
        max_open_orders_total=max_open_orders_total_from_dict(raw),
    )
