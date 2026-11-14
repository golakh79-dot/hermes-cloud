from __future__ import annotations

from polyester.gen.orderbook.v1 import orderbook_pb2
from polyester.models import OrderbookData, OrderbookLevel
from polyester.orderbook.local_book import format_orderbook_level


def orderbook_level_from_proto(
    msg: orderbook_pb2.PriceLevel,
    *,
    quantity_scale: int,
) -> OrderbookLevel:
    return format_orderbook_level(
        price_ticks=int(msg.price_ticks),
        qty_scaled=int(msg.qty_scaled),
        quantity_scale=quantity_scale,
    )


def orderbook_from_proto(
    msg: orderbook_pb2.GetOrderBookResponse,
    *,
    symbol: str,
    depth: int,
    quantity_scale: int,
) -> OrderbookData:
    return OrderbookData(
        symbol=symbol,
        depth=depth,
        book_seq=str(msg.book_seq),
        bids=[orderbook_level_from_proto(item, quantity_scale=quantity_scale) for item in msg.bids],
        asks=[orderbook_level_from_proto(item, quantity_scale=quantity_scale) for item in msg.asks],
        available=bool(msg.available),
    )
