"""Account order streams over the private WebSocket (``GET /v1/ws/private``).

One connection carries every account subscription. Each account has one
server subscription shared by all of its consumers. A subscription resumes
from its last applied cursor after a sequence gap, an expired token or a
reconnect; a snapshot is staged and installed only at ``snapshotEnd``.
"""

from __future__ import annotations

import asyncio
import contextlib
import secrets
import time
from collections.abc import Awaitable, Callable, Coroutine
from dataclasses import dataclass
from typing import Any, Literal
from urllib.parse import urlsplit, urlunsplit

from websockets.asyncio.client import ClientConnection, connect
from websockets.exceptions import ConnectionClosed

from polyester.codecs.decode.private_orders import (
    private_orders_from_proto,
    private_orders_unit_from_proto,
)
from polyester.codecs.scalars import format_id, id_to_int
from polyester.errors import (
    PolyesterAuthError,
    PolyesterRealtimeError,
    PolyesterRealtimeOverflowError,
    PolyesterValidationError,
)
from polyester.gen.orders.v1.orders_read_pb2 import Order as OrderPb
from polyester.gen.privatews.v1 import private_ws_pb2 as pb
from polyester.models.private_orders import (
    PrivateOrdersConnected,
    PrivateOrdersDisconnected,
    PrivateOrdersError,
    PrivateOrdersEvent,
    PrivateOrdersReady,
    PrivateOrdersSnapshot,
    PrivateOrdersStale,
)
from polyester.models.trading import Order
from polyester.realtime.client import WS_MAX_MESSAGE_BYTES, AsyncSubscription

PRIVATE_WS_PATH = "/v1/ws/private"
PRIVATE_WS_SUBPROTOCOL = "polyester.v1.proto"
# The server sends a heartbeat every second; a connection silent this long is stale.
HEARTBEAT_TIMEOUT = 3.0
RECONNECT_BASE_DELAY = 0.5
RECONNECT_MAX_DELAY = 10.0
# A connection that stayed up this long resets the reconnect backoff.
STABLE_CONNECTION = 10.0
OPEN_TIMEOUT = 10.0
# A malformed frame (4400) and a rejected connect token (4403) recur on every reconnect.
TERMINAL_CLOSE_CODES = frozenset({4400, 4403})
HEARTBEAT_TIMEOUT_CLOSE_CODE = 4000


def private_ws_url(api_url: str) -> str:
    """The private WebSocket URL on the API host (``wss://`` for ``https://``)."""
    parts = urlsplit(api_url.rstrip("/"))
    scheme = {"https": "wss", "http": "ws"}.get(parts.scheme, parts.scheme)
    return urlunsplit((scheme, parts.netloc, parts.path + PRIVATE_WS_PATH, "", ""))


def private_orders_channel(account_id: str | int) -> str:
    """The channel a subscribe token is minted for (base form, base58 account)."""
    return f"private:spot:orders:{format_id(account_id)}"


def _backoff_delay(attempt: int) -> float:
    """0.5 s doubling to 10 s, jittered over the upper half of each step."""
    ceiling = min(RECONNECT_MAX_DELAY, RECONNECT_BASE_DELAY * 2 ** (min(attempt, 16) + 1))
    return ceiling / 2 + (secrets.randbelow(1_000_001) / 1_000_000) * (ceiling / 2)


def _is_terminal_token_error(exc: BaseException) -> bool:
    """A refused token stays refused; other failures (timeouts, 5xx) are retried."""
    return isinstance(exc, (PolyesterAuthError, PolyesterValidationError))


def _request_error_code(code: int) -> str:
    try:
        return pb.RequestError.Code.Name(code)
    except ValueError:
        return str(code)


@dataclass(eq=False)
class _Consumer:
    queue: asyncio.Queue[PrivateOrdersEvent | None]
    subscription: AsyncSubscription[PrivateOrdersEvent]
    ready: asyncio.Future[None]


