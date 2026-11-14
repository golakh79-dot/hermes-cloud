from __future__ import annotations

from polyester.codecs.realtime_decode import (
    decode_api_policy_bytes,
    decode_subaccount_policy_bytes,
)
from polyester.models.policies import ApiPolicy, SubaccountPolicy
from polyester.realtime.client import AsyncRealtimeClient, AsyncSubscription
from polyester.services._base import BaseService
from polyester.services._realtime_subscribe import subscribe_account_proto


class AsyncPoliciesService(BaseService):
    """Realtime policy subscriptions (unary policy admin RPCs require session JWT)."""

    def __init__(
        self,
        transport,
        *,
        default_account_id: str | int | None = None,
        realtime: AsyncRealtimeClient | None = None,
    ) -> None:
        super().__init__(transport)
        self._default_account_id = default_account_id
        self._realtime = realtime

    async def subscribe_subaccount_policies(
        self,
        *,
        account_id: str | int | None = None,
    ) -> AsyncSubscription[SubaccountPolicy]:
        return await subscribe_account_proto(
            self._realtime,
            channel_template="private:auth:subaccount-policies:{account_id}:proto",
            account_id=account_id,
            default_account_id=self._default_account_id,
            decode=decode_subaccount_policy_bytes,
        )

    async def subscribe_api_policies(
        self,
        *,
        account_id: str | int | None = None,
    ) -> AsyncSubscription[ApiPolicy]:
        return await subscribe_account_proto(
            self._realtime,
            channel_template="private:auth:api-policies:{account_id}:proto",
            account_id=account_id,
            default_account_id=self._default_account_id,
            decode=decode_api_policy_bytes,
        )
