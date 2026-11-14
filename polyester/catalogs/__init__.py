from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from typing import Any

from polyester.catalogs.zipper import build_zipper_catalog_data
from polyester.catalogs.zipper_supply import patch_zipper_catalog_supply
from polyester.codecs.scalars import MAX_PROTOCOL_SCALE, UINT32_MAX, validate_protocol_scale
from polyester.codecs.spot_config import (
    max_open_orders_total_from_dict,
    pair_order_limits_from_dict,
)
from polyester.errors import PolyesterValidationError
from polyester.models.common import PairOrderLimits
from polyester.models.zipper import (
    DepositWithdrawConfig,
    ZippedAssetSupplyUpdate,
    ZipperCatalogData,
)


def _parse_u32_field(value: Any, *, field_name: str) -> int | None:
    """Parse a catalog id/scale candidate; reject values that would truncate as u32."""
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, str)):
        raise PolyesterValidationError(f"catalog {field_name} must be an integer")
    try:
        parsed = int(value)
    except (TypeError, ValueError) as exc:
        raise PolyesterValidationError(f"catalog {field_name} must be an integer") from exc
    if parsed < 0:
        raise PolyesterValidationError(f"catalog {field_name} must be non-negative")
    if parsed > UINT32_MAX:
        raise PolyesterValidationError(
            f"catalog {field_name} {parsed} exceeds uint32 range (silent truncation rejected)"
        )
    return parsed


def _parse_protocol_scale(value: Any, *, field_name: str) -> int | None:
    parsed = _parse_u32_field(value, field_name=field_name)
    if parsed is None:
        return None
    validate_protocol_scale(parsed, field_name=f"catalog {field_name}")
    return parsed


def _parse_positive_decimal_field(value: Any, *, field_name: str) -> str | None:
    if value is None or value == "":
        return None
    if isinstance(value, (bool, float)):
        raise PolyesterValidationError(f"catalog {field_name} must be a positive decimal string")
    try:
        parsed = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise PolyesterValidationError(
            f"catalog {field_name} must be a positive decimal string"
        ) from exc
    if parsed == 0:
        if field_name in {"min_qty_base", "min_notional_quote"}:
            # Optional protobuf minimums arrive as "0" when disabled.
            return None
        raise PolyesterValidationError(f"catalog {field_name} must be positive")
    if not parsed.is_finite() or parsed < 0:
        raise PolyesterValidationError(f"catalog {field_name} must be positive")
    return format(parsed, "f")


