"""Typed exclusive order identity (order id XOR client order id)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class OrderId:
    """Exchange-assigned order id."""

    value: str | int


@dataclass(frozen=True, slots=True)
class ClientOrderId:
    """Caller-supplied client order id."""

    value: str


OrderKey = OrderId | ClientOrderId

__all__ = ["ClientOrderId", "OrderId", "OrderKey"]
