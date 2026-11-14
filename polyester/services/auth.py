from __future__ import annotations

from polyester.codecs.decode.auth import me_from_proto
from polyester.gen.auth.v1.auth_connect import AuthServiceClient
from polyester.gen.auth.v1.auth_pb2 import MeRequest
from polyester.models.auth import MeResult
from polyester.realtime.client import AsyncRealtimeClient
from polyester.services._base import BaseService
from polyester.services._generated import unary_auth_decoded
from polyester.services.profile import AsyncProfileService


class AsyncAuthService(BaseService):
    def __init__(self, transport, *, realtime: AsyncRealtimeClient | None = None) -> None:
        super().__init__(transport)
        self.profile = AsyncProfileService(transport, realtime=realtime)

    async def me(self) -> MeResult:
        return await unary_auth_decoded(
            self._transport,
            AuthServiceClient,
            lambda client, req: client.me(req),
            MeRequest(),
            me_from_proto,
        )
