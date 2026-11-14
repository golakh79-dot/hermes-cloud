from __future__ import annotations

import asyncio
import builtins
import contextlib
from collections.abc import Awaitable, Callable

from polyester.catalogs import CatalogManager
from polyester.codecs.decode.market_overview import (
    currency_conversion_config_from_proto,
    currency_conversion_rates_from_proto,
    market_overview_list_from_proto,
    spot_volume_history_from_proto,
)
from polyester.codecs.realtime_decode import decode_market_overview_batch_bytes
from polyester.errors import PolyesterValidationError
from polyester.gen.marketoverview.v1.marketoverview_connect import MarketOverviewServiceClient
from polyester.gen.marketoverview.v1.marketoverview_pb2 import (
    GetCurrencyConversionConfigRequest,
    GetCurrencyConversionRatesRequest,
    GetSpotVolumeHistoryRequest,
    ListMarketOverviewRequest,
)
from polyester.market_overview.subscription import MarketOverviewSubscription
from polyester.models.market import (
    CurrencyConversionConfig,
    CurrencyConversionRates,
    MarketOverviewEntry,
    MarketOverviewList,
    SpotVolumeHistory,
)
from polyester.realtime.client import AsyncRealtimeClient, AsyncSubscription
from polyester.realtime.snapshot_then_stream import AsyncSnapshotThenStreamSubscription
from polyester.services._base import BaseService
from polyester.services._generated import unary_public_decoded
from polyester.services._realtime_subscribe import require_realtime, subscribe_public_proto
from polyester.services._symbols import resolve_symbol_ids
from polyester.services._validation import validate_limit


