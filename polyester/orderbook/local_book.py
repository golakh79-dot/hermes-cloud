from __future__ import annotations

from polyester.codecs.scalars import parse_price_ticks
from polyester.errors import PolyesterValidationError
from polyester.models import OrderbookData, OrderbookLevel
from polyester.models.realtime import OrderBookDeltaUpdate

BookSide = dict[int, int]


def levels_to_map(levels: list[tuple[str, str]] | None) -> BookSide:
    book: BookSide = {}
    for price_ticks, qty_scaled in levels or []:
        price = int(price_ticks)
        qty = int(qty_scaled)
        if price <= 0:
            raise PolyesterValidationError("orderbook level has invalid or missing price")
        if qty <= 0:
            raise PolyesterValidationError("orderbook level has invalid or missing quantity")
        book[price] = qty
    return book


def levels_from_proto_levels(
    levels: list[object] | None,
    *,
    price_attr: str = "price_ticks",
    qty_attr: str = "qty_scaled",
) -> BookSide:
    book: BookSide = {}
    for level in levels or []:
        price = int(getattr(level, price_attr))
        qty = int(getattr(level, qty_attr))
        if price <= 0:
            raise PolyesterValidationError("orderbook level has invalid or missing price")
        if qty <= 0:
            raise PolyesterValidationError("orderbook level has invalid or missing quantity")
        book[price] = qty
    return book


def apply_side_delta(book: BookSide, levels: list[tuple[str, str]] | None) -> None:
    for price_ticks, qty_scaled in levels or []:
        price = int(price_ticks)
        qty = int(qty_scaled)
        # Negative price/qty is wire corruption; never materialize it into the book.
        if price < 0 or qty < 0:
            continue
        if qty == 0:
            book.pop(price, None)
        else:
            book[price] = qty


def bucket_side(book: BookSide, bucket_ticks: int | None, *, asks: bool = False) -> BookSide:
    if not bucket_ticks or bucket_ticks <= 0:
        for price_ticks, qty_scaled in book.items():
            if price_ticks < 0:
                raise PolyesterValidationError("orderbook price ticks must be non-negative")
            if qty_scaled < 0:
                raise PolyesterValidationError("orderbook quantity must be non-negative")
        return book
    aggregated: BookSide = {}
    for price_ticks, qty_scaled in book.items():
        if price_ticks < 0:
            raise PolyesterValidationError("orderbook price ticks must be non-negative")
        if qty_scaled <= 0:
            continue
        floor = (price_ticks // bucket_ticks) * bucket_ticks
        bucket_price = floor
        if asks and price_ticks % bucket_ticks != 0:
            bucket_price = floor + bucket_ticks
        aggregated[bucket_price] = aggregated.get(bucket_price, 0) + qty_scaled
    return aggregated


def format_orderbook_level(
    *,
    price_ticks: int,
    qty_scaled: int,
    quantity_scale: int,
    symbol: str | None = None,
) -> OrderbookLevel:
    from polyester.types.money import Price, Quantity

    if price_ticks <= 0:
        raise PolyesterValidationError("orderbook level has invalid or missing price")
    if qty_scaled <= 0:
        raise PolyesterValidationError("orderbook level has invalid or missing quantity")
    return OrderbookLevel(
        price=Price.from_ticks(price_ticks, symbol=symbol),
        qty=Quantity.from_scaled(qty_scaled, scale=quantity_scale, symbol=symbol),
    )


def side_to_levels(
    book: BookSide,
    *,
    side: str,
    limit: int,
    quantity_scale: int,
    bucket_ticks: int | None = None,
) -> list[OrderbookLevel]:
    view = bucket_side(book, bucket_ticks, asks=side == "asks")
    entries = list(view.items())
    entries.sort(
        key=lambda item: item[0],
        reverse=side == "bids",
    )
    return [
        format_orderbook_level(
            price_ticks=price,
            qty_scaled=qty,
            quantity_scale=quantity_scale,
        )
        for price, qty in entries[:limit]
    ]


def build_orderbook_data(
    *,
    symbol: str,
    depth: int,
    book_seq: int,
    bids: BookSide,
    asks: BookSide,
    quantity_scale: int,
    bucket_ticks: int | None = None,
    available: bool = True,
) -> OrderbookData:
    return OrderbookData(
        symbol=symbol,
        depth=depth,
        book_seq=str(book_seq),
        available=available,
        bids=side_to_levels(
            bids,
            side="bids",
            limit=depth,
            bucket_ticks=bucket_ticks,
            quantity_scale=quantity_scale,
        ),
        asks=side_to_levels(
            asks,
            side="asks",
            limit=depth,
            bucket_ticks=bucket_ticks,
            quantity_scale=quantity_scale,
        ),
    )


def parse_bucket_ticks(bucket: str | None) -> int | None:
    if not bucket:
        return None
    try:
        return parse_price_ticks(bucket, "bucket")
    except Exception:
        return None


def apply_delta(
    *,
    bids: BookSide,
    asks: BookSide,
    current_book_seq: int,
    delta: OrderBookDeltaUpdate,
) -> tuple[int, bool]:
    """Apply one delta. Returns (new_book_seq, needs_snapshot_refresh)."""
    # Reject the whole update atomically. Skipping corrupt rows while advancing
    # the sequence permanently leaves stale quantity in the local book.
    pairs = [*delta.bids, *delta.asks]
    if any(int(price) < 0 or int(qty) < 0 for price, qty in pairs):
        return current_book_seq, True

    try:
        seq_start = int(delta.book_seq_start)
        seq_end = int(delta.book_seq_end)
    except (TypeError, ValueError):
        return current_book_seq, True
    if seq_start < 0 or seq_end < seq_start:
        return current_book_seq, True

    # A reset is a complete replacement through seq_end. A snapshot at the
    # same or newer sequence is already authoritative, so a buffered reset
    # must not clear or rewind it. A reset that reaches a newer sequence can
    # safely replace the book even if its range starts before or after the
    # current sequence.
    if delta.reset and seq_end <= current_book_seq:
        return current_book_seq, False

    if not delta.reset and current_book_seq != 0 and seq_start > current_book_seq + 1:
        return current_book_seq, True

    if not delta.reset and seq_end <= current_book_seq:
        return current_book_seq, False

    if delta.reset:
        bids.clear()
        asks.clear()
        current_book_seq = 0

    apply_side_delta(bids, list(delta.bids))
    apply_side_delta(asks, list(delta.asks))
    if seq_end > current_book_seq:
        current_book_seq = seq_end
    return current_book_seq, False
