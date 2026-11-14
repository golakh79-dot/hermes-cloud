from __future__ import annotations

from polyester.catalogs import CatalogManager
from polyester.codecs.decode.orders import user_trades_list_from_proto
from polyester.codecs.orders import parse_optional_subaccount_id
from polyester.codecs.realtime_decode import decode_user_trade_batch_bytes
from polyester.codecs.scalars import UINT64_MAX, id_to_int
from polyester.errors import PolyesterValidationError
from polyester.gen.orders.v1.orders_read_connect import OrdersReadServiceClient
from polyester.gen.orders.v1.orders_read_pb2 import GetUserTradesRequest
from polyester.models import UserTrade, UserTradesList
from polyester.realtime.client import AsyncRealtimeClient, AsyncSubscription
from polyester.services._base import BaseService
from polyester.services._generated import unary_auth_decoded
from polyester.services._realtime_subscribe import subscribe_account_proto_batch
from polyester.services._scope import AccountScope, ScopedSubAccountMixin
from polyester.services._symbols import resolve_symbol_id
from polyester.services._validation import validate_limit


class AsyncTradesService(ScopedSubAccountMixin, BaseService):
    def __init__(
        self,
        transport,
        catalogs: CatalogManager,
        default_sub_account_id: str | None,
        *,
        default_account_id: str | int | None = None,
        realtime: AsyncRealtimeClient | None = None,
    ) -> None:
        super().__init__(transport)
        self._catalogs = catalogs
        self._default_sub_account_id = default_sub_account_id
        self._default_account_id = default_account_id
        self._realtime = realtime

    async def list(
        self,
        *,
        account: AccountScope | None = None,
        sub_account_id: str | None = None,
        symbol: str | None = None,
        symbol_id: int | None = None,
        after_match_id: int | None = None,
        order_id: str | int | None = None,
        lineage_id: str | int | None = None,
        through_generation: int | None = None,
        include_transfers: bool = False,
        limit: int = 100,
        page_token: str | None = None,
    ) -> UserTradesList:
        """List user fills, optionally scoped to one physical order or lineage.

        ``order_id`` and ``lineage_id`` are mutually exclusive. Use
        ``order_id`` for one physical order or ``lineage_id`` for executions
        across accepted replacements. ``through_generation`` is an inclusive
        ceiling and requires ``lineage_id``. Set ``include_transfers`` to
        receive settlement legs; identify a match by ``(symbol_id, match_id)``
        and deduplicate repeated legs across pages by ``tx_id``.
        """
        if order_id is not None and lineage_id is not None:
            raise PolyesterValidationError(
                "trades.list order_id and lineage_id are mutually exclusive"
            )
        if through_generation is not None and lineage_id is None:
            raise PolyesterValidationError(
                "trades.list through_generation requires lineage_id"
            )
        if through_generation is not None:
            if isinstance(through_generation, bool) or not isinstance(through_generation, int):
                raise PolyesterValidationError(
                    "trades.list through_generation must be a positive integer"
                )
            if through_generation <= 0:
                raise PolyesterValidationError(
                    "trades.list through_generation must be a positive integer"
                )
        validated_limit = validate_limit(limit)
        request = GetUserTradesRequest(limit=validated_limit)
        if order_id is not None:
            request.order_id = id_to_int(order_id, "order_id")
        if lineage_id is not None:
            request.lineage_id = id_to_int(lineage_id, "lineage_id")
        if through_generation is not None:
            request.through_generation = through_generation
        if include_transfers:
            request.include_transfers = True
        if after_match_id is not None:
            if not 0 < int(after_match_id) <= UINT64_MAX:
                raise PolyesterValidationError(
                    "trades.list after_match_id must be a positive uint64 match id"
                )
            request.symbol_id = resolve_symbol_id(
                self._catalogs,
                symbol=symbol,
                symbol_id=symbol_id,
                label="trades.list",
            )
            request.after_match_id = int(after_match_id)
        elif symbol is not None or symbol_id is not None:
            request.symbol_id = resolve_symbol_id(
                self._catalogs,
                symbol=symbol,
                symbol_id=symbol_id,
                label="trades.list",
            )
        parsed_sub = parse_optional_subaccount_id(
            self._resolve_sub_account_id(sub_account_id, account=account)
        )
        if parsed_sub is not None:
            request.subaccount_id = parsed_sub
        if page_token:
            request.page_token = page_token
        return await unary_auth_decoded(
            self._transport,
            OrdersReadServiceClient,
            lambda client, req: client.get_user_trades(req),
            request,
            user_trades_list_from_proto,
        )

    async def subscribe(
        self,
        *,
        account_id: str | int | None = None,
    ) -> AsyncSubscription[UserTrade]:
        return await subscribe_account_proto_batch(
            self._realtime,
            channel_template="private:spot:trades:{account_id}:proto",
            account_id=account_id,
            default_account_id=self._default_account_id,
            decode_batch=decode_user_trade_batch_bytes,
        )