@dataclass(eq=False)
class _Subscription:
    channel: str
    account: int
    consumers: list[_Consumer]
    # Server subscription ID; empty until Subscribed.
    sub: str = ""
    seq: int = 0
    # Last applied resume position, kept across resubscribes and reconnects.
    cursor: str = ""
    staged: list[OrderPb] | None = None
    # The live view as last applied, for consumers that join later.
    orders: dict[str, Order] | None = None
    # The last connection state consumers were told about.
    state: Literal["pending", "connected", "disconnected"] = "pending"
    stale: bool = False
    # The current server subscription reported Ready; reset on every new server subscription.
    ready: bool = False
    # Subscribe attempts since the subscription last delivered data; drives retry backoff.
    retries: int = 0
    retry_handle: asyncio.TimerHandle | None = None
    # The server confirmed this subscription at least once.
    confirmed: bool = False


@dataclass(frozen=True)
class _PendingRequest:
    kind: Literal["subscribe", "refresh"]
    subscription: _Subscription


@dataclass
class _Closed:
    code: int
    reason: str = ""


class PrivateOrderStream:
    """Account order streams over the private WebSocket."""

    def __init__(
        self,
        *,
        url: str,
        fetch_connect_token: Callable[[], Awaitable[str]],
        fetch_subscribe_token: Callable[[str], Awaitable[str]],
        max_queue_size: int = 1000,
    ) -> None:
        self._url = url
        self._fetch_connect_token = fetch_connect_token
        self._fetch_subscribe_token = fetch_subscribe_token
        self._max_queue_size = max_queue_size
        self._subs: dict[str, _Subscription] = {}
        self._pending: dict[str, _PendingRequest] = {}
        self._by_sub: dict[str, _Subscription] = {}
        # IDs of Unsubscribe requests awaiting their answer.
        self._unsubscribing: set[str] = set()
        self._ws: ClientConnection | None = None
        self._authenticated = False
        self._outbox: asyncio.Queue[bytes] | None = None
        self._run_task: asyncio.Task[None] | None = None
        self._tasks: set[asyncio.Task[Any]] = set()
        self._request_seq = 0
        self._closed = False

    @property
    def active_accounts(self) -> int:
        """Accounts with at least one consumer."""
        return len(self._subs)

    async def subscribe(self, account_id: str | int) -> AsyncSubscription[PrivateOrdersEvent]:
        """Stream one account's orders.

        Returns once the server confirmed the subscription; the first event is
        ``PrivateOrdersConnected``. A failure before that raises. Later
        failures the stream recovers from arrive as ``PrivateOrdersError``
        events; one that ends the stream is raised from iteration.
        """
        if self._closed:
            raise PolyesterRealtimeError("private order stream is closed")
        account = id_to_int(account_id, "account_id")
        channel = private_orders_channel(account)
        consumer = self._new_consumer()
        s = self._subs.get(channel)
        if s is not None:
            s.consumers.append(consumer)
            self._catch_up(s, consumer)
        else:
            s = _Subscription(channel=channel, account=account, consumers=[consumer])
            self._subs[channel] = s
            if self._ws is not None and self._authenticated:
                self._spawn(self._subscribe(self._ws, s))
            elif self._run_task is None:
                self._run_task = self._spawn(self._run())
        sub = s
        consumer.subscription._on_closed = lambda _closed: self._remove(sub, consumer)
        try:
            await consumer.ready
        except BaseException:
            self._remove(sub, consumer)
            raise
        return consumer.subscription

    async def aclose(self) -> None:
        """Close the connection and end every consumer's iteration."""
        self._closed = True
        for s in list(self._subs.values()):
            self._clear_retry(s)
            for consumer in list(s.consumers):
                self._end_consumer(consumer, None)
            s.consumers.clear()
        self._subs.clear()
        self._shutdown()
        for task in [task for task in self._tasks if task is not asyncio.current_task()]:
            with contextlib.suppress(asyncio.CancelledError, Exception):
                await asyncio.wait_for(task, timeout=2.0)

    # --- consumers ------------------------------------------------------

    def _new_consumer(self) -> _Consumer:
        queue: asyncio.Queue[PrivateOrdersEvent | None] = asyncio.Queue(
            maxsize=self._max_queue_size
        )
        subscription = AsyncSubscription[PrivateOrdersEvent](queue=queue, close=asyncio.Event())
        ready: asyncio.Future[None] = asyncio.get_running_loop().create_future()
        return _Consumer(queue=queue, subscription=subscription, ready=ready)

    def _catch_up(self, s: _Subscription, consumer: _Consumer) -> None:
        """Give a consumer that joined a running subscription what the others know."""
        if s.state == "connected":
            self._deliver_to(s, consumer, PrivateOrdersConnected())
        if s.orders is not None:
            self._deliver_to(s, consumer, PrivateOrdersSnapshot(orders=list(s.orders.values())))
        if s.ready:
            self._deliver_to(s, consumer, PrivateOrdersReady())
        if s.stale:
            self._deliver_to(s, consumer, PrivateOrdersStale(stale=True))

    def _deliver(self, s: _Subscription, event: PrivateOrdersEvent) -> None:
        for consumer in list(s.consumers):
            self._deliver_to(s, consumer, event)

    def _deliver_to(self, s: _Subscription, consumer: _Consumer, event: PrivateOrdersEvent) -> None:
        if consumer not in s.consumers:
            return
        try:
            consumer.queue.put_nowait(event)
        except asyncio.QueueFull:
            # Never drop an update silently: fail this consumer only.
            s.consumers.remove(consumer)
            self._end_consumer(
                consumer,
                PolyesterRealtimeOverflowError(
                    "private order stream queue full; consumer too slow"
                ),
            )
            if not s.consumers:
                self._teardown(s)
            return
        if isinstance(event, PrivateOrdersConnected) and not consumer.ready.done():
            consumer.ready.set_result(None)

    def _end_consumer(self, consumer: _Consumer, error: BaseException | None) -> None:
        subscription = consumer.subscription
        if error is not None:
            subscription._set_error(error)
            if not consumer.ready.done():
                consumer.ready.set_exception(error)
        elif not consumer.ready.done():
            consumer.ready.set_exception(PolyesterRealtimeError("private order stream closed"))
        subscription._close.set()
        with contextlib.suppress(asyncio.QueueFull):
            consumer.queue.put_nowait(None)

    def _remove(self, s: _Subscription, consumer: _Consumer) -> None:
        if consumer not in s.consumers:
            return
        s.consumers.remove(consumer)
        self._end_consumer(consumer, None)
        if not s.consumers:
            self._teardown(s)

    def _report(self, s: _Subscription, kind: str, error: Exception) -> None:
        self._deliver(s, PrivateOrdersError(kind=kind, error=error))
        for consumer in list(s.consumers):
            consumer.subscription._notify_error(error)

    def _report_all(self, kind: str, error: Exception) -> None:
        for s in list(self._subs.values()):
            self._report(s, kind, error)

    def _fail(self, s: _Subscription, kind: str, error: Exception, *, terminal: bool) -> None:
        """A subscription the server never confirmed fails fast, like every SDK subscribe."""
        if terminal or not s.confirmed:
            self._terminate(s, error)
        else:
            self._report(s, kind, error)

    def _fail_all(self, kind: str, error: Exception, *, terminal: bool) -> None:
        for s in list(self._subs.values()):
            self._fail(s, kind, error, terminal=terminal)

    def _terminate(self, s: _Subscription, error: BaseException) -> None:
        if self._subs.get(s.channel) is not s:
            return
        consumers = list(s.consumers)
        told_disconnected = s.state != "connected"
        s.state = "disconnected"
        s.consumers.clear()
        self._teardown(s)
        for consumer in consumers:
            if not told_disconnected:
                with contextlib.suppress(asyncio.QueueFull):
                    consumer.queue.put_nowait(PrivateOrdersDisconnected())
            self._end_consumer(consumer, error)

    def _terminate_all(self, error: BaseException) -> None:
        for s in list(self._subs.values()):
            self._terminate(s, error)

    # --- connection -----------------------------------------------------

    def _owns_connection(self) -> bool:
        """Whether the calling connection loop is still the stream's current one."""
        return bool(self._subs) and self._run_task is asyncio.current_task()

    async def _run(self) -> None:
        attempt = 0
        try:
            while self._owns_connection():
                try:
                    token = await self._fetch_connect_token()
                except asyncio.CancelledError:
                    raise
                except Exception as exc:
                    self._fail_all(
                        "connection_token", exc, terminal=_is_terminal_token_error(exc)
                    )
                    if not self._owns_connection():
                        return
                    await asyncio.sleep(_backoff_delay(attempt))
                    attempt += 1
                    continue
                if not self._owns_connection():
                    return
                try:
                    ws = await connect(
                        self._url,
                        subprotocols=[PRIVATE_WS_SUBPROTOCOL],
                        open_timeout=OPEN_TIMEOUT,
                        max_size=WS_MAX_MESSAGE_BYTES,
                        ping_interval=None,
                        close_timeout=1,
                    )
                except asyncio.CancelledError:
                    raise
                except Exception as exc:
                    error = PolyesterRealtimeError(f"private WebSocket connection failed: {exc}")
                    self._fail_all("connection", error, terminal=False)
                    if not self._owns_connection():
                        return
                    await asyncio.sleep(_backoff_delay(attempt))
                    attempt += 1
                    continue
                closed, stable = await self._serve(ws, token)
                if stable:
                    attempt = 0
                if not self._owns_connection():
                    return
                if closed.code in TERMINAL_CLOSE_CODES:
                    self._terminate_all(
                        PolyesterRealtimeError(
                            closed.reason or f"private WebSocket closed with code {closed.code}",
                            close_code=closed.code,
                        )
                    )
                    return
                # A close that reconnects is not an error.
                for s in list(self._subs.values()):
                    if not s.confirmed:
                        self._terminate(
                            s,
                            PolyesterRealtimeError(
                                f"private WebSocket closed with code {closed.code} "
                                "before the subscription was confirmed",
                                close_code=closed.code,
                            ),
                        )
                    elif s.state == "connected":
                        s.state = "disconnected"
                        self._deliver(s, PrivateOrdersDisconnected())
                if not self._owns_connection():
                    return
                await asyncio.sleep(_backoff_delay(attempt))
                attempt += 1
        finally:
            if self._run_task is asyncio.current_task():
                self._run_task = None

    async def _serve(self, ws: ClientConnection, token: str) -> tuple[_Closed, bool]:
        """Authenticate, subscribe every account, and read until the socket closes."""
        outbox: asyncio.Queue[bytes] = asyncio.Queue()
        self._ws = ws
        self._outbox = outbox
        writer = asyncio.create_task(self._write(ws, outbox))
        closed = _Closed(code=1000)
        auth_at = time.monotonic()
        try:
            self._send(ws, pb.ClientMessage(auth=pb.Auth(token=token)))
            self._authenticated = True
            for s in list(self._subs.values()):
                self._spawn(self._subscribe(ws, s))
            while self._ws is ws:
                try:
                    raw = await asyncio.wait_for(ws.recv(), timeout=HEARTBEAT_TIMEOUT)
                except TimeoutError:
                    closed = _Closed(HEARTBEAT_TIMEOUT_CLOSE_CODE, "heartbeat timeout")
                    break
                except ConnectionClosed as exc:
                    frame = exc.rcvd
                    closed = _Closed(frame.code, frame.reason) if frame else _Closed(1006)
                    break
                self._on_frame(ws, raw)
        finally:
            writer.cancel()
            if self._ws is ws:
                self._detach()
            if closed.code == HEARTBEAT_TIMEOUT_CLOSE_CODE:
                self._spawn(ws.close(closed.code, closed.reason))
            else:
                self._spawn(ws.close(1000))
        return closed, time.monotonic() - auth_at >= STABLE_CONNECTION

    async def _write(self, ws: ClientConnection, outbox: asyncio.Queue[bytes]) -> None:
        with contextlib.suppress(ConnectionClosed):
            while True:
                await ws.send(await outbox.get())

    def _send(self, ws: ClientConnection, message: pb.ClientMessage) -> None:
        if self._ws is ws and self._outbox is not None:
            self._outbox.put_nowait(message.SerializeToString())

    def _detach(self) -> None:
        self._ws = None
        self._outbox = None
        self._authenticated = False
        self._pending.clear()
        self._by_sub.clear()
        self._unsubscribing.clear()
        for s in self._subs.values():
            self._clear_retry(s)
            s.sub = ""
            s.seq = 0
            s.staged = None
            s.ready = False

    def _shutdown(self) -> None:
        ws = self._ws
        self._detach()
        current = asyncio.current_task()
        # A loop that is not cancelled here (it called this) sees it no longer owns the stream.
        self._run_task = None
        for task in list(self._tasks):
            if task is not current:
                task.cancel()
        if ws is not None:
            self._spawn(ws.close(1000))

    def _spawn(self, coro: Coroutine[Any, Any, Any]) -> asyncio.Task[Any]:
        task = asyncio.create_task(coro)
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)
        return task

    def _next_request_id(self) -> str:
        self._request_seq += 1
        return str(self._request_seq)

    # --- subscriptions --------------------------------------------------

    def _is_current(self, s: _Subscription) -> bool:
        return self._subs.get(s.channel) is s

    async def _subscribe(self, ws: ClientConnection, s: _Subscription) -> None:
        if not self._is_current(s):
            return
        request_id = self._next_request_id()
        request = _PendingRequest("subscribe", s)
        self._pending[request_id] = request
        try:
            token = await self._fetch_subscribe_token(s.channel)
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            if self._pending.get(request_id) is not request:
                return
            del self._pending[request_id]
            self._fail(s, "subscription_token", exc, terminal=_is_terminal_token_error(exc))
            if self._is_current(s):
                self._retry_subscribe(ws, s)
            return
        if self._ws is not ws or self._pending.get(request_id) is not request:
            return
        self._send(
            ws,
            pb.ClientMessage(
                subscribe=pb.Subscribe(
                    id=request_id,
                    channel=pb.ORDERS,
                    account=s.account,
                    token=token,
                    cursor=s.cursor,
                )
            ),
        )

    def _retry_subscribe(self, ws: ClientConnection, s: _Subscription) -> None:
        """Subscribe again after a backoff that grows until the subscription delivers data."""
        self._clear_retry(s)

        def retry() -> None:
            s.retry_handle = None
            if self._ws is ws and self._is_current(s) and not s.sub:
                self._spawn(self._subscribe(ws, s))

        s.retry_handle = asyncio.get_running_loop().call_later(_backoff_delay(s.retries), retry)
        s.retries += 1

    def _clear_retry(self, s: _Subscription) -> None:
        if s.retry_handle is not None:
            s.retry_handle.cancel()
        s.retry_handle = None

    async def _refresh(self, ws: ClientConnection, s: _Subscription) -> None:
        sub = s.sub
        try:
            token = await self._fetch_subscribe_token(s.channel)
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            # An unrefreshed subscription ends with TOKEN_EXPIRED and resubscribes.
            if self._ws is ws and s.sub == sub:
                self._report(s, "subscription_token", exc)
            return
        if self._ws is not ws or s.sub != sub:
            return
        request_id = self._next_request_id()
        self._pending[request_id] = _PendingRequest("refresh", s)
        self._send(
            ws,
            pb.ClientMessage(
                subscribe_refresh=pb.SubscribeRefresh(id=request_id, sub=sub, token=token)
            ),
        )

    async def _reauthenticate(self, ws: ClientConnection) -> None:
        try:
            token = await self._fetch_connect_token()
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            if self._ws is not ws:
                return
            if _is_terminal_token_error(exc):
                self._terminate_all(exc)
            else:
                self._report_all("connection_token", exc)
            return
        self._send(ws, pb.ClientMessage(auth=pb.Auth(token=token)))

    def _resubscribe(self, ws: ClientConnection, s: _Subscription) -> None:
        """Drop the server subscription and subscribe again from the last applied cursor:
        at once the first time, then with backoff until the subscription delivers data."""
        if s.sub:
            self._by_sub.pop(s.sub, None)
            self._unsubscribe(ws, s.sub)
        s.sub = ""
        s.seq = 0
        s.staged = None
        s.ready = False
        if s.retries > 0:
            self._retry_subscribe(ws, s)
        else:
            s.retries = 1
            self._spawn(self._subscribe(ws, s))
        # Consumers see the gap as a disconnect and the replacement's Subscribed as a reconnect.
        if s.state == "connected":
            s.state = "disconnected"
            self._deliver(s, PrivateOrdersDisconnected())

    def _unsubscribe(self, ws: ClientConnection, sub: str) -> None:
        request_id = self._next_request_id()
        self._unsubscribing.add(request_id)
        self._send(ws, pb.ClientMessage(unsubscribe=pb.Unsubscribe(id=request_id, sub=sub)))

    def _teardown(self, s: _Subscription) -> None:
        if not self._is_current(s):
            return
        del self._subs[s.channel]
        self._clear_retry(s)
        ws = self._ws
        if ws is not None and s.sub:
            self._by_sub.pop(s.sub, None)
            self._unsubscribe(ws, s.sub)
        s.sub = ""
        for request_id, request in list(self._pending.items()):
            if request.subscription is s:
                del self._pending[request_id]
        if not self._subs:
            self._shutdown()

    # --- frames ---------------------------------------------------------

    def _on_frame(self, ws: ClientConnection, raw: str | bytes) -> None:
        if not isinstance(raw, bytes):
            self._report_all(
                "decode", PolyesterRealtimeError("expected a binary private WebSocket frame")
            )
            return
        msg = pb.ServerMessage()
        try:
            msg.ParseFromString(raw)
        except Exception as exc:
            # Its seq is lost too, so the next frame resubscribes on the gap.
            self._report_all(
                "decode", PolyesterRealtimeError(f"invalid private WebSocket frame: {exc}")
            )
            return
        kind = msg.WhichOneof("frame")

        if kind == "subscribed":
            self._on_subscribed(ws, msg)
            return
        if kind == "subscribe_refreshed":
            self._pending.pop(msg.subscribe_refreshed.id, None)
            return
        if kind == "unsubscribed" and msg.unsubscribed.id in self._unsubscribing:
            self._unsubscribing.discard(msg.unsubscribed.id)
            return
        if kind == "error":
            self._on_request_error(ws, msg.sub, msg.error)
            return
        if kind == "token_expiring":
            self._spawn(self._reauthenticate(ws))
            return

        s = self._by_sub.get(msg.sub)
        if s is None:
            return
        if msg.seq > 0:
            if msg.seq != s.seq + 1:
                self._resubscribe(ws, s)
                return
            s.seq = msg.seq

        if kind == "snapshot_begin":
            s.staged = []
        elif kind == "snapshot_page":
            if s.staged is not None:
                s.staged.extend(msg.snapshot_page.orders)
        elif kind == "snapshot_end":
            self._on_snapshot_end(ws, s, msg.snapshot_end)
        elif kind == "unit":
            self._on_unit(ws, s, msg.unit)
        elif kind == "covered":
            s.cursor = msg.covered.cursor
            s.retries = 0
        elif kind == "ready":
            # A resumed subscription on a quiet account delivers no data, only this.
            s.retries = 0
            if not s.ready:
                s.ready = True
                self._deliver(s, PrivateOrdersReady())
        elif kind in ("unavailable", "available"):
            s.stale = kind == "unavailable"
            self._deliver(s, PrivateOrdersStale(stale=s.stale))
        elif kind == "subscribe_expiring":
            self._spawn(self._refresh(ws, s))
        elif kind == "unsubscribed":
            # The server ended it: its token expired, or for a reason this client does not know.
            self._by_sub.pop(s.sub, None)
            s.sub = ""
            self._resubscribe(ws, s)
        # resync_required: the next snapshot replaces the state. A frame kind this
        # SDK does not know is skipped; its seq was counted above.

    def _on_subscribed(self, ws: ClientConnection, msg: pb.ServerMessage) -> None:
        request = self._pending.get(msg.subscribed.id)
        if request is None or request.kind != "subscribe":
            # Its consumers left before the server confirmed it.
            if msg.sub:
                self._unsubscribe(ws, msg.sub)
            return
        del self._pending[msg.subscribed.id]
        s = request.subscription
        s.sub = msg.sub
        s.seq = 0
        s.ready = False
        s.confirmed = True
        self._by_sub[msg.sub] = s
        if s.state != "connected":
            s.state = "connected"
            self._deliver(s, PrivateOrdersConnected())
        # A new subscription reports Unavailable itself if its view is still behind.
        if s.stale:
            s.stale = False
            self._deliver(s, PrivateOrdersStale(stale=False))

    def _on_snapshot_end(
        self, ws: ClientConnection, s: _Subscription, end: pb.SnapshotEnd
    ) -> None:
        staged = s.staged
        s.staged = None
        if staged is None or len(staged) != end.count:
            s.cursor = ""
            self._resubscribe(ws, s)
            return
        try:
            orders = private_orders_from_proto(staged)
        except Exception as exc:
            self._report(s, "decode", exc)
            s.cursor = ""
            self._resubscribe(ws, s)
            return
        s.cursor = end.cursor
        s.retries = 0
        s.orders = {order.order_id: order for order in orders}
        self._deliver(s, PrivateOrdersSnapshot(orders=orders))

    def _on_unit(self, ws: ClientConnection, s: _Subscription, unit: pb.Unit) -> None:
        try:
            event = private_orders_unit_from_proto(unit)
        except Exception as exc:
            # The unit is not applied: resume from the cursor before it.
            self._report(s, "decode", exc)
            self._resubscribe(ws, s)
            return
        s.cursor = unit.next_cursor
        s.retries = 0
        if s.orders is not None:
            for order in event.orders:
                s.orders[order.order_id] = order
            for order_id in event.removed_order_ids:
                s.orders.pop(order_id, None)
        self._deliver(s, event)

    def _on_request_error(self, ws: ClientConnection, sub: str, error: pb.RequestError) -> None:
        if error.id and error.id in self._unsubscribing:
            self._unsubscribing.discard(error.id)
            return
        request = self._pending.get(error.id) if error.id else None
        # The answer to a request already answered, or whose subscription has since gone.
        if error.id and request is None:
            return
        if request is not None:
            del self._pending[error.id]
        s = request.subscription if request is not None else self._by_sub.get(sub)
        code = _request_error_code(error.code)
        realtime_error = PolyesterRealtimeError(
            error.message or f"private order stream request failed: {code}",
            code=code,
        )
        if s is None:
            self._report_all("request", realtime_error)
            return
        if request is not None and request.kind == "subscribe":
            if error.code == pb.RequestError.CURSOR_INVALID:
                s.cursor = ""
                self._spawn(self._subscribe(ws, s))
                return
            self._terminate(s, realtime_error)
            return
        if error.code == pb.RequestError.SUBSCRIPTION_UNKNOWN and s.sub == sub:
            self._by_sub.pop(s.sub, None)
            s.sub = ""
            self._resubscribe(ws, s)
            return
        self._report(s, request.kind if request is not None else "request", realtime_error)
