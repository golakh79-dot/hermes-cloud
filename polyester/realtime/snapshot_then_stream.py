from __future__ import annotations

import asyncio
import contextlib
import threading
from collections.abc import Awaitable, Callable
from typing import Generic, TypeVar

from polyester.errors import PolyesterRealtimeError, PolyesterRealtimeOverflowError
from polyester.realtime.client import AsyncRealtimeClient, AsyncSubscription, _ReconnectBackoff

TSnapshot = TypeVar("TSnapshot")
TPublication = TypeVar("TPublication")

_RECONNECT_SNAPSHOT_RETRIES = 1
_REQUEST_REFRESH_MAX_ATTEMPTS = 4
_REQUEST_REFRESH_INITIAL_BACKOFF = 0.05
_REQUEST_REFRESH_MAX_BACKOFF = 0.4


class AsyncSnapshotThenStreamSubscription(Generic[TSnapshot, TPublication]):
    """Fetch a snapshot, buffer publications until ready, and refresh on disconnect."""

    def __init__(
        self,
        *,
        realtime: AsyncRealtimeClient,
        channel: str,
        decode: Callable[[bytes], TPublication],
        fetch_snapshot: Callable[[], Awaitable[TSnapshot]],
        read_publication: Callable[[TPublication], list[TPublication]],
        apply_snapshot: Callable[[TSnapshot, list[TPublication]], None],
        apply_live_publications: Callable[[list[TPublication]], None],
        max_buffered_publications: int = 200,
        on_open: Callable[[], None] | None = None,
        on_close: Callable[[], None] | None = None,
        on_error: Callable[[Exception], None] | None = None,
        on_reconnect: Callable[[], None] | None = None,
        on_snapshot_refresh: Callable[[], None] | None = None,
    ) -> None:
        self._realtime = realtime
        self._channel = channel
        self._decode = decode
        self._fetch_snapshot = fetch_snapshot
        self._read_publication = read_publication
        self._apply_snapshot = apply_snapshot
        self._apply_live_publications = apply_live_publications
        self._max_buffered_publications = max_buffered_publications
        self._on_open = on_open
        self._on_close = on_close
        self._on_error = on_error
        self._on_reconnect = on_reconnect
        self._on_snapshot_refresh = on_snapshot_refresh

        self._ready = False
        self._disposed = False
        self._generation = 0
        self._pending: list[TPublication] = []
        self._lock = asyncio.Lock()
        self._state_lock = threading.Lock()
        self._ws_sub: AsyncSubscription[TPublication] | None = None
        self._runner_task: asyncio.Task[None] | None = None
        self._request_refresh_task: asyncio.Task[None] | None = None
        self._refresh_requested = False
        self._last_error: BaseException | None = None
        self._initial_handshake: asyncio.Future[None] | None = None

    @property
    def last_error(self) -> BaseException | None:
        """Terminal or latest snapshot/stream error; cleared only after a successful refresh."""
        return self._last_error

    def err(self) -> BaseException | None:
        return self._last_error

    async def start(self) -> None:
        if self._runner_task is not None:
            return
        self._initial_handshake = asyncio.get_running_loop().create_future()
        self._runner_task = asyncio.create_task(self._run_ws_loop())
        try:
            await self._initial_handshake
            if not await self.refresh_snapshot():
                error = self._last_error or PolyesterRealtimeError("initial snapshot failed")
                raise error
        except BaseException as exc:
            if isinstance(exc, Exception):
                self._last_error = exc
                self._report_snapshot_error(exc)
            await self.aclose()
            raise

    def is_ready(self) -> bool:
        return self._ready

    def is_disposed(self) -> bool:
        return self._disposed

    async def refresh_snapshot(self) -> bool:
        """Fetch snapshot and merge buffered publications.

        Returns True on success. On failure, stores ``last_error``, keeps ready=False,
        and returns False (does not raise — callers decide retry/fail-closed policy).
        """
        async with self._lock:
            generation = self._generation + 1
            self._generation = generation
            with self._state_lock:
                self._ready = False
            # Publications buffered during a failed refresh must survive for
            # the next successful retry and be merged exactly once.
            try:
                snapshot = await self._fetch_snapshot()
            except Exception as exc:
                if not self._disposed:
                    self._last_error = exc
                    self._report_snapshot_error(exc)
                return False
            if self._disposed or generation != self._generation:
                return False
            buffered = self._take_pending()
            try:
                self._apply_snapshot(snapshot, buffered)
            except Exception as exc:
                self._fail_closed(
                    PolyesterRealtimeError(f"apply_snapshot callback failed: {exc}")
                )
                return False
            while True:
                next_buffered = self._take_pending_or_mark_ready(generation)
                if next_buffered is None:
                    return False
                if not next_buffered:
                    break
                try:
                    self._apply_live_publications(next_buffered)
                except Exception as exc:
                    self._fail_closed(
                        PolyesterRealtimeError(
                            f"apply_live_publications callback failed: {exc}"
                        )
                    )
                    return False
            self._last_error = None
            self._notify(self._on_snapshot_refresh)
            return True

    async def aclose(self) -> None:
        self._disposed = True
        self._generation += 1
        with self._state_lock:
            self._ready = False
            self._pending.clear()
        if self._request_refresh_task is not None and not self._request_refresh_task.done():
            self._request_refresh_task.cancel()
        if self._runner_task is not None and not self._runner_task.done():
            self._runner_task.cancel()
            with contextlib.suppress(asyncio.CancelledError, Exception):
                await asyncio.wait_for(self._runner_task, timeout=2.0)
        if self._ws_sub is not None:
            await self._ws_sub.aclose()

    def _take_pending(self) -> list[TPublication]:
        with self._state_lock:
            buffered = self._pending
            self._pending = []
            return buffered

    def _take_pending_or_mark_ready(
        self, generation: int
    ) -> list[TPublication] | None:
        with self._state_lock:
            if self._disposed or generation != self._generation:
                return None
            if self._pending:
                buffered = self._pending
                self._pending = []
                return buffered
            self._ready = True
            return []

    def _handle_publication(self, message: TPublication) -> None:
        try:
            publications = self._read_publication(message)
        except Exception as exc:
            self._fail_closed(
                PolyesterRealtimeError(f"read_publication callback failed: {exc}")
            )
            return
        if not publications:
            return
        overflow: PolyesterRealtimeOverflowError | None = None
        buffered = False
        with self._state_lock:
            if not self._ready:
                buffered = True
                self._pending.extend(publications)
                if len(self._pending) > self._max_buffered_publications:
                    self._pending.clear()
                    overflow = PolyesterRealtimeOverflowError(
                        "snapshot recovery buffer full; recreate the subscription"
                    )
        if overflow is not None:
            self._fail_closed(overflow)
            return
        if buffered:
            return
        try:
            self._apply_live_publications(publications)
        except Exception as exc:
            self._fail_closed(
                PolyesterRealtimeError(f"apply_live_publications callback failed: {exc}")
            )

    def request_refresh(self) -> None:
        """Coalesce refresh requests into one bounded fail-closed worker."""
        if self._disposed:
            return
        self._refresh_requested = True
        self._generation += 1
        with self._state_lock:
            self._ready = False
        if self._request_refresh_task is None or self._request_refresh_task.done():
            self._request_refresh_task = asyncio.get_running_loop().create_task(
                self._run_requested_refreshes()
            )

    async def _run_requested_refreshes(self) -> None:
        attempts = 0
        try:
            while not self._disposed:
                self._refresh_requested = False
                attempts += 1
                succeeded = await self.refresh_snapshot()
                follow_up = self._refresh_requested
                if succeeded and not follow_up:
                    return
                if attempts >= _REQUEST_REFRESH_MAX_ATTEMPTS:
                    if succeeded:
                        self._fail_closed(
                            PolyesterRealtimeError(
                                "snapshot refresh did not converge after repeated "
                                "publication gaps"
                            )
                        )
                    else:
                        error = self._last_error
                        if not isinstance(error, Exception):
                            error = PolyesterRealtimeError(
                                "snapshot refresh failed after bounded retries"
                            )
                        self._fail_closed(error)
                    return
                delay = min(
                    _REQUEST_REFRESH_INITIAL_BACKOFF * (2 ** (attempts - 1)),
                    _REQUEST_REFRESH_MAX_BACKOFF,
                )
                await asyncio.sleep(delay)
        except asyncio.CancelledError:
            return

    async def _refresh_after_reconnect(self) -> None:
        """One bounded retry on reconnect, then fail-closed."""
        for attempt in range(_RECONNECT_SNAPSHOT_RETRIES + 1):
            if self._disposed:
                return
            if await self.refresh_snapshot():
                return
            if attempt < _RECONNECT_SNAPSHOT_RETRIES:
                await asyncio.sleep(0.05)
        # Fail closed: stop the stream with the stored snapshot error.
        if self._last_error is None:
            self._last_error = PolyesterRealtimeError(
                "snapshot refresh failed after reconnect; subscription closed"
            )
        self._disposed = True
        self._ready = False
        self._report_snapshot_error(
            self._last_error
            if isinstance(self._last_error, Exception)
            else Exception(str(self._last_error))
        )

    async def _run_ws_loop(self) -> None:
        first = True
        backoff = _ReconnectBackoff()
        while not self._disposed:
            sub: AsyncSubscription[TPublication] | None = None
            try:
                # Disable transport auto-reconnect so this loop can refresh
                # REST snapshot state between reconnect attempts.
                sub = await self._realtime.subscribe_proto(
                    self._channel,
                    decode=self._decode,
                    auto_reconnect=False,
                )
                if self._disposed:
                    await sub.aclose()
                    break
                self._ws_sub = sub
                backoff.reset()
                if (
                    first
                    and self._initial_handshake is not None
                    and not self._initial_handshake.done()
                ):
                    self._initial_handshake.set_result(None)
                self._notify(self._on_open)
                if not first:
                    self._notify(self._on_reconnect)
                    await self._refresh_after_reconnect()
                    if self._disposed:
                        await sub.aclose()
                        break
                first = False
                async for message in sub:
                    if self._disposed:
                        break
                    self._handle_publication(message)
                if sub.error is not None:
                    self._last_error = sub.error
                    self._report_snapshot_error(
                        sub.error
                        if isinstance(sub.error, Exception)
                        else Exception(str(sub.error))
                    )
            except asyncio.CancelledError:
                break
            except Exception as exc:
                if not self._disposed:
                    self._last_error = exc
                    if (
                        first
                        and self._initial_handshake is not None
                        and not self._initial_handshake.done()
                    ):
                        self._initial_handshake.set_exception(exc)
                        return
                    self._report_snapshot_error(exc)
            finally:
                if sub is not None:
                    await sub.aclose()
                self._ws_sub = None
            if self._disposed:
                break
            self._notify(self._on_close)
            await asyncio.sleep(backoff.next_delay())

    def _report_snapshot_error(self, error: Exception) -> None:
        if self._on_error is not None:
            with contextlib.suppress(BaseException):
                self._on_error(error)

    @staticmethod
    def _notify(callback: Callable[[], None] | None) -> None:
        if callback is not None:
            with contextlib.suppress(BaseException):
                callback()

    def _fail_closed(self, error: Exception) -> None:
        self._last_error = error
        self._disposed = True
        self._generation += 1
        with self._state_lock:
            self._ready = False
            self._pending.clear()
        self._report_snapshot_error(error)