class AsyncMarketOverviewService(BaseService):
    def __init__(
        self,
        transport,
        *,
        catalogs: CatalogManager | None = None,
        realtime: AsyncRealtimeClient | None = None,
        wait_for_catalogs: Callable[[], Awaitable[None]] | None = None,
    ) -> None:
        super().__init__(transport)
        self._catalogs = catalogs or CatalogManager()
        self._realtime = realtime
        self._wait_for_catalogs = wait_for_catalogs

    async def _ensure_catalogs(self) -> None:
        if self._wait_for_catalogs is not None:
            await self._wait_for_catalogs()

    async def list(
        self,
        *,
        symbols: builtins.list[str] | None = None,
        limit: int = 50,
        page_token: str = "",
        include_sparklines: bool = False,
    ) -> MarketOverviewList:
        validated_limit = validate_limit(limit)
        if symbols:
            await self._ensure_catalogs()
        request = ListMarketOverviewRequest(
            limit=validated_limit,
            page_token=page_token,
            include_sparklines=include_sparklines,
        )
        resolved_ids = resolve_symbol_ids(
            self._catalogs, symbols, label="market_overview.list symbols"
        )
        if resolved_ids:
            request.symbol_id.extend(resolved_ids)
        return await unary_public_decoded(
            self._transport,
            MarketOverviewServiceClient,
            lambda client, req: client.list_market_overview(req),
            request,
            lambda msg: market_overview_list_from_proto(msg, self._catalogs),
        )

    async def get_spot_volume_history(
        self,
        *,
        symbols: builtins.list[str] | None = None,
        symbol_ids: builtins.list[int] | None = None,
    ) -> SpotVolumeHistory:
        """Trailing 24-hour USD volume samples for configured spot pairs.

        Omit both filters to select every configured pair. Send at most 2,000
        distinct positive pair IDs. Do not sum the overlapping samples.
        """
        if symbols and symbol_ids:
            raise PolyesterValidationError(
                "market_overview.get_spot_volume_history accepts only one of symbols or symbol_ids"
            )
        request = GetSpotVolumeHistoryRequest()
        resolved: list[int] = []
        if symbol_ids:
            seen: set[int] = set()
            for value in symbol_ids:
                sid = int(value)
                if sid <= 0:
                    raise PolyesterValidationError(
                        "market_overview.get_spot_volume_history symbol_ids must be positive"
                    )
                if sid in seen:
                    continue
                seen.add(sid)
                resolved.append(sid)
        elif symbols:
            await self._ensure_catalogs()
            resolved = resolve_symbol_ids(
                self._catalogs, symbols, label="market_overview.get_spot_volume_history symbols"
            )
        if len(resolved) > 2_000:
            raise PolyesterValidationError(
                "market_overview.get_spot_volume_history accepts at most 2000 symbol_ids"
            )
        if resolved:
            request.symbol_id.extend(resolved)
        return await unary_public_decoded(
            self._transport,
            MarketOverviewServiceClient,
            lambda client, req: client.get_spot_volume_history(req),
            request,
            lambda msg: spot_volume_history_from_proto(msg, self._catalogs),
        )

    async def get_currency_conversion_config(self) -> CurrencyConversionConfig:
        """Supported fiat and stablecoin display metadata.

        Entries are ordered by code. Names, symbols, and fraction digits are
        presentation defaults; fraction digits do not specify rate precision.
        Configuration remains available before rates are observed.
        """
        return await unary_public_decoded(
            self._transport,
            MarketOverviewServiceClient,
            lambda client, req: client.get_currency_conversion_config(req),
            GetCurrencyConversionConfigRequest(),
            currency_conversion_config_from_proto,
        )

    async def get_currency_conversion_rates(self) -> CurrencyConversionRates:
        """Fiat units per USD and USD per stablecoin unit.

        Fiat ``units_per_usd_e8`` is currency units per 1 USD, scaled by 1e8
        (USD identity is 100_000_000). Stablecoin ``usd_per_unit_e8`` is
        observed USD per unit at the same scale. A missing fiat snapshot or
        omitted stablecoin is unobserved, not zero. The request fails with
        unavailable (HTTP 503) before any observation exists.
        """
        return await unary_public_decoded(
            self._transport,
            MarketOverviewServiceClient,
            lambda client, req: client.get_currency_conversion_rates(req),
            GetCurrencyConversionRatesRequest(),
            currency_conversion_rates_from_proto,
        )

    async def subscribe(self) -> AsyncSubscription[MarketOverviewList]:
        """Raw Centrifugo batches (no snapshot merge). Prefer ``create_subscription``."""
        return await subscribe_public_proto(
            self._realtime,
            channel="public:spot:market_overview:updates:proto",
            decode=lambda payload: decode_market_overview_batch_bytes(payload, self._catalogs),
        )

    async def create_subscription(
        self,
        *,
        symbols: builtins.list[str] | None = None,
        limit: int = 50,
        include_sparklines: bool = False,
        on_event: Callable[[builtins.list[MarketOverviewEntry]], None] | None = None,
        on_open: Callable[[], None] | None = None,
        on_close: Callable[[], None] | None = None,
        on_error: Callable[[Exception], None] | None = None,
    ) -> MarketOverviewSubscription:
        """Snapshot-then-stream merged overview rows (TS parity).

        With ``symbols``, the snapshot and every live or buffered update keep
        only those markets; the channel itself publishes all markets.
        """
        realtime = require_realtime(self._realtime)
        channel = "public:spot:market_overview:updates:proto"
        if symbols:
            await self._ensure_catalogs()
        wanted_ids = set(
            resolve_symbol_ids(self._catalogs, symbols, label="market_overview.subscribe symbols")
        )
        by_symbol_id: dict[int, MarketOverviewEntry] = {}
        queue: asyncio.Queue[list[MarketOverviewEntry] | None] = asyncio.Queue(maxsize=50)
        close = asyncio.Event()

        def emit() -> None:
            if close.is_set():
                return
            snapshot = list(by_symbol_id.values())
            if on_event is not None:
                on_event(snapshot)
            if close.is_set():
                return
            try:
                from polyester.realtime.client import enqueue_or_overflow

                enqueue_or_overflow(
                    queue,
                    snapshot,
                    close=close,
                    message="market overview subscription queue full; consumer too slow",
                )
            except Exception:
                close.set()
                with contextlib.suppress(asyncio.QueueFull):
                    queue.put_nowait(None)

        def matches_symbol(row: MarketOverviewEntry) -> bool:
            return not wanted_ids or row.symbol_id in wanted_ids

        def apply_rows(rows: list[MarketOverviewEntry]) -> None:
            for row in rows:
                if matches_symbol(row):
                    by_symbol_id[row.symbol_id] = row

        async def fetch_snapshot() -> MarketOverviewList:
            return await self.list(
                symbols=symbols,
                limit=limit,
                include_sparklines=include_sparklines,
            )

        def apply_snapshot(
            snapshot: MarketOverviewList,
            buffered: list[MarketOverviewEntry],
        ) -> None:
            by_symbol_id.clear()
            apply_rows(snapshot.markets)
            apply_rows(buffered)
            emit()

        def apply_live(rows: list[MarketOverviewEntry]) -> None:
            apply_rows(rows)
            emit()

        stream = AsyncSnapshotThenStreamSubscription(
            realtime=realtime,
            channel=channel,
            decode=lambda payload: decode_market_overview_batch_bytes(payload, self._catalogs),
            fetch_snapshot=fetch_snapshot,
            read_publication=lambda batch: [row for row in batch.markets if matches_symbol(row)],
            apply_snapshot=apply_snapshot,
            apply_live_publications=apply_live,
            max_buffered_publications=2000,
            on_open=on_open,
            on_close=on_close,
            on_error=on_error,
        )

        subscription = MarketOverviewSubscription(
            queue=queue,
            close=close,
            stream=stream,
        )
        try:
            await stream.start()
        except BaseException:
            await subscription.aclose()
            raise
        return subscription
