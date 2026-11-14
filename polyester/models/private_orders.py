"""Events delivered by the private order stream (``client.orders.subscribe``)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from polyester.errors import PolyesterRealtimeError
from polyester.models.trading import Order
from polyester.types.money import Price, Quantity


@dataclass(frozen=True, slots=True)
class PrivateOrderFill:
    """One execution of an order. ``match_id`` is the user trade's ``match_id``."""

    match_id: str
    ordinal: int
    role: str
    qty: Quantity
    price: Price | None


@dataclass(frozen=True, slots=True)
class PrivateOrderEvent:
    """A change to one order: ``accepted``, ``filled``, ``canceled``, ``rejected``,
    ``replaced`` or ``attached_risk``.

    ``reject_reason`` names a ``rejected`` order's refusal as the order write API
    does (for example ``POST_ONLY_CROSS``), the same value as the order's
    ``reject_reason``. ``cancel_reason`` names why a ``canceled`` order ended
    (for example ``USER_REQUEST``), and is ``REPLACED`` on the ``replaced`` event
    of the order a replace ended. Both are ``None`` otherwise, including on the
    ``replaced`` event that installs the successor.
    ``replacement_order_id`` is set for ``replaced``; ``fill`` for ``filled``.
    """

    order_id: str
    version: int
    kind: str
    reject_reason: str | None = None
    cancel_reason: str | None = None
    replacement_order_id: str = ""
    fill: PrivateOrderFill | None = None


@dataclass(frozen=True, slots=True)
class PrivateOrderCommandOutcome:
    """A command outcome that changed no order: ``amend_rejected``,
    ``cancel_rejected``, ``replace_rejected``, ``rejected`` or ``cancel_all_done``.

    ``reason`` is the order error code the Orders API returns for the same
    refusal (for example ``INSUFFICIENT_BALANCE``); empty when unset.
    """

    kind: str
    order_id: str = ""
    new_order_id: str = ""
    client_order_id: str = ""
    reason: str = ""


@dataclass(frozen=True, slots=True)
class PrivateOrdersSnapshot:
    """The account's full live view. Replace local state with ``orders``."""

    orders: list[Order]
    type: Literal["snapshot"] = "snapshot"


@dataclass(frozen=True, slots=True)
class PrivateOrdersUnit:
    """One change, applied whole.

    ``orders`` are complete changed orders: keep the copy with the higher
    ``version`` (equal versions are identical). ``removed_order_ids`` left the
    live view; a removal is not a cancellation. ``events`` are in order and
    never coalesced.
    """

    orders: list[Order]
    removed_order_ids: list[str]
    events: list[PrivateOrderEvent | PrivateOrderCommandOutcome]
    type: Literal["unit"] = "unit"


@dataclass(frozen=True, slots=True)
class PrivateOrdersStale:
    """The account's live view is temporarily behind (``True``) or caught up (``False``)."""

    stale: bool
    type: Literal["stale"] = "stale"


@dataclass(frozen=True, slots=True)
class PrivateOrdersReady:
    """The subscription reached the account's read boundary, sampled when the
    server received the subscribe.

    From here the stream reflects at least every acknowledgement given before
    the subscribe, including every order read made before it. Wait for it
    before relying on the stream: read, subscribe, wait for ready, then merge
    by ``version``. Delivered once per server subscription, so again after a
    resubscribe or reconnect.
    """

    type: Literal["ready"] = "ready"


@dataclass(frozen=True, slots=True)
class PrivateOrdersConnected:
    """The server confirmed the subscription; again after each reconnect or resubscribe."""

    type: Literal["connected"] = "connected"


@dataclass(frozen=True, slots=True)
class PrivateOrdersDisconnected:
    """The connection or subscription carrying the stream dropped.

    The stream resumes from its last position on its own unless it ends with
    an error.
    """

    type: Literal["disconnected"] = "disconnected"


@dataclass(frozen=True, slots=True)
class PrivateOrdersError:
    """A failure the stream recovers from by itself (it keeps running).

    ``kind`` names the step that failed: ``connection_token``,
    ``subscription_token``, ``connection``, ``decode``, ``request`` or
    ``refresh``. A failure that ends the stream is raised from iteration
    instead.
    """

    kind: str
    error: PolyesterRealtimeError | Exception = field(compare=False)
    type: Literal["error"] = "error"


PrivateOrdersEvent = (
    PrivateOrdersSnapshot
    | PrivateOrdersUnit
    | PrivateOrdersStale
    | PrivateOrdersReady
    | PrivateOrdersConnected
    | PrivateOrdersDisconnected
    | PrivateOrdersError
)

__all__ = [
    "PrivateOrderCommandOutcome",
    "PrivateOrderEvent",
    "PrivateOrderFill",
    "PrivateOrdersConnected",
    "PrivateOrdersDisconnected",
    "PrivateOrdersError",
    "PrivateOrdersEvent",
    "PrivateOrdersReady",
    "PrivateOrdersSnapshot",
    "PrivateOrdersStale",
    "PrivateOrdersUnit",
]
