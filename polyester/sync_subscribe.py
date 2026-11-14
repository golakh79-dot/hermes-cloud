from __future__ import annotations

import asyncio
import contextlib
from collections.abc import Awaitable, Callable, Coroutine
from concurrent.futures import Future
from typing import Any, TypeVar

from polyester.realtime.client import AsyncSubscription

T = TypeVar("T")


class SyncSubscription:
    """Thread-safe handle for a sync client realtime subscription."""

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        *,
        close_coro: Callable[[], Coroutine[Any, Any, None]],
        holder: dict[str, object | None] | None = None,
    ) -> None:
        self._loop = loop
        self._close_coro = close_coro
        self._holder = holder
        self._closed = False

    def set_bucket(self, bucket: str | None) -> None:
        """Forward bucket changes to orderbook subscriptions (no-op otherwise)."""
        if self._holder is None:
            return
        sub = self._holder.get("sub")
        if sub is not None and hasattr(sub, "set_bucket"):
            self._loop.call_soon_threadsafe(sub.set_bucket, bucket)

    def unsubscribe(self) -> None:
        self.close()

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        future: Future[None] = asyncio.run_coroutine_threadsafe(self._close_coro(), self._loop)
        future.result(timeout=10)


def subscribe_sync(
    loop: asyncio.AbstractEventLoop,
    subscribe: Callable[[], Awaitable[AsyncSubscription[T]]],
    *,
    on_event: Callable[[T], None],
    on_error: Callable[[Exception], None] | None = None,
) -> SyncSubscription:
    holder: dict[str, object | None] = {"sub": None, "task": None}

    async def _consume() -> None:
        sub = await subscribe()
        holder["sub"] = sub
        try:
            async for event in sub:
                on_event(event)
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            if on_error is not None:
                on_error(exc)
            else:
                raise

    async def _close() -> None:
        task = holder.get("task")
        if isinstance(task, asyncio.Task):
            task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await task
        sub = holder.get("sub")
        if sub is not None:
            aclose = getattr(sub, "aclose", None)
            if callable(aclose):
                await aclose()

    async def _start() -> None:
        holder["task"] = asyncio.create_task(_consume())

    asyncio.run_coroutine_threadsafe(_start(), loop).result(timeout=10)
    return SyncSubscription(loop, close_coro=_close, holder=holder)
