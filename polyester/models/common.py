from __future__ import annotations

from decimal import Decimal
from typing import Any

import msgspec

from polyester.models.trading import Order, OrderMutationResult, OrdersList
from polyester.types.money import Price, Quantity

# Backward-compatible aliases for early alpha imports.
OpenOrdersResult = OrdersList
CreateOrderResult = OrderMutationResult

# Public write inputs: human decimal or resolved typed scalars.
QtyInput = str | Decimal | Quantity
PriceInput = str | Decimal | Price


class OrderbookLevel(msgspec.Struct, kw_only=True, omit_defaults=True):
    price: Price | None = None
    qty: Quantity | None = None


class OrderbookData(msgspec.Struct, kw_only=True, omit_defaults=True):
    """An order book at ``book_seq``.

    ``available`` is ``False`` while the server is building the book or after
    it invalidated it: its levels are then unknown, not empty, so do not read
    empty sides as no liquidity; request the snapshot again later. Only a
    snapshot carries it: a subscription's book reports the value of the last
    snapshot it applied, and deltas, resets included, do not change it.
    """

    symbol: str
    depth: int
    book_seq: str
    bids: list[OrderbookLevel]
    asks: list[OrderbookLevel]
    available: bool = True


class ApiData(msgspec.Struct, kw_only=True, omit_defaults=True):
    """Escape hatch for responses not yet modeled as typed structs."""

    raw: dict[str, Any]


class PairOrderLimits(msgspec.Struct, kw_only=True, omit_defaults=True):
    """Per-order and open-order limits of one spot pair.

    The decimal maxima are ``None`` when the pair has no maximum.
    ``max_open_orders_per_pair`` is the venue default for a typical account
    (``0`` when unpublished); an account may have a lower limit of its own.
    """

    symbol: str
    symbol_id: int
    # Largest quantity of one limit order in base units; a replacement counts
    # its new total less the filled quantity.
    max_limit_qty_base: str | None = None
    # Largest quantity of one market order in base units, after converting a
    # quote-sized order to base.
    max_market_qty_base: str | None = None
    # Largest notional of one order in quote units: quantity times limit price,
    # or times protection price for a market order.
    max_order_notional_quote: str | None = None
    # Largest notional of one market order in quote units, valued at the top
    # of its band: a buy at its protection price, a sell at its reference price.
    max_market_notional_quote: str | None = None
    # Default resting-order (GTC and GTD) limit on this pair.
    max_open_orders_per_pair: int = 0


class SpotConfig(msgspec.Struct, kw_only=True, omit_defaults=True):
    """Spot pair catalog payload. Prefer resolving symbols via ``client.catalogs``."""

    raw: dict[str, Any]
    pair_order_limits: list[PairOrderLimits] = []
    # Default resting-order limit for a typical account across all pairs
    # (``0`` when unpublished); an account may have a lower limit of its own.
    max_open_orders_total: int = 0


class CreateOrderRequest(msgspec.Struct, kw_only=True, omit_defaults=True):
    symbol: str | None = None
    symbol_id: int | None = None
    side: str
    order_type: str
    tif: str | None = None
    # Any: msgspec accepts str | Decimal | Quantity at runtime.
    qty: Any | None = None
    # BUY market-IOC and limit-IOC orders may instead specify a quote budget.
    # Decimal/str inputs use the hydrated catalog quote_quantity_scale.
    # Typed Quantity values must use QuantityDomain.ORDER_QUOTE and embed that
    # same catalog scale (Quantity.from_quote_scaled / from_quote_decimal).
    max_quote_debit: Any | None = None
    price: Any | None = None
    sub_account_id: str | None = None
    # Optional. Set a stable non-empty value so you can reconcile after an
    # ambiguous failure. Look up that id before creating again; a second
    # create with the same id is always a conflict if the first attempt admitted.
    client_order_id: str | None = None
    post_only: bool = False
    # Required RFC3339 UTC timestamp when tif="gtd"; rejected otherwise.
    # Maps to proto LimitGtd.expire_at (1 second–30 days after validation).
    expires_at: str | None = None
    # Friendly dict, proto-JSON, or AttachedRisk. Encoded in risk_policy_from_dict.
    attached_risk: Any | None = None
    market_client_ref_price: Any | None = None
    fee_asset: str | None = None
    # Market-IOC execution protection. Set at most one; both omitted keeps
    # pair defaults. Rejected on limit orders. ``max_slippage_bps`` is 1–10000.
    max_slippage_ticks: int | None = None
    max_slippage_bps: int | None = None


__all__ = [
    "CreateOrderRequest",
    "CreateOrderResult",
    "OpenOrdersResult",
    "Order",
    "OrderbookData",
    "OrderbookLevel",
    "PairOrderLimits",
    "SpotConfig",
]
