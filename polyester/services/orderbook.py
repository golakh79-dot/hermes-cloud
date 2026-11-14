from __future__ import annotations

import asyncio
import contextlib
from collections.abc import Callable

from polyester.catalogs import CatalogManager
from polyester.codecs.decode.orderbook import orderbook_from_proto
from polyester.codecs.orderbook import depth_to_connect_enum
from polyester.codecs.realtime_decode import decode_orderbook_delta_bytes
from polyester.errors import PolyesterValidationError
from polyester.gen.orderbook.v1.orderbook_connect import OrderbookServiceClient
from polyester.gen.orderbook.v1.orderbook_pb2 import GetOrderBookRequest
from polyester.models import OrderbookData
from polyester.models.realtime import OrderBookDeltaUpdate
from polyester.orderbook.local_book import (
    apply_delta,
    build_orderbook_data,
    levels_from_proto_levels,
    parse_bucket_ticks,
)
from polyester.orderbook.subscription import OrderbookSubscription
from polyester.realtime.client import AsyncRealtimeClient, AsyncSubscription
from polyester.realtime.snapshot_then_stream import AsyncSnapshotThenStreamSubscription
from polyester.services._base import BaseService
from polyester.services._generated import unary_public_decoded
from polyester.services._realtime_subscribe import require_realtime, subscribe_public_proto


