from __future__ import annotations

from collections.abc import Awaitable, Callable

from connectrpc.codec import Codec
from connectrpc.interceptor import UnaryInterceptor
from connectrpc.request import RequestContext
from google.protobuf.message import Message

from polyester.auth import ApiKeyCredentials, sign_request_async
from polyester.user_agent import USER_AGENT, USER_AGENT_HEADER


class UserAgentUnaryInterceptor(UnaryInterceptor):
    """Attach the Polyester SDK User-Agent on every Connect unary call."""

    async def intercept_unary(
        self,
        call_next: Callable[[Message, RequestContext], Awaitable[Message]],
        request: Message,
        ctx: RequestContext,
    ) -> Message:
        ctx.request_headers()[USER_AGENT_HEADER] = USER_AGENT
        return await call_next(request, ctx)


class ApiKeyAuthUnaryInterceptor(UnaryInterceptor):
    """Attach Polyester API-key headers to generated Connect unary calls."""

    def __init__(
        self,
        credentials: ApiKeyCredentials,
        *,
        base_url: str,
        codec: Codec,
    ) -> None:
        self._credentials = credentials
        self._base_url = base_url.rstrip("/")
        self._codec = codec

    async def intercept_unary(
        self,
        call_next: Callable[[Message, RequestContext], Awaitable[Message]],
        request: Message,
        ctx: RequestContext,
    ) -> Message:
        info = ctx.method()
        url = f"{self._base_url}/{info.service_name}/{info.name}"
        body = self._codec.encode(request)
        headers = await sign_request_async(
            self._credentials,
            method=ctx.http_method(),
            url=url,
            body=body,
        )
        ctx.request_headers().update(headers)
        return await call_next(request, ctx)
