from __future__ import annotations

from polyester.codecs.decode.trading_rate_limits import (
    rate_limit_config_from_proto,
    trading_rate_limits_from_proto,
)
from polyester.codecs.orders import parse_optional_subaccount_id
from polyester.gen.ratelimit.v1.ratelimit_connect import RateLimitServiceClient
from polyester.gen.ratelimit.v1.ratelimit_pb2 import (
    GetRateLimitConfigRequest,
    GetTradingRateLimitsRequest,
)
from polyester.models.trading_rate_limits import RateLimitConfig, TradingRateLimits
from polyester.services._base import BaseService
from polyester.services._generated import unary_auth_decoded, unary_public_decoded
from polyester.services._scope import AccountScope, ScopedSubAccountMixin


class AsyncRateLimitService(ScopedSubAccountMixin, BaseService):
    def __init__(self, transport, default_sub_account_id: str | None) -> None:
        super().__init__(transport)
        self._default_sub_account_id = default_sub_account_id

    async def get_rate_limit_config(self) -> RateLimitConfig:
        return await unary_public_decoded(
            self._transport,
            RateLimitServiceClient,
            lambda client, request: client.get_rate_limit_config(request),
            GetRateLimitConfigRequest(),
            rate_limit_config_from_proto,
        )

    async def get_trading_rate_limits(
        self,
        *,
        account: AccountScope | None = None,
        sub_account_id: str | None = None,
    ) -> TradingRateLimits:
        request = GetTradingRateLimitsRequest()
        parsed_sub = parse_optional_subaccount_id(
            self._resolve_sub_account_id(sub_account_id, account=account)
        )
        if parsed_sub is not None:
            request.subaccount_id = parsed_sub
        return await unary_auth_decoded(
            self._transport,
            RateLimitServiceClient,
            lambda client, req: client.get_trading_rate_limits(req),
            request,
            trading_rate_limits_from_proto,
        )
