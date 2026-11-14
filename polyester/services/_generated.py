from __future__ import annotations

from collections.abc import Callable
from typing import Any, TypeVar

from connectrpc.errors import ConnectError
from google.protobuf.message import Message

from polyester._wire import map_connect_error, protobuf_to_public_dict
from polyester.transport import TransportFactory

TRequest = TypeVar("TRequest", bound=Message)
TResponse = TypeVar("TResponse", bound=Message)
R = TypeVar("R")


async def unary_public_message(
    transport: TransportFactory,
    client_cls: type,
    call: Callable[..., Any],
    request: TRequest,
) -> TResponse:
    client = transport.create_public_client(client_cls)
    try:
        response: TResponse = await call(client, request)
        return response
    except ConnectError as exc:
        raise map_connect_error(exc) from exc


async def unary_auth_message(
    transport: TransportFactory,
    client_cls: type,
    call: Callable[..., Any],
    request: TRequest,
) -> TResponse:
    client = transport.create_auth_client(client_cls)
    try:
        response: TResponse = await call(client, request)
        return response
    except ConnectError as exc:
        raise map_connect_error(exc) from exc


async def unary_public(
    transport: TransportFactory,
    client_cls: type,
    call: Callable[..., Any],
    request: TRequest,
) -> dict[str, Any]:
    """Legacy dict bridge for services not yet on proto decoders."""
    response: Message = await unary_public_message(transport, client_cls, call, request)
    return protobuf_to_public_dict(response)


async def unary_auth(
    transport: TransportFactory,
    client_cls: type,
    call: Callable[..., Any],
    request: TRequest,
) -> dict[str, Any]:
    """Legacy dict bridge for services not yet on proto decoders."""
    response: Message = await unary_auth_message(transport, client_cls, call, request)
    return protobuf_to_public_dict(response)


async def unary_public_decoded(
    transport: TransportFactory,
    client_cls: type,
    call: Callable[..., Any],
    request: TRequest,
    decoder: Callable[[TResponse], R],
) -> R:
    response: TResponse = await unary_public_message(transport, client_cls, call, request)
    return decoder(response)


async def unary_auth_decoded(
    transport: TransportFactory,
    client_cls: type,
    call: Callable[..., Any],
    request: TRequest,
    decoder: Callable[[TResponse], R],
) -> R:
    response: TResponse = await unary_auth_message(transport, client_cls, call, request)
    return decoder(response)