class AsyncOrderbookService(BaseService):
    def __init__(
        self,
        transport,
        *,
        catalogs: CatalogManager | None = None,
        realtime: AsyncRealtimeClient | None = None,
    ) -> None:
        super().__init__(transport)
        self._catalogs = catalogs or CatalogManager()
        self._realtime = realtime

    def _require_quantity_scale(self, symbol: str) -> int:
        scale = self._catalogs.base_quantity_scale_for_symbol(symbol)
        if scale is None:
            raise PolyesterValidationError(
                f"orderbook decoding requires a hydrated catalog quantity scale for {symbol!r}"
            )
        return scale

    async def get(self, *, symbol: str, depth: int = 50) -> OrderbookData:
        from polyester.gen.orderbook.v1 import orderbook_pb2
        from polyester.services._symbols import resolve_symbol_id

        depth_enum = getattr(orderbook_pb2, depth_to_connect_enum(depth))
        request = GetOrderBookRequest(
            symbol_id=resolve_symbol_id(
                self._catalogs, symbol=symbol, symbol_id=None, label="orderbook.get"
            ),
            depth=depth_enum,
        )
        return await unary_public_decoded(
            self._transport,
            OrderbookServiceClient,
            lambda client, req: client.get_order_book(req),
            request,
            lambda msg: orderbook_from_proto(
                msg,
                symbol=symbol,
                depth=depth,
                quantity_scale=self._require_quantity_scale(symbol),
            ),
        )

    async def subscribe_deltas(
        self,
        *,
        symbol_id: int,
        depth: int = 50,
    ) -> AsyncSubscription[OrderBookDeltaUpdate]:
        ws_depth = min(500, max(1, int(depth)))
        channel = f"public:spot:orderbook:deltas:depth:{ws_depth}:{symbol_id}:proto"
        return await subscribe_public_proto(
            self._realtime,
            channel=channel,
            decode=decode_orderbook_delta_bytes,
        )

    async def create_subscription(
        self,
        *,
        symbol: str,
        symbol_id: int | None = None,
        depth: int = 50,
        bucket: str | None = None,
        on_event: Callable[[OrderbookData], None] | None = None,
        on_open: Callable[[], None] | None = None,
        on_close: Callable[[], None] | None = None,
        on_error: Callable[[Exception], None] | None = None,
        on_sequence_gap: Callable[[], None] | None = None,
        on_reconnect: Callable[[], None] | None = None,
        on_snapshot_refresh: Callable[[], None] | None = None,
    ) -> OrderbookSubscription:
        """Snapshot + sequence-checked delta stream with optional price bucketing."""
        realtime = require_realtime(self._realtime)
        resolved_symbol_id = symbol_id
        if resolved_symbol_id is None:
            resolved_symbol_id = self._catalogs.symbol_id_for_symbol(symbol)
        if resolved_symbol_id is None or resolved_symbol_id <= 0:
            raise PolyesterValidationError(
                f"symbol_id is required for orderbook subscriptions ({symbol!r})"
            )

        ws_depth = min(500, max(1, int(depth)))
        channel = f"public:spot:orderbook:deltas:depth:{ws_depth}:{resolved_symbol_id}:proto"

        bids_map: dict[int, int] = {}
        asks_map: dict[int, int] = {}
        current_book_seq = 0
        # The last snapshot's wire ``available``; deltas, resets included, never change it.
        book_available = True
        bucket_ticks: int | None = parse_bucket_ticks(bucket)
        queue: asyncio.Queue[OrderbookData | None] = asyncio.Queue(maxsize=200)
        close = asyncio.Event()
        stream_holder: dict[str, AsyncSnapshotThenStreamSubscription | None] = {"stream": None}

        def emit() -> None:
            if close.is_set():
                return
            data = build_orderbook_data(
                symbol=symbol,
                depth=ws_depth,
                book_seq=current_book_seq,
                bids=bids_map,
                asks=asks_map,
                bucket_ticks=bucket_ticks,
                quantity_scale=self._require_quantity_scale(symbol),
                available=book_available,
            )
            if on_event is not None:
                on_event(data)
            if close.is_set():
                return
            try:
                from polyester.realtime.client import enqueue_or_overflow

                enqueue_or_overflow(
                    queue,
                    data,
                    close=close,
                    message="orderbook subscription queue full; consumer too slow",
                )
            except Exception as exc:
                if on_error is not None:
                    with contextlib.suppress(BaseException):
                        on_error(exc)
                close.set()
                with contextlib.suppress(asyncio.QueueFull):
                    queue.put_nowait(None)

        def set_bucket(value: str | None) -> None:
            nonlocal bucket_ticks
            bucket_ticks = parse_bucket_ticks(value)
            if stream_holder["stream"] is not None and stream_holder["stream"].is_ready():
                emit()

        async def fetch_snapshot():
            from polyester.gen.orderbook.v1 import orderbook_pb2

            depth_enum = getattr(orderbook_pb2, depth_to_connect_enum(ws_depth))
            request = GetOrderBookRequest(symbol_id=resolved_symbol_id, depth=depth_enum)
            return await unary_public_decoded(
                self._transport,
                OrderbookServiceClient,
                lambda client, req: client.get_order_book(req),
                request,
                lambda msg: msg,
            )

        def apply_snapshot(snapshot, buffered_deltas: list[OrderBookDeltaUpdate]) -> None:
            nonlocal bids_map, asks_map, current_book_seq, book_available
            bids_map = levels_from_proto_levels(snapshot.bids)
            asks_map = levels_from_proto_levels(snapshot.asks)
            current_book_seq = int(snapshot.book_seq or 0)
            book_available = bool(snapshot.available)
            emit()
            for delta in buffered_deltas:
                if close.is_set():
                    return
                handle_delta(delta)

        def apply_live_publications(deltas: list[OrderBookDeltaUpdate]) -> None:
            for delta in deltas:
                if close.is_set():
                    return
                handle_delta(delta)

        def handle_delta(delta: OrderBookDeltaUpdate) -> None:
            nonlocal current_book_seq
            current_book_seq, needs_refresh = apply_delta(
                bids=bids_map,
                asks=asks_map,
                current_book_seq=current_book_seq,
                delta=delta,
            )
            if needs_refresh:
                if on_sequence_gap is not None:
                    on_sequence_gap()
                stream = stream_holder["stream"]
                if stream is not None and not stream.is_disposed():
                    stream.request_refresh()
                return
            emit()

        stream = AsyncSnapshotThenStreamSubscription(
            realtime=realtime,
            channel=channel,
            decode=decode_orderbook_delta_bytes,
            fetch_snapshot=fetch_snapshot,
            read_publication=lambda delta: [delta],
            apply_snapshot=apply_snapshot,
            apply_live_publications=apply_live_publications,
            on_open=on_open,
            on_close=on_close,
            on_error=on_error,
            on_reconnect=on_reconnect,
            on_snapshot_refresh=on_snapshot_refresh,
        )
        stream_holder["stream"] = stream

        subscription = OrderbookSubscription(
            queue=queue,
            close=close,
            stream=stream,
            set_bucket=set_bucket,
        )
        try:
            await stream.start()
        except BaseException:
            await subscription.aclose()
            raise
        return subscription

    async def subscribe(
        self,
        *,
        symbol: str,
        symbol_id: int | None = None,
        depth: int = 50,
        bucket: str | None = None,
        on_event: Callable[[OrderbookData], None] | None = None,
        on_open: Callable[[], None] | None = None,
        on_close: Callable[[], None] | None = None,
        on_error: Callable[[Exception], None] | None = None,
        on_sequence_gap: Callable[[], None] | None = None,
        on_reconnect: Callable[[], None] | None = None,
        on_snapshot_refresh: Callable[[], None] | None = None,
    ) -> OrderbookSubscription:
        """Convenience wrapper around create_subscription."""
        return await self.create_subscription(
            symbol=symbol,
            symbol_id=symbol_id,
            depth=depth,
            bucket=bucket,
            on_event=on_event,
            on_open=on_open,
            on_close=on_close,
            on_error=on_error,
            on_sequence_gap=on_sequence_gap,
            on_reconnect=on_reconnect,
            on_snapshot_refresh=on_snapshot_refresh,
        )
