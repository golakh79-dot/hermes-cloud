from __future__ import annotations

import asyncio
import contextlib
from collections.abc import AsyncIterator, Callable

from polyester.models import OrderbookData


class OrderbookSubscription:
    """Stateful order book stream with snapshot prefetch and sequence-checked deltas."""

    def __init__(
        self,
        *,
        queue: asyncio.Queue[OrderbookData | None],
        close: asyncio.Event,
        stream,
        set_bucket: Callable[[str | None], None],
        start_task: asyncio.Task[None] | None = None,
    ) -> None:
        self._queue = queue
        self._close = close
        self._stream = stream
        self._set_bucket = set_bucket
        self._start_task = start_task

    def set_bucket(self, bucket: str | None) -> None:
        self._set_bucket(bucket)

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

    async def __aenter__(self) -> OrderbookSubscription:
        return self

    async def __aexit__(self, *exc_info: object) -> None:
        await self.aclose()

    def unsubscribe(self) -> None:
        """Fire-and-forget close for TS-style ergonomics in running loops."""
        asyncio.get_running_loop().create_task(self.aclose())

    def __aiter__(self) -> AsyncIterator[OrderbookData]:
        return self

    async def __anext__(self) -> OrderbookData:
        if self._close.is_set():
            raise StopAsyncIteration
        item = await self._queue.get()
        if item is None:
            raise StopAsyncIteration
        return item
