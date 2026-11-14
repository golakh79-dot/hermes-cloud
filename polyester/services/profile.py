from __future__ import annotations

from polyester.codecs.realtime_decode import decode_account_identity_bytes
from polyester.models.auth import AccountIdentity
from polyester.realtime.client import AsyncRealtimeClient, AsyncSubscription
from polyester.services._base import BaseService
from polyester.services._realtime_subscribe import subscribe_public_proto


class AsyncProfileService(BaseService):
    """Public identity realtime (profile CRUD RPCs require session JWT)."""

    def __init__(self, transport, *, realtime: AsyncRealtimeClient | None = None) -> None:
        super().__init__(transport)
        self._realtime = realtime

    async def subscribe_identity(self) -> AsyncSubscription[AccountIdentity]:
        return await subscribe_public_proto(
            self._realtime,
            channel="public:identity:updates:proto",
            decode=decode_account_identity_bytes,
        )
