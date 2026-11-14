from __future__ import annotations

import asyncio
import contextlib
from collections.abc import AsyncIterator

from polyester.models.market import MarketOverviewEntry


class MarketOverviewSubscription:
    """Merged market-overview stream: REST snapshot then realtime row updates."""

    def __init__(
        self,
        *,
        queue: asyncio.Queue[list[MarketOverviewEntry] | None],
        close: asyncio.Event,
        stream,
        start_task: asyncio.Task[None] | None = None,
    ) -> None:
        self._queue = queue
        self._close = close
        self._stream = stream
        self._start_task = start_task

    @property
    def last_error(self) -> BaseException | None:
        stream = self._stream
        return getattr(stream, "last_error", None)

    async def refresh_snapshot(self) -> None:
        await self._stream.refresh_snapshot()

    async def aclose(self) -> None:
        self._close.set()
        await self._stream.aclose()
        if self._start_task is not None and not self._start_task.done():
            with contextlib.suppress(asyncio.CancelledError, Exception):
                await self._start_task
        await self._queue.put(None)

    async def __aenter__(self) -> MarketOverviewSubscription:
        return self

    async def __aexit__(self, *exc_info: object) -> None:
        await self.aclose()

    def unsubscribe(self) -> None:
        asyncio.get_running_loop().create_task(self.aclose())

    def __aiter__(self) -> AsyncIterator[list[MarketOverviewEntry]]:
        return self

    async def __anext__(self) -> list[MarketOverviewEntry]:
        if self._close.is_set():
            raise StopAsyncIteration
        item = await self._queue.get()
        if item is None:
            raise StopAsyncIteration
        return item