@dataclass(slots=True)
class CatalogManager:
    spot_config: dict[str, Any] = field(default_factory=dict)
    zipper: ZipperCatalogData | None = None
    deposit_withdraw_config: DepositWithdrawConfig | None = None
    _legacy_zipper_raw: dict[str, Any] = field(default_factory=dict)
    _unusable: bool = False
    _unusable_reason: str | None = None

    @property
    def is_unusable(self) -> bool:
        return self._unusable

    @property
    def unusable_reason(self) -> str | None:
        return self._unusable_reason

    def mark_unusable(self, reason: str) -> None:
        self._unusable = True
        self._unusable_reason = reason
        self.spot_config = {}
        self.zipper = None
        self.deposit_withdraw_config = None
        self._legacy_zipper_raw = {}

    def _reject_refresh(self, reason: str) -> None:
        """Keep a previously valid snapshot intact when a refresh is invalid."""
        if (
            self.spot_config
            or self.zipper is not None
            or self.deposit_withdraw_config is not None
            or self._legacy_zipper_raw
        ):
            return
        self.mark_unusable(reason)

    @property
    def zipper_config(self) -> dict[str, Any]:
        """Backward-compatible raw dict view of the typed zipper catalog."""
        if self.deposit_withdraw_config is None:
            return {}
        config = self.deposit_withdraw_config
        return {
            "chains": [msgspec_to_dict(chain) for chain in config.chains],
            "assets": [
                {
                    **msgspec_to_dict(asset),
                    "variants": [msgspec_to_dict(variant) for variant in asset.variants],
                }
                for asset in config.assets
            ],
            "contracts": [msgspec_to_dict(item) for item in config.contracts],
            "tsSec": config.ts_ms // 1000 if config.ts_ms else 0,
        }

    def hydrate_spot_config(self, config: dict[str, Any]) -> None:
        """Hydrate spot pairs; reject out-of-range ids/scales (no silent truncation)."""
        if not isinstance(config, dict):
            self._reject_refresh("spot catalog is not an object")
            raise PolyesterValidationError("spot catalog is not an object")
        pairs = config.get("pairs") or config.get("symbols") or []
        if not isinstance(pairs, list) or not pairs:
            self._reject_refresh("spot catalog empty or missing pairs")
            raise PolyesterValidationError("spot catalog empty or missing pairs")
        cleaned_pairs: list[dict[str, Any]] = []
        symbols_seen: set[str] = set()
        symbol_ids_seen: set[int] = set()
        try:
            for pair in pairs:
                if not isinstance(pair, dict):
                    continue
                symbol = pair.get("symbol")
                symbol_id_raw = (
                    pair.get("symbol_id")
                    if pair.get("symbol_id") is not None
                    else pair.get("symbolId")
                )
                symbol_id = _parse_u32_field(
                    symbol_id_raw,
                    field_name="symbol_id",
                )
                scale = _parse_protocol_scale(
                    pair.get("base_quantity_scale")
                    if pair.get("base_quantity_scale") is not None
                    else pair.get("baseQuantityScale")
                    if pair.get("baseQuantityScale") is not None
                    else pair.get("qtyScale"),
                    field_name="base_quantity_scale",
                )
                row = dict(pair)
                if not isinstance(symbol, str) or not symbol.strip():
                    raise PolyesterValidationError("catalog symbol is required")
                if symbol_id is None or symbol_id == 0:
                    raise PolyesterValidationError("catalog symbol_id must be non-zero")
                if scale is None:
                    raise PolyesterValidationError("catalog base_quantity_scale is required")
                quote_scale = _parse_protocol_scale(
                    pair.get("quote_quantity_scale")
                    if pair.get("quote_quantity_scale") is not None
                    else pair.get("quoteQuantityScale"),
                    field_name="quote_quantity_scale",
                )
                for snake, camel in (
                    ("tick_size", "tickSize"),
                    ("step_size", "stepSize"),
                    ("min_qty_base", "minQtyBase"),
                    ("min_notional_quote", "minNotionalQuote"),
                ):
                    parsed_constraint = _parse_positive_decimal_field(
                        pair.get(snake) if pair.get(snake) is not None else pair.get(camel),
                        field_name=snake,
                    )
                    if parsed_constraint is not None:
                        row[snake] = parsed_constraint
                    else:
                        row.pop(snake, None)
                        row.pop(camel, None)
                if symbol in symbols_seen:
                    raise PolyesterValidationError(f"catalog contains duplicate symbol {symbol!r}")
                if symbol_id in symbol_ids_seen:
                    raise PolyesterValidationError(
                        f"catalog contains duplicate symbol_id {symbol_id}"
                    )
                # Fail closed on malformed limits, like the other constraints.
                pair_order_limits_from_dict(row)
                symbols_seen.add(symbol)
                symbol_ids_seen.add(symbol_id)
                row["symbol_id"] = symbol_id
                row["base_quantity_scale"] = scale
                if quote_scale is not None:
                    row["quote_quantity_scale"] = quote_scale
                cleaned_pairs.append(row)
            max_open_orders_total_from_dict(config)
        except PolyesterValidationError as exc:
            self._reject_refresh(str(exc))
            raise
        if not cleaned_pairs:
            self._reject_refresh("spot catalog contained no usable pairs")
            raise PolyesterValidationError("spot catalog contained no usable pairs")
        self._unusable = False
        self._unusable_reason = None
        self.spot_config = {**config, "pairs": cleaned_pairs}

    def hydrate_zipper_config(
        self,
        config: DepositWithdrawConfig | dict[str, Any],
    ) -> None:
        if isinstance(config, DepositWithdrawConfig):
            self.hydrate_zipper_config_typed(config)
            return
        if not isinstance(config, dict):
            self._reject_refresh("zipper catalog is not an object")
            raise PolyesterValidationError("zipper catalog is not an object")
        assets = config.get("assets") or []
        if not isinstance(assets, list):
            self._reject_refresh("zipper catalog assets must be a list")
            raise PolyesterValidationError("zipper catalog assets must be a list")
        assets_seen: set[str] = set()
        ledger_ids_seen: set[int] = set()
        zipped_ids_seen: set[int] = set()
        try:
            for row in assets:
                if not isinstance(row, dict):
                    continue
                ledger_id_raw = (
                    row.get("ledgerId") if row.get("ledgerId") is not None else row.get("ledger_id")
                )
                asset = row.get("asset") or row.get("code")
                if not isinstance(asset, str) or not asset.strip():
                    raise PolyesterValidationError("catalog asset is required")
                ledger_id = _parse_u32_field(
                    ledger_id_raw,
                    field_name="ledger_id",
                )
                if ledger_id is None or ledger_id == 0:
                    raise PolyesterValidationError("catalog ledger_id must be non-zero")
                scale_raw = (
                    row.get("quantityScale")
                    if row.get("quantityScale") is not None
                    else row.get("quantity_scale")
                )
                if scale_raw is None:
                    raise PolyesterValidationError("catalog quantity_scale is required")
                _parse_protocol_scale(scale_raw, field_name="quantity_scale")
                if asset in assets_seen:
                    raise PolyesterValidationError(f"catalog contains duplicate asset {asset!r}")
                if ledger_id in ledger_ids_seen:
                    raise PolyesterValidationError(
                        f"catalog contains duplicate ledger_id {ledger_id}"
                    )
                assets_seen.add(asset)
                ledger_ids_seen.add(ledger_id)
                for variant in row.get("variants") or []:
                    if not isinstance(variant, dict):
                        raise PolyesterValidationError("catalog variant must be an object")
                    zipped_id = _parse_u32_field(
                        variant.get("zippedAssetId")
                        if variant.get("zippedAssetId") is not None
                        else variant.get("zipped_asset_id"),
                        field_name="zipped_asset_id",
                    )
                    if zipped_id is None or zipped_id == 0:
                        raise PolyesterValidationError("catalog zipped_asset_id must be non-zero")
                    if zipped_id in zipped_ids_seen:
                        raise PolyesterValidationError(
                            f"catalog contains duplicate zipped_asset_id {zipped_id}"
                        )
                    zipped_ids_seen.add(zipped_id)
        except PolyesterValidationError as exc:
            self._reject_refresh(str(exc))
            raise
        self.deposit_withdraw_config = None
        self.zipper = None
        self._legacy_zipper_raw = config
        self._unusable = False
        self._unusable_reason = None

    def hydrate_zipper_config_typed(self, config: DepositWithdrawConfig) -> None:
        """Hydrate from the typed deposit/withdraw config (no consumer JSON round-trip)."""
        assets_seen: set[str] = set()
        ledger_ids_seen: set[int] = set()
        zipped_ids_seen: set[int] = set()
        try:
            for asset in config.assets:
                if not asset.asset.strip():
                    raise PolyesterValidationError("catalog asset is required")
                ledger_id = _parse_u32_field(asset.ledger_id, field_name="ledger_id")
                if ledger_id is None or ledger_id == 0:
                    raise PolyesterValidationError("catalog ledger_id must be non-zero")
                validate_protocol_scale(
                    int(asset.quantity_scale),
                    field_name="catalog quantity_scale",
                )
                if asset.asset in assets_seen:
                    raise PolyesterValidationError(
                        f"catalog contains duplicate asset {asset.asset!r}"
                    )
                if ledger_id in ledger_ids_seen:
                    raise PolyesterValidationError(
                        f"catalog contains duplicate ledger_id {ledger_id}"
                    )
                assets_seen.add(asset.asset)
                ledger_ids_seen.add(ledger_id)
                for variant in asset.variants:
                    zipped_id = _parse_u32_field(
                        variant.zipped_asset_id, field_name="zipped_asset_id"
                    )
                    if zipped_id is None or zipped_id == 0:
                        raise PolyesterValidationError("catalog zipped_asset_id must be non-zero")
                    if zipped_id in zipped_ids_seen:
                        raise PolyesterValidationError(
                            f"catalog contains duplicate zipped_asset_id {zipped_id}"
                        )
                    zipped_ids_seen.add(zipped_id)
        except PolyesterValidationError as exc:
            self._reject_refresh(str(exc))
            raise
        self.deposit_withdraw_config = config
        self.zipper = build_zipper_catalog_data(config)
        self._legacy_zipper_raw = {}
        self._unusable = False
        self._unusable_reason = None

    def hydrate_deposit_withdraw_config(self, config: DepositWithdrawConfig) -> None:
        self.hydrate_zipper_config_typed(config)

    def symbol_id_for_symbol(self, symbol: str) -> int | None:
        if self._unusable:
            return None
        for pair in self._pairs():
            if pair.get("symbol") == symbol:
                value = pair.get("symbol_id") or pair.get("symbolId")
                return int(value) if value is not None else None
        return None

    def symbol_for_symbol_id(self, symbol_id: int) -> str | None:
        if self._unusable or not symbol_id:
            return None
        for pair in self._pairs():
            value = pair.get("symbol_id") or pair.get("symbolId")
            if value is not None and int(value) == int(symbol_id):
                symbol = pair.get("symbol")
                return str(symbol) if symbol else None
        return None

    def base_quantity_scale_for_symbol(self, symbol: str) -> int | None:
        """Return the pair base quantity scale, or None when unknown/unhydrated.

        Never invents scale 8 for missing symbols — callers that need a decode
        fallback must choose it explicitly.
        """
        if self._unusable:
            return None
        for pair in self._pairs():
            if pair.get("symbol") == symbol:
                value = pair.get("base_quantity_scale")
                if value is None:
                    value = pair.get("baseQuantityScale")
                if value is None:
                    value = pair.get("qtyScale")
                return int(value) if value is not None else None
        return None

    def quote_quantity_scale_for_symbol(self, symbol: str) -> int | None:
        """Return the pair quote quantity scale, or None when unknown/unhydrated."""
        if self._unusable:
            return None
        for pair in self._pairs():
            if pair.get("symbol") == symbol:
                value = pair.get("quote_quantity_scale")
                if value is None:
                    value = pair.get("quoteQuantityScale")
                return int(value) if value is not None else None
        return None

    def market_data_volume_scale_for_symbol_id(self, symbol_id: int) -> int | None:
        """Return the base asset candle/overview volume scale, or None when missing.

        Zero is valid and is returned as 0.
        """
        if self._unusable:
            return None
        pair = self._pair_for_symbol_id(symbol_id)
        if pair is None:
            return None
        base = pair.get("base_asset")
        if base is None:
            base = pair.get("baseAsset")
        if not isinstance(base, str) or not base:
            return None
        for asset in self._assets():
            code = asset.get("asset")
            if code != base:
                continue
            return _optional_int(
                asset, "market_data_volume_scale", "marketDataVolumeScale"
            )
        return None

    def order_limits_for_symbol(self, symbol: str) -> PairOrderLimits | None:
        """Return the pair's order-size and open-order limits, or None when unknown."""
        if self._unusable:
            return None
        pair = self._pair_for_symbol(symbol)
        return pair_order_limits_from_dict(pair) if pair is not None else None

    def order_limits_for_symbol_id(self, symbol_id: int) -> PairOrderLimits | None:
        if self._unusable:
            return None
        pair = self._pair_for_symbol_id(symbol_id)
        return pair_order_limits_from_dict(pair) if pair is not None else None

    @property
    def max_open_orders_total(self) -> int:
        """Venue default resting-order limit across all pairs; ``0`` when unpublished."""
        if self._unusable or not self.spot_config:
            return 0
        return max_open_orders_total_from_dict(self.spot_config)

    def reference_price_scale_for_symbol_id(self, symbol_id: int) -> int | None:
        """Return the pair reference-candle price scale, or None when missing."""
        if self._unusable:
            return None
        pair = self._pair_for_symbol_id(symbol_id)
        if pair is None:
            return None
        return _optional_int(pair, "reference_price_scale", "referencePriceScale")

    def base_quantity_scale_for_symbol_id(self, symbol_id: int) -> int | None:
        if self._unusable:
            return None
        for pair in self._pairs():
            value = pair.get("symbol_id") or pair.get("symbolId")
            if value is not None and int(value) == int(symbol_id):
                symbol = pair.get("symbol")
                if symbol:
                    return self.base_quantity_scale_for_symbol(str(symbol))
                break
        return None

    def orderbook_price_buckets_for_symbol(self, symbol: str) -> list[str]:
        pair = self._pair_for_symbol(symbol)
        if pair is None:
            return []
        marketdata = pair.get("marketdata") or pair.get("marketData") or {}
        buckets = marketdata.get("orderbook_price_buckets") or marketdata.get(
            "orderbookPriceBuckets"
        )
        if not isinstance(buckets, list):
            return []
        result: list[str] = []
        for value in buckets:
            if isinstance(value, (int, float)):
                text = format(value, "f").rstrip("0").rstrip(".") or "0"
                result.append(text)
            elif value is not None:
                result.append(str(value))
        return result

    def ledger_id_for_asset(self, asset_symbol: str) -> int | None:
        if self._unusable:
            return None
        catalog = self.zipper
        if catalog is not None:
            for asset in catalog.assets:
                if asset.asset == asset_symbol:
                    return asset.ledger_id or None
        raw = self._legacy_zipper_raw or self.zipper_config
        for row in raw.get("assets") or []:
            symbol = row.get("asset") or row.get("code")
            if symbol == asset_symbol:
                value = row.get("ledgerId") or row.get("ledger_id")
                return int(value) if value is not None else None
        return None

    def quantity_scale_for_asset(self, asset_symbol: str) -> int | None:
        if self._unusable:
            return None
        catalog = self.zipper
        if catalog is not None:
            for asset in catalog.assets:
                if asset.asset == asset_symbol:
                    return asset.quantity_scale
        raw = self._legacy_zipper_raw or self.zipper_config
        for row in raw.get("assets") or []:
            symbol = row.get("asset") or row.get("code")
            if symbol == asset_symbol:
                value = row.get("quantityScale")
                if value is None:
                    value = row.get("quantity_scale")
                return int(value) if value is not None else None
        return None

    def quantity_scale_for_zipped_asset_id(self, zipped_asset_id: int) -> int | None:
        catalog = self.zipper
        if catalog is not None:
            for asset in catalog.assets:
                for chain in asset.chains:
                    if chain.zipped_asset_id == zipped_asset_id:
                        return asset.quantity_scale
        return None

    def patch_zipper_supply(self, updates: list[ZippedAssetSupplyUpdate]) -> bool:
        if self.zipper is None or not updates:
            return False
        patched = patch_zipper_catalog_supply(self.zipper, updates)
        if patched is self.zipper:
            return False
        self.zipper = patched
        return True

    def _pair_for_symbol(self, symbol: str) -> dict[str, Any] | None:
        for pair in self._pairs():
            if pair.get("symbol") == symbol:
                return pair
        return None

    def _pairs(self) -> list[dict[str, Any]]:
        pairs = self.spot_config.get("pairs") or self.spot_config.get("symbols") or []
        return [pair for pair in pairs if isinstance(pair, dict)]

    def _assets(self) -> list[dict[str, Any]]:
        assets = self.spot_config.get("assets") or []
        return [asset for asset in assets if isinstance(asset, dict)]

    def _pair_for_symbol_id(self, symbol_id: int) -> dict[str, Any] | None:
        for pair in self._pairs():
            value = pair.get("symbol_id")
            if value is None:
                value = pair.get("symbolId")
            if value is not None and int(value) == int(symbol_id):
                return pair
        return None


def _optional_int(row: dict[str, Any], *keys: str) -> int | None:
    for key in keys:
        if key not in row or row[key] is None:
            continue
        return int(row[key])
    return None


def msgspec_to_dict(value: object) -> dict[str, Any]:
    import msgspec

    return msgspec.to_builtins(value)


__all__ = [
    "MAX_PROTOCOL_SCALE",
    "CatalogManager",
    "msgspec_to_dict",
]
