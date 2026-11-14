from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import TypeVar

from polyester.errors import PolyesterRealtimeError
from polyester.realtime.client import AsyncRealtimeClient, AsyncSubscription
from polyester.services._scope import resolve_account_id

T = TypeVar("T")


def require_realtime(realtime: AsyncRealtimeClient | None) -> AsyncRealtimeClient:
    if realtime is None:
        raise PolyesterRealtimeError("Realtime client is not configured on this Polyester instance")
    return realtime


async def subscribe_account_proto(
    realtime: AsyncRealtimeClient | None,
    *,
    channel_template: str,
    account_id: str | int | None,
    default_account_id: str | int | None,
    decode: Callable[[bytes], T],
) -> AsyncSubscription[T]:
    client = require_realtime(realtime)
    resolved = resolve_account_id(account_id, default_account_id)
    channel = channel_template.format(account_id=resolved)
    return await client.subscribe_proto(channel, decode=decode)


async def subscribe_account_proto_batch(
    realtime: AsyncRealtimeClient | None,
    *,
    channel_template: str,
    account_id: str | int | None,
    default_account_id: str | int | None,
    decode_batch: Callable[[bytes], Sequence[T | BaseException]],
) -> AsyncSubscription[T]:
    client = require_realtime(realtime)
    resolved = resolve_account_id(account_id, default_account_id)
    channel = channel_template.format(account_id=resolved)
    return await client.subscribe_proto_batch(channel, decode_batch=decode_batch)


async def subscribe_public_proto(
    realtime: AsyncRealtimeClient | None,
    *,
    channel: str,
    decode: Callable[[bytes], T],
) -> AsyncSubscription[T]:
    client = require_realtime(realtime)
    return await client.subscribe_proto(channel, decode=decode)
