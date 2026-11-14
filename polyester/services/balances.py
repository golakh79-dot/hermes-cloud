from __future__ import annotations

import builtins

from polyester.catalogs import CatalogManager
from polyester.codecs.decode.balances import (
    balance_history_from_proto,
    balances_list_from_proto,
    equity_history_from_proto,
    holds_list_from_proto,
)
from polyester.codecs.ledger import resolve_balance_range, resolve_equity_group_by
from polyester.codecs.orders import parse_optional_subaccount_id
from polyester.codecs.realtime_decode import decode_asset_balance_bytes
from polyester.gen.ledger.read.v1.ledger_read_connect import LedgerReadServiceClient
from polyester.gen.ledger.read.v1.ledger_read_pb2 import (
    GetBalanceHistoryRequest,
    GetBalancesRequest,
    GetEquityHistorySeriesRequest,
    ListHoldsRequest,
)
from polyester.models import (
    AssetBalance,
    BalanceHistory,
    BalancesList,
    EquityHistory,
    HoldsList,
)
from polyester.realtime.client import AsyncRealtimeClient, AsyncSubscription
from polyester.services._base import BaseService
from polyester.services._generated import unary_auth_decoded
from polyester.services._realtime_subscribe import subscribe_account_proto
from polyester.services._scope import AccountScope, ScopedSubAccountMixin
from polyester.services._validation import validate_limit


class AsyncBalancesService(ScopedSubAccountMixin, BaseService):
    def __init__(
        self,
        transport,
        catalogs: CatalogManager | None = None,
        default_sub_account_id: str | None = None,
        default_account_id: str | int | None = None,
        *,
        realtime: AsyncRealtimeClient | None = None,
    ) -> None:
        super().__init__(transport)
        self._catalogs = catalogs or CatalogManager()
        self._default_sub_account_id = default_sub_account_id
        self._default_account_id = default_account_id
        self._realtime = realtime

    async def list(
        self,
        *,
        account: AccountScope | None = None,
        sub_account_id: str | int | None = None,
    ) -> BalancesList:
        request = GetBalancesRequest()
        resolved = parse_optional_subaccount_id(
            self._resolve_sub_account_id(sub_account_id, account=account)
        )
        if resolved is not None:
            request.subaccount_id = resolved
        return await unary_auth_decoded(
            self._transport,
            LedgerReadServiceClient,
            lambda client, req: client.get_balances(req),
            request,
            balances_list_from_proto,
        )

    async def get_balance_history(
        self,
        *,
        account: AccountScope | None = None,
        range: str = "7d",
        sub_account_id: str | None = None,
        ledger: int = 0,
        account_codes: builtins.list[int] | None = None,
    ) -> BalanceHistory:
        request = GetBalanceHistoryRequest(
            range=resolve_balance_range(range),
            ledger=ledger,
        )
        parsed_sub = parse_optional_subaccount_id(
            self._resolve_sub_account_id(sub_account_id, account=account)
        )
        if parsed_sub is not None:
            request.subaccount_id = parsed_sub
        if account_codes:
            request.account_codes.extend(account_codes)
        return await unary_auth_decoded(
            self._transport,
            LedgerReadServiceClient,
            lambda client, req: client.get_balance_history(req),
            request,
            balance_history_from_proto,
        )

    async def get_equity_history(
        self,
        *,
        account: AccountScope | None = None,
        range: str = "7d",
        sub_account_id: str | None = None,
        account_codes: builtins.list[int] | None = None,
        group_by: str = "account",
    ) -> EquityHistory:
        request = GetEquityHistorySeriesRequest(
            range=resolve_balance_range(range),
            group_by=resolve_equity_group_by(group_by),
        )
        parsed_sub = parse_optional_subaccount_id(
            self._resolve_sub_account_id(sub_account_id, account=account)
        )
        if parsed_sub is not None:
            request.subaccount_id = parsed_sub
        if account_codes:
            request.account_codes.extend(account_codes)
        return await unary_auth_decoded(
            self._transport,
            LedgerReadServiceClient,
            lambda client, req: client.get_equity_history_series(req),
            request,
            equity_history_from_proto,
        )

    async def list_holds(
        self,
        *,
        account: AccountScope | None = None,
        sub_account_id: str | None = None,
        limit: int = 50,
        reversed: bool = False,
    ) -> HoldsList:
        request = ListHoldsRequest(limit=validate_limit(limit), reversed=reversed)
        parsed_sub = parse_optional_subaccount_id(
            self._resolve_sub_account_id(sub_account_id, account=account)
        )
        if parsed_sub is not None:
            request.subaccount_id = parsed_sub
        return await unary_auth_decoded(
            self._transport,
            LedgerReadServiceClient,
            lambda client, req: client.list_holds(req),
            request,
            holds_list_from_proto,
        )

    async def subscribe(
        self,
        *,
        account_id: str | int | None = None,
    ) -> AsyncSubscription[AssetBalance]:
        return await subscribe_account_proto(
            self._realtime,
            channel_template="private:ledger:balances:{account_id}:proto",
            account_id=account_id,
            default_account_id=self._default_account_id,
            decode=decode_asset_balance_bytes,
        )
