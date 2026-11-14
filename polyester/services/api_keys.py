from __future__ import annotations

from polyester.auth import generate_ed25519_keypair
from polyester.codecs.decode.api_keys import (
    api_key_from_get_proto,
    api_keys_list_from_proto,
)
from polyester.codecs.orders import parse_optional_subaccount_id
from polyester.codecs.realtime_decode import decode_api_key_bytes
from polyester.gen.auth.v1.api_keys_connect import ApiKeyServiceClient
from polyester.gen.auth.v1.api_keys_pb2 import (
    GetApiKeyRequest,
    ListApiKeysRequest,
)
from polyester.models import ApiKeysList, ApiKeySummary
from polyester.models.auth import Ed25519Keypair
from polyester.realtime.client import AsyncRealtimeClient, AsyncSubscription
from polyester.services._base import BaseService
from polyester.services._generated import unary_auth_decoded
from polyester.services._realtime_subscribe import subscribe_account_proto
from polyester.services._scope import AccountScope, ScopedSubAccountMixin


class AsyncApiKeysService(ScopedSubAccountMixin, BaseService):
    def __init__(
        self,
        transport,
        default_sub_account_id: str | None,
        *,
        default_account_id: str | int | None = None,
        realtime: AsyncRealtimeClient | None = None,
    ) -> None:
        super().__init__(transport)
        self._default_sub_account_id = default_sub_account_id
        self._default_account_id = default_account_id
        self._realtime = realtime

    async def list(
        self,
        *,
        account: AccountScope | None = None,
        sub_account_id: str | None = None,
    ) -> ApiKeysList:
        request = ListApiKeysRequest()
        parsed_sub = parse_optional_subaccount_id(
            self._resolve_sub_account_id(sub_account_id, account=account)
        )
        if parsed_sub is not None:
            request.subaccount_id = parsed_sub
        return await unary_auth_decoded(
            self._transport,
            ApiKeyServiceClient,
            lambda client, req: client.list_api_keys(req),
            request,
            api_keys_list_from_proto,
        )

    async def get(self, *, key_id: str) -> ApiKeySummary | None:
        return await unary_auth_decoded(
            self._transport,
            ApiKeyServiceClient,
            lambda client, req: client.get_api_key(req),
            GetApiKeyRequest(key_id=key_id),
            api_key_from_get_proto,
        )

    def generate_keypair(self) -> Ed25519Keypair:
        """Generate a local Ed25519 keypair for API key creation (secret never sent to API)."""
        public_key, secret_key = generate_ed25519_keypair()
        return Ed25519Keypair(
            public_key_hex=public_key.hex(),
            public_key=public_key,
            secret_key_hex=secret_key.hex(),
            secret_key=secret_key,
        )

    async def subscribe(
        self,
        *,
        account_id: str | int | None = None,
    ) -> AsyncSubscription[ApiKeySummary]:
        return await subscribe_account_proto(
            self._realtime,
            channel_template="private:auth:api-keys:{account_id}:proto",
            account_id=account_id,
            default_account_id=self._default_account_id,
            decode=decode_api_key_bytes,
        )
