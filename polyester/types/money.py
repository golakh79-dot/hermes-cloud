"""Immutable money scalar types for SDK write and read surfaces."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum
from typing import Any

from polyester.codecs.scalars import (
    INT64_MAX,
    INT64_MIN,
    PRICE_TICK_SCALE,
    decimal_to_scaled,
    format_price_ticks,
    format_qty_scaled,
    parse_price_ticks,
    parse_qty_scaled,
    validate_protocol_scale,
)
from polyester.errors import PolyesterValidationError


class QuantityDomain(StrEnum):
    ORDER_BASE = "order_base"
    ORDER_QUOTE = "order_quote"
    ASSET = "asset"
    LEDGER_E18 = "ledger_e18"


def _reject_bool(value: Any, field_name: str) -> None:
    if isinstance(value, bool):
        raise PolyesterValidationError(f"{field_name} must not be a boolean")


def _require_scaled_int(value: int, field_name: str, *, allow_u128: bool = False) -> int:
    _reject_bool(value, field_name)
    if not isinstance(value, int):
        raise PolyesterValidationError(f"{field_name} must be an int")
    if value < 0:
        raise PolyesterValidationError(f"{field_name} must be non-negative")
    if not allow_u128 and (value < INT64_MIN or value > INT64_MAX):
        raise PolyesterValidationError(f"{field_name} exceeds int64 range")
    return value


@dataclass(frozen=True, slots=True)
class Price:
    """Resolved protocol price units (protobuf price_ticks, fixed 1e9)."""

    ticks: int
    symbol: str | None = None

    @classmethod
    def from_ticks(cls, ticks: int, *, symbol: str | None = None) -> Price:
        value = _require_scaled_int(ticks, "ticks")
        if value < 0:
            raise PolyesterValidationError("ticks must be non-negative")
        return cls(ticks=value, symbol=symbol)

    def as_decimal(self) -> Decimal:
        return Decimal(format_price_ticks(self.ticks))

    def format(self) -> str:
        return format_price_ticks(self.ticks)

    def compatible_with(self, *, symbol: str | None = None) -> None:
        if self.symbol is not None and symbol is not None and self.symbol != symbol:
            raise PolyesterValidationError(
                f"price symbol mismatch: value is for {self.symbol}, destination is {symbol}"
            )


@dataclass(frozen=True, slots=True)
class Quantity:
    """Resolved order/trigger base or quote quantity (protobuf qty_scaled)."""

    scaled: int
    scale: int | None = None
    domain: QuantityDomain = QuantityDomain.ORDER_BASE
    symbol: str | None = None
    symbol_id: int | None = None

    @classmethod
    def from_scaled(
        cls,
        scaled: int,
        *,
        scale: int | None = None,
        domain: QuantityDomain = QuantityDomain.ORDER_BASE,
        symbol: str | None = None,
        symbol_id: int | None = None,
    ) -> Quantity:
        value = _require_scaled_int(scaled, "scaled")
        if domain not in (QuantityDomain.ORDER_BASE, QuantityDomain.ORDER_QUOTE):
            raise PolyesterValidationError(
                "Quantity domain must be order_base or order_quote"
            )
        if scale is not None:
            validate_protocol_scale(scale)
        return cls(
            scaled=value,
            scale=scale,
            domain=domain,
            symbol=symbol,
            symbol_id=symbol_id,
        )

    @classmethod
    def from_quote_scaled(
        cls,
        scaled: int,
        scale: int,
        *,
        symbol: str | None = None,
        symbol_id: int | None = None,
    ) -> Quantity:
        """Construct a quote-debit budget from scaled integer units.

        ``scale`` is required so a bare integer can never silently inherit the
        catalog scale. Use
        ``CatalogManager.quote_quantity_scale_for_symbol``.
        """
        return cls.from_scaled(
            scaled,
            scale=scale,
            domain=QuantityDomain.ORDER_QUOTE,
            symbol=symbol,
            symbol_id=symbol_id,
        )

    @classmethod
    def from_quote_decimal_str(
        cls,
        raw: str,
        scale: int,
        *,
        symbol: str | None = None,
        symbol_id: int | None = None,
    ) -> Quantity:
        scaled = parse_qty_scaled(raw, scale, "quote amount")
        return cls.from_quote_scaled(
            scaled, scale, symbol=symbol, symbol_id=symbol_id
        )

    @classmethod
    def from_quote_decimal(
        cls,
        raw: Decimal,
        scale: int,
        *,
        symbol: str | None = None,
        symbol_id: int | None = None,
    ) -> Quantity:
        scaled = parse_qty_scaled(raw, scale, "quote amount")
        return cls.from_quote_scaled(
            scaled, scale, symbol=symbol, symbol_id=symbol_id
        )

    def as_decimal(self, scale: int | None = None) -> Decimal:
        resolved = scale if scale is not None else self.scale
        if resolved is None:
            raise PolyesterValidationError(
                "as_decimal requires a known scale; pass scale= or construct with scale="
            )
        validate_protocol_scale(resolved)
        return Decimal(format_qty_scaled(self.scaled, resolved))

    def format(self, scale: int | None = None) -> str:
        resolved = scale if scale is not None else self.scale
        if resolved is None:
            raise PolyesterValidationError(
                "format requires a known scale; pass scale= or construct with scale="
            )
        validate_protocol_scale(resolved)
        return format_qty_scaled(self.scaled, resolved)

    def compatible_with(
        self,
        *,
        domain: QuantityDomain = QuantityDomain.ORDER_BASE,
        scale: int | None = None,
        symbol: str | None = None,
        symbol_id: int | None = None,
    ) -> None:
        if self.domain != domain:
            raise PolyesterValidationError(
                f"quantity domain mismatch: value is {self.domain.value}, "
                f"destination is {domain.value}"
            )
        if self.scale is not None and scale is not None and self.scale != scale:
            raise PolyesterValidationError(
                f"quantity scale mismatch: value scale is {self.scale}, destination is {scale}"
            )
        if self.symbol is not None and symbol is not None and self.symbol != symbol:
            raise PolyesterValidationError(
                f"quantity symbol mismatch: value is for {self.symbol}, destination is {symbol}"
            )
        if self.symbol_id is not None and symbol_id is not None and self.symbol_id != symbol_id:
            raise PolyesterValidationError(
                f"quantity symbol_id mismatch: value is for {self.symbol_id}, "
                f"destination is {symbol_id}"
            )


@dataclass(frozen=True, slots=True)
class AssetAmount:
    """Resolved asset/ledger amount (transfer/withdraw amount_e18)."""

    scaled: int
    scale: int | None = None
    domain: QuantityDomain = QuantityDomain.ASSET
    asset_id: int | None = None

    @classmethod
    def from_scaled(
        cls,
        scaled: int,
        *,
        scale: int | None = None,
        domain: QuantityDomain = QuantityDomain.ASSET,
        asset_id: int | None = None,
    ) -> AssetAmount:
        value = _require_scaled_int(
            scaled,
            "scaled",
            allow_u128=domain == QuantityDomain.LEDGER_E18,
        )
        if scale is not None:
            validate_protocol_scale(scale)
        if domain not in (QuantityDomain.ASSET, QuantityDomain.LEDGER_E18):
            raise PolyesterValidationError("AssetAmount domain must be asset or ledger_e18")
        return cls(scaled=value, scale=scale, domain=domain, asset_id=asset_id)

    def as_decimal(self, scale: int | None = None) -> Decimal:
        resolved = scale if scale is not None else self.scale
        if resolved is None:
            raise PolyesterValidationError(
                "as_decimal requires a known scale; pass scale= or construct with scale="
            )
        validate_protocol_scale(resolved)
        return Decimal(format_qty_scaled(self.scaled, resolved))

    def format(self, scale: int | None = None) -> str:
        resolved = scale if scale is not None else self.scale
        if resolved is None:
            raise PolyesterValidationError(
                "format requires a known scale; pass scale= or construct with scale="
            )
        validate_protocol_scale(resolved)
        return format_qty_scaled(self.scaled, resolved)

    def compatible_with(
        self,
        *,
        domain: QuantityDomain = QuantityDomain.ASSET,
        scale: int | None = None,
        asset_id: int | None = None,
    ) -> None:
        if self.domain != domain:
            raise PolyesterValidationError(
                f"amount domain mismatch: value is {self.domain.value}, "
                f"destination is {domain.value}"
            )
        if self.scale is not None and scale is not None and self.scale != scale:
            raise PolyesterValidationError(
                f"amount scale mismatch: value scale is {self.scale}, destination is {scale}"
            )
        if self.asset_id is not None and asset_id is not None and self.asset_id != asset_id:
            raise PolyesterValidationError(
                f"amount asset_id mismatch: value is for {self.asset_id}, destination is {asset_id}"
            )


def resolve_price_ticks(
    value: str | Decimal | Price,
    field_name: str = "price",
    *,
    symbol: str | None = None,
) -> int:
    if isinstance(value, Price):
        value.compatible_with(symbol=symbol)
        return value.ticks
    if isinstance(value, (int, float, bool)) and not isinstance(value, Decimal):
        raise PolyesterValidationError(
            f"{field_name} must be a decimal string, Decimal, or Price "
            "(use Price.from_ticks for scaled ints)"
        )
    return parse_price_ticks(value, field_name)


def resolve_qty_scaled(
    value: str | Decimal | Quantity,
    scale: int,
    field_name: str = "qty",
    *,
    symbol: str | None = None,
    symbol_id: int | None = None,
) -> int:
    if isinstance(value, Quantity):
        value.compatible_with(
            domain=QuantityDomain.ORDER_BASE,
            scale=scale,
            symbol=symbol,
            symbol_id=symbol_id,
        )
        if value.scaled <= 0:
            raise PolyesterValidationError(f"{field_name} must be positive")
        return value.scaled
    if isinstance(value, AssetAmount):
        raise PolyesterValidationError(
            f"{field_name} expects Quantity (order/trigger), not AssetAmount"
        )
    if isinstance(value, (int, float, bool)) and not isinstance(value, Decimal):
        raise PolyesterValidationError(
            f"{field_name} must be a decimal string, Decimal, or Quantity "
            "(use Quantity.from_scaled for scaled ints)"
        )
    return parse_qty_scaled(value, scale, field_name)


def resolve_quote_qty_scaled(
    value: str | Decimal | Quantity,
    scale: int,
    field_name: str = "max_quote_debit",
    *,
    symbol: str | None = None,
    symbol_id: int | None = None,
) -> int:
    """Resolve a quote-debit budget. Typed values must carry the catalog quote scale."""
    if isinstance(value, Quantity):
        if value.scale is None:
            raise PolyesterValidationError(
                "quote amount scale is required; use "
                "Quantity.from_quote_scaled/from_quote_decimal"
            )
        value.compatible_with(
            domain=QuantityDomain.ORDER_QUOTE,
            scale=scale,
            symbol=symbol,
            symbol_id=symbol_id,
        )
        if value.scaled <= 0:
            raise PolyesterValidationError(f"{field_name} must be positive")
        return value.scaled
    if isinstance(value, AssetAmount):
        raise PolyesterValidationError(
            f"{field_name} expects Quantity (order quote), not AssetAmount"
        )
    if isinstance(value, (int, float, bool)) and not isinstance(value, Decimal):
        raise PolyesterValidationError(
            f"{field_name} must be a decimal string, Decimal, or Quantity "
            "(use Quantity.from_quote_scaled for scaled ints)"
        )
    return parse_qty_scaled(value, scale, field_name)


def resolve_asset_amount_scaled(
    value: str | Decimal | AssetAmount,
    scale: int,
    field_name: str = "amount",
    *,
    domain: QuantityDomain = QuantityDomain.ASSET,
    asset_id: int | None = None,
) -> int:
    if isinstance(value, AssetAmount):
        value.compatible_with(domain=domain, scale=scale, asset_id=asset_id)
        if value.scaled <= 0:
            raise PolyesterValidationError(f"{field_name} must be positive")
        return value.scaled
    if isinstance(value, Quantity):
        raise PolyesterValidationError(f"{field_name} expects AssetAmount, not order Quantity")
    if isinstance(value, (int, float, bool)) and not isinstance(value, Decimal):
        raise PolyesterValidationError(
            f"{field_name} must be a decimal string, Decimal, or AssetAmount "
            "(use AssetAmount.from_scaled for scaled ints)"
        )
    return parse_qty_scaled(value, scale, field_name)


def resolve_asset_amount_scaled_with_input_scale(
    value: str | Decimal | AssetAmount,
    input_scale: int | None,
    target_scale: int,
    field_name: str = "amount",
    *,
    asset_id: int | None = None,
) -> int:
    """Rescale an asset amount exactly from its declared scale to ``target_scale``."""
    validate_protocol_scale(target_scale)
    if isinstance(value, AssetAmount):
        if value.asset_id is not None and asset_id is not None and value.asset_id != asset_id:
            raise PolyesterValidationError(
                f"amount asset_id mismatch: value is for {value.asset_id}, "
                f"destination is {asset_id}"
            )
        source_scale = value.scale if value.scale is not None else input_scale
        if source_scale is None:
            raise PolyesterValidationError(
                f"{field_name} requires a declared input scale on AssetAmount or input_scale="
            )
        validate_protocol_scale(source_scale)
        scaled = value.scaled
    else:
        if input_scale is None:
            raise PolyesterValidationError(f"{field_name} requires input_scale")
        validate_protocol_scale(input_scale)
        source_scale = input_scale
        scaled = decimal_to_scaled(value, source_scale, field_name)

    if scaled <= 0:
        raise PolyesterValidationError(f"{field_name} must be positive")
    if source_scale < target_scale:
        scaled *= 10 ** (target_scale - source_scale)
    elif source_scale > target_scale:
        divisor = 10 ** (source_scale - target_scale)
        scaled, remainder = divmod(scaled, divisor)
        if remainder:
            raise PolyesterValidationError(
                f"{field_name} cannot be rescaled exactly from scale {source_scale} "
                f"to {target_scale}"
            )
    if scaled >= 1 << 128:
        raise PolyesterValidationError(f"{field_name} exceeds uint128 range")
    return scaled


__all__ = [
    "AssetAmount",
    "PRICE_TICK_SCALE",
    "Price",
    "Quantity",
    "QuantityDomain",
    "resolve_asset_amount_scaled",
    "resolve_asset_amount_scaled_with_input_scale",
    "resolve_price_ticks",
    "resolve_qty_scaled",
    "resolve_quote_qty_scaled",
]
