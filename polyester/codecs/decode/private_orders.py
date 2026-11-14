"""Decoders for the private WebSocket order stream (``privatews.v1``)."""

from __future__ import annotations

from collections.abc import Iterable

from polyester.codecs.decode.orders import (
    _error_code_label,
    cancel_reason_label,
    order_from_proto,
)
from polyester.codecs.proto_helpers import format_uint64_id, proto_enum_name
from polyester.gen.orders.v1.orders_read_pb2 import Order as OrderPb
from polyester.gen.privatews.v1 import private_ws_pb2
from polyester.models.private_orders import (
    PrivateOrderCommandOutcome,
    PrivateOrderEvent,
    PrivateOrderFill,
    PrivateOrdersUnit,
)
from polyester.models.trading import Order
from polyester.types.money import Price, Quantity


def private_orders_from_proto(orders: Iterable[OrderPb]) -> list[Order]:
    """Decode stream orders with the same decoder as the order reads."""
    return [order_from_proto(item) for item in orders]


def _fill_from_proto(msg: private_ws_pb2.Fill) -> PrivateOrderFill:
    return PrivateOrderFill(
        match_id=str(msg.match_id),
        ordinal=int(msg.ordinal),
        role=proto_enum_name(private_ws_pb2.Fill.Role, msg.role),
        qty=Quantity.from_scaled(int(msg.qty_scaled)),
        price=Price.from_ticks(int(msg.price_ticks)) if msg.price_ticks else None,
    )


def _order_event_from_proto(msg: private_ws_pb2.OrderEvent) -> PrivateOrderEvent:
    return PrivateOrderEvent(
        order_id=format_uint64_id(msg.order_id),
        version=int(msg.version),
        kind=proto_enum_name(private_ws_pb2.OrderEvent.Kind, msg.kind),
        reject_reason=_error_code_label(int(msg.reject_reason)) if msg.reject_reason else None,
        cancel_reason=cancel_reason_label(int(msg.cancel_reason)) if msg.cancel_reason else None,
        replacement_order_id=(
            format_uint64_id(msg.replacement_order_id) if msg.replacement_order_id else ""
        ),
        fill=_fill_from_proto(msg.fill) if msg.HasField("fill") else None,
    )


def _command_outcome_from_proto(msg: private_ws_pb2.CommandOutcome) -> PrivateOrderCommandOutcome:
    return PrivateOrderCommandOutcome(
        kind=proto_enum_name(private_ws_pb2.CommandOutcome.Kind, msg.kind),
        order_id=format_uint64_id(msg.order_id) if msg.order_id else "",
        new_order_id=format_uint64_id(msg.new_order_id) if msg.new_order_id else "",
        client_order_id=msg.client_order_id,
        reason=_error_code_label(int(msg.reason)) if msg.reason else "",
    )


def private_orders_unit_from_proto(msg: private_ws_pb2.Unit) -> PrivateOrdersUnit:
    events: list[PrivateOrderEvent | PrivateOrderCommandOutcome] = []
    for event in msg.events:
        kind = event.WhichOneof("kind")
        if kind == "order":
            events.append(_order_event_from_proto(event.order))
        elif kind == "outcome":
            events.append(_command_outcome_from_proto(event.outcome))
        # An event kind this SDK does not know is skipped (forward compatibility).
    return PrivateOrdersUnit(
        orders=private_orders_from_proto(msg.orders),
        removed_order_ids=[format_uint64_id(order_id) for order_id in msg.removed_order_ids],
        events=events,
    )
