from __future__ import annotations

import asyncio
import time
from collections.abc import Awaitable, Callable
from typing import Any

import msgspec

from polyester.catalogs import CatalogManager
from polyester.codecs.decode.orders import (
    batch_cancel_from_proto,
    batch_create_from_proto,
    batch_replace_from_proto,
    batch_replace_status_from_proto,
    cancel_all_after_from_proto,
    cancel_all_from_proto,
    get_order_from_proto,
    modify_order_from_proto,
    order_mutation_from_proto,
    orders_list_from_proto,
    preview_order_from_proto,
)
from polyester.codecs.orders import (
    batch_cancel_orders_to_proto,
    batch_create_orders_to_proto,
    batch_replace_orders_to_proto,
    cancel_all_after_to_proto,
    cancel_all_orders_to_proto,
    create_order_to_proto,
    modify_order_to_proto,
    normalize_create_order_request,
    parse_optional_subaccount_id,
    preview_order_to_proto,
    resolve_quantity_scale,
    resolve_quote_quantity_scale,
    set_order_key,
)
from polyester.codecs.scalars import id_to_int
from polyester.errors import PolyesterTransportError, PolyesterValidationError
from polyester.gen.orders.v1.orders_connect import OrdersServiceClient
from polyester.gen.orders.v1.orders_pb2 import CancelOrderRequest
from polyester.gen.orders.v1.orders_read_connect import OrdersReadServiceClient
from polyester.gen.orders.v1.orders_read_pb2 import (
    GetBatchReplaceStatusRequest,
    GetOpenOrdersRequest,
    GetOrderHistoryRequest,
    GetOrderRequest,
)
from polyester.models import (
    AttachedRisk,
    BatchCancelOrdersResult,
    BatchCreateOrdersResult,
    BatchReplaceItem,
    BatchReplaceOrdersResult,
    BatchReplaceStatusResult,
    CancelAllAfterResult,
    CancelAllOrdersResult,
    CreateOrderRequest,
    GetOrderResult,
    ModifyOrderResult,
    OrderKey,
    OrderMutationResult,
    OrdersList,
    PreviewOrderResult,
)
from polyester.models.private_orders import PrivateOrdersEvent
from polyester.realtime.client import AsyncRealtimeClient, AsyncSubscription
from polyester.services._base import BaseService
from polyester.services._generated import unary_auth_decoded
from polyester.services._realtime_subscribe import require_realtime
from polyester.services._scope import AccountScope, ScopedSubAccountMixin, resolve_account_id
from polyester.services._symbols import (
    resolve_cancel_all_symbol_ids,
    resolve_optional_symbol_id,
    resolve_symbol_id,
)
from polyester.services._validation import validate_limit


class AsyncOrdersService(ScopedSubAccountMixin, BaseService):
    def __init__(
        self,
        transport,
        catalogs: CatalogManager,
        default_sub_account_id: str | None,
        *,
        default_account_id: str | int | None = None,
        realtime: AsyncRealtimeClient | None = None,
        wait_for_catalogs: Callable[[], Awaitable[None]] | None = None,
    ) -> None:
        super().__init__(transport)
        self._catalogs = catalogs
        self._default_sub_account_id = default_sub_account_id
        self._default_account_id = default_account_id
        self._realtime = realtime
        self._wait_for_catalogs = wait_for_catalogs

    async def _ensure_catalogs(self) -> None:
        if self._wait_for_catalogs is not None:
            await self._wait_for_catalogs()

    async def list_open(
        self,
        *,
        account: AccountScope | None = None,
        sub_account_id: str | None = None,
        page_token: str | None = None,
        limit: int | None = None,
        include_attached_risk: bool = False,
        include_attached_risk_state: bool = False,
        trigger_id: str | int | None = None,
    ) -> OrdersList:
        """List open orders.

        When ``trigger_id`` is set, only child orders created by that trigger
        are returned (for example TWAP/ladder slice children).
        """
        validated_limit = validate_limit(limit, allow_none=True)
        request = GetOpenOrdersRequest(
            include_attached_risk=include_attached_risk,
            include_attached_risk_state=include_attached_risk_state,
        )
        parsed_sub = parse_optional_subaccount_id(
            self._resolve_sub_account_id(sub_account_id, account=account)
        )
        if parsed_sub is not None:
            request.subaccount_id = parsed_sub
        if page_token:
            request.page_token = page_token
        if validated_limit is not None:
            request.limit = validated_limit
        if trigger_id is not None and trigger_id != "":
            request.trigger_id = id_to_int(trigger_id, "trigger_id")
        return await unary_auth_decoded(
            self._transport,
            OrdersReadServiceClient,
            lambda client, req: client.get_open_orders(req),
            request,
            orders_list_from_proto,
        )

    async def list_history(
        self,
        *,
        account: AccountScope | None = None,
        sub_account_id: str | None = None,
        symbol: str | None = None,
        symbol_id: int | None = None,
        page_token: str | None = None,
        limit: int = 100,
        include_attached_risk: bool = False,
        include_attached_risk_state: bool = False,
        trigger_id: str | int | None = None,
    ) -> OrdersList:
        """List order history.

        When ``trigger_id`` is set, only child orders created by that trigger
        are returned (for example TWAP/ladder slice children).
        """
        validated_limit = validate_limit(limit)
        request = GetOrderHistoryRequest(
            limit=validated_limit,
            include_attached_risk=include_attached_risk,
            include_attached_risk_state=include_attached_risk_state,
        )
        parsed_sub = parse_optional_subaccount_id(
            self._resolve_sub_account_id(sub_account_id, account=account)
        )
        if parsed_sub is not None:
            request.subaccount_id = parsed_sub
        if symbol_id is not None:
            request.symbol_id.append(symbol_id)
        elif symbol:
            resolved = resolve_symbol_id(
                self._catalogs, symbol=symbol, symbol_id=None, label="list_history"
            )
            request.symbol_id.append(resolved)
        if page_token:
            request.page_token = page_token
        if trigger_id is not None and trigger_id != "":
            request.trigger_id = id_to_int(trigger_id, "trigger_id")
        return await unary_auth_decoded(
            self._transport,
            OrdersReadServiceClient,
            lambda client, req: client.get_order_history(req),
            request,
            orders_list_from_proto,
        )

    async def get(
        self,
        *,
        key: OrderKey,
        account: AccountScope | None = None,
        sub_account_id: str | None = None,
        include_attached_risk: bool = False,
        include_attached_risk_state: bool = False,
        include_execution_history: bool | None = None,
        limit: int | None = None,
        page_token: str | None = None,
    ) -> GetOrderResult:
        """Fetch one order and an optional page of lineage execution history.

        Execution history is enabled by default on the server. Pass
        ``include_execution_history=False`` for state-only polling and omit
        ``limit`` / ``page_token``. Continue pagination with the same physical
        ``order_id`` and ``next_page_token``. An empty page is not a
        settlement watermark; ``cum_qty`` / ``avg_px`` are lineage-cumulative.
        """
        if include_execution_history is False and (
            limit is not None or (page_token is not None and page_token != "")
        ):
            raise PolyesterValidationError(
                "orders.get limit and page_token require include_execution_history"
            )
        request = GetOrderRequest(
            include_attached_risk=include_attached_risk,
            include_attached_risk_state=include_attached_risk_state,
        )
        if include_execution_history is not None:
            request.include_execution_history = include_execution_history
        validated_limit = validate_limit(limit, allow_none=True)
        if validated_limit is not None:
            request.limit = validated_limit
        if page_token:
            request.page_token = page_token
        set_order_key(request, key, op="get")
        parsed_sub = parse_optional_subaccount_id(
            self._resolve_sub_account_id(sub_account_id, account=account)
        )
        if parsed_sub is not None:
            request.subaccount_id = parsed_sub
        return await unary_auth_decoded(
            self._transport,
            OrdersReadServiceClient,
            lambda client, req: client.get_order(req),
            request,
            get_order_from_proto,
        )

    async def create(
        self,
        request: CreateOrderRequest | None = None,
        *,
        account: str | dict[str, str] | None = None,
        **kwargs: Any,
    ) -> OrderMutationResult:
        """Create an order.

        ``client_order_id`` is optional. Set a stable non-empty value so you
        can reconcile after an ambiguous failure. Look up that id before
        creating again; a second create with the same id is a conflict if the
        first attempt admitted.
        """
        if account is not None:
            kwargs = {
                **kwargs,
                "sub_account_id": self._resolve_sub_account_id(account=account),
            }
        normalized = normalize_create_order_request(request, **kwargs)
        if normalized.sub_account_id is None:
            resolved_sub = self._resolve_sub_account_id(None)
            if resolved_sub is not None:
                normalized = msgspec.structs.replace(normalized, sub_account_id=resolved_sub)
        await self._ensure_catalogs()
        quantity_scale = resolve_quantity_scale(self._catalogs, normalized.symbol, normalized.qty)
        quote_quantity_scale = resolve_quote_quantity_scale(
            self._catalogs, normalized.symbol, normalized.max_quote_debit
        )
        normalized = msgspec.structs.replace(
            normalized,
            symbol_id=resolve_symbol_id(
                self._catalogs,
                symbol=normalized.symbol,
                symbol_id=normalized.symbol_id,
                label="orders.create",
            ),
        )
        proto_request = create_order_to_proto(
            normalized,
            quantity_scale=quantity_scale,
            quote_quantity_scale=quote_quantity_scale,
        )
        return await unary_auth_decoded(
            self._transport,
            OrdersServiceClient,
            lambda client, req: client.create_order(req),
            proto_request,
            lambda response: order_mutation_from_proto(response, quantity_scale=quantity_scale),
        )

    async def preview_order(
        self,
        request: CreateOrderRequest | None = None,
        *,
        account: str | dict[str, str] | None = None,
        **kwargs: Any,
    ) -> PreviewOrderResult:
        """Check current order admissibility without creating an order.

        Returns resolved base size and protected price bound when available.
        Does not return fee or quote-debit estimates. Accepts the same public
        create shape; the wire request wraps an ``OrderIntent``.
        """
        if account is not None:
            kwargs = {
                **kwargs,
                "sub_account_id": self._resolve_sub_account_id(account=account),
            }
        normalized = normalize_create_order_request(request, **kwargs)
        if normalized.sub_account_id is None:
            resolved_sub = self._resolve_sub_account_id(None)
            if resolved_sub is not None:
                normalized = msgspec.structs.replace(normalized, sub_account_id=resolved_sub)
        await self._ensure_catalogs()
        quantity_scale = resolve_quantity_scale(self._catalogs, normalized.symbol, normalized.qty)
        quote_quantity_scale = resolve_quote_quantity_scale(
            self._catalogs, normalized.symbol, normalized.max_quote_debit
        )
        normalized = msgspec.structs.replace(
            normalized,
            symbol_id=resolve_symbol_id(
                self._catalogs,
                symbol=normalized.symbol,
                symbol_id=normalized.symbol_id,
                label="orders.preview",
            ),
        )
        symbol_id = normalized.symbol_id
        proto_request = preview_order_to_proto(
            normalized,
            quantity_scale=quantity_scale,
            quote_quantity_scale=quote_quantity_scale,
        )
        return await unary_auth_decoded(
            self._transport,
            OrdersServiceClient,
            lambda client, req: client.preview_order(req),
            proto_request,
            lambda response: preview_order_from_proto(
                response,
                quantity_scale=quantity_scale,
                symbol=normalized.symbol,
                symbol_id=symbol_id,
            ),
        )

    async def cancel(
        self,
        *,
        key: OrderKey,
        account: AccountScope | None = None,
        symbol: str | None = None,
        symbol_id: int | None = None,
        sub_account_id: str | None = None,
    ) -> OrderMutationResult:
        if symbol is not None and symbol_id is not None:
            raise PolyesterValidationError("cancel accepts only one of symbol or symbol_id")
        if symbol is not None:
            symbol_id = resolve_symbol_id(
                self._catalogs,
                symbol=symbol,
                symbol_id=None,
                label="cancel",
            )
        request = CancelOrderRequest()
        set_order_key(request, key, op="cancel")
        if symbol_id is not None:
            request.symbol_id = symbol_id
        parsed_sub = parse_optional_subaccount_id(
            self._resolve_sub_account_id(sub_account_id, account=account)
        )
        if parsed_sub is not None:
            request.subaccount_id = parsed_sub
        return await unary_auth_decoded(
            self._transport,
            OrdersServiceClient,
            lambda client, req: client.cancel_order(req),
            request,
            order_mutation_from_proto,
        )

    async def modify(
        self,
        *,
        key: OrderKey,
        symbol: str,
        account: AccountScope | None = None,
        sub_account_id: str | None = None,
        request_id: str | None = None,
        new_price: object | None = None,
        new_qty: object | None = None,
        new_attached_risk: dict | AttachedRisk | None = None,
        behavior: str | None = None,
        new_client_order_id: str | None = None,
    ) -> ModifyOrderResult:
        await self._ensure_catalogs()
        scale = resolve_quantity_scale(self._catalogs, symbol, new_qty)
        proto_request = modify_order_to_proto(
            symbol=symbol,
            symbol_id=resolve_symbol_id(
                self._catalogs, symbol=symbol, symbol_id=None, label="orders.modify"
            ),
            key=key,
            sub_account_id=self._resolve_sub_account_id(sub_account_id, account=account),
            request_id=request_id,
            new_price=new_price,
            new_qty=new_qty,
            new_attached_risk=new_attached_risk,
            behavior=behavior,
            new_client_order_id=new_client_order_id,
            quantity_scale=scale,
        )
        return await unary_auth_decoded(
            self._transport,
            OrdersServiceClient,
            lambda client, req: client.modify_order(req),
            proto_request,
            modify_order_from_proto,
        )

    async def cancel_all(
        self,
        *,
        account: AccountScope | None = None,
        sub_account_id: str | None = None,
        symbol: str | None = None,
        symbols: list[str] | None = None,
        symbol_ids: list[int] | None = None,
        side: str | None = None,
        dry_run: bool = False,
        request_id: str | None = None,
    ) -> CancelAllOrdersResult:
        if symbol or symbols:
            await self._ensure_catalogs()
        proto_request = cancel_all_orders_to_proto(
            sub_account_id=self._resolve_sub_account_id(sub_account_id, account=account),
            symbol_ids=resolve_cancel_all_symbol_ids(
                self._catalogs,
                symbol=symbol,
                symbols=symbols,
                symbol_ids=symbol_ids,
                label="orders.cancel_all",
            ),
            side=side,
            dry_run=dry_run,
            request_id=request_id,
        )
        return await unary_auth_decoded(
            self._transport,
            OrdersServiceClient,
            lambda client, req: client.cancel_all_orders(req),
            proto_request,
            cancel_all_from_proto,
        )

    async def batch_replace(
        self,
        *,
        account: AccountScope | None = None,
        items: list[BatchReplaceItem | dict],
        sub_account_id: str | None = None,
        symbol: str,
        request_id: str | None = None,
    ) -> BatchReplaceOrdersResult:
        await self._ensure_catalogs()
        symbol_id = resolve_symbol_id(
            self._catalogs, symbol=symbol, symbol_id=None, label="batch_replace"
        )
        scale = resolve_quantity_scale(
            self._catalogs,
            symbol,
            *(
                item.new_qty if isinstance(item, BatchReplaceItem) else item.get("new_qty")
                for item in items
            ),
        )
        proto_request = batch_replace_orders_to_proto(
            items=items,
            symbol_id=symbol_id,
            sub_account_id=self._resolve_sub_account_id(sub_account_id, account=account),
            request_id=request_id,
            quantity_scale=scale,
        )
        return await unary_auth_decoded(
            self._transport,
            OrdersServiceClient,
            lambda client, req: client.batch_replace_orders(req),
            proto_request,
            batch_replace_from_proto,
        )

    async def get_batch_replace_status(
        self,
        *,
        batch_request_id: str,
        account: AccountScope | None = None,
        sub_account_id: str | None = None,
    ) -> BatchReplaceStatusResult:
        request = GetBatchReplaceStatusRequest(
            batch_request_id=id_to_int(batch_request_id, "batch_request_id")
        )
        parsed_sub = parse_optional_subaccount_id(
            self._resolve_sub_account_id(sub_account_id, account=account)
        )
        if parsed_sub is not None:
            request.subaccount_id = parsed_sub
        return await unary_auth_decoded(
            self._transport,
            OrdersReadServiceClient,
            lambda client, req: client.get_batch_replace_status(req),
            request,
            batch_replace_status_from_proto,
        )

    async def batch_create(
        self,
        *,
        account: AccountScope | None = None,
        items: list[CreateOrderRequest | dict[str, Any]],
        sub_account_id: str | None = None,
        symbol: str | None = None,
        request_id: str | None = None,
        allow_partial: bool = False,
    ) -> BatchCreateOrdersResult:
        qty_values: list[object | None] = []
        scale_symbol = symbol
        for item in items:
            if isinstance(item, CreateOrderRequest):
                qty_values.append(item.qty)
                if scale_symbol is None and item.symbol:
                    scale_symbol = item.symbol
            else:
                qty_values.append(item.get("qty"))
                if scale_symbol is None and item.get("symbol"):
                    scale_symbol = str(item["symbol"])
        await self._ensure_catalogs()
        scale = resolve_quantity_scale(self._catalogs, scale_symbol, *qty_values)
        resolved_items: list[CreateOrderRequest] = []
        for item in items:
            normalized = (
                item
                if isinstance(item, CreateOrderRequest)
                else normalize_create_order_request(item)
            )
            resolved_items.append(
                msgspec.structs.replace(
                    normalized,
                    symbol_id=resolve_symbol_id(
                        self._catalogs,
                        symbol=normalized.symbol,
                        symbol_id=normalized.symbol_id,
                        label="batch_create",
                    ),
                )
            )
        proto_request = batch_create_orders_to_proto(
            items=resolved_items,
            sub_account_id=self._resolve_sub_account_id(sub_account_id, account=account),
            request_id=request_id,
            allow_partial=allow_partial,
            quantity_scale=scale,
        )
        return await unary_auth_decoded(
            self._transport,
            OrdersServiceClient,
            lambda client, req: client.batch_create_orders(req),
            proto_request,
            batch_create_from_proto,
        )

    async def batch_cancel(
        self,
        *,
        account: AccountScope | None = None,
        items: list[dict],
        sub_account_id: str | None = None,
        request_id: str | None = None,
    ) -> BatchCancelOrdersResult:
        proto_request = batch_cancel_orders_to_proto(
            items=items,
            sub_account_id=self._resolve_sub_account_id(sub_account_id, account=account),
            request_id=request_id,
        )
        return await unary_auth_decoded(
            self._transport,
            OrdersServiceClient,
            lambda client, req: client.batch_cancel_orders(req),
            proto_request,
            batch_cancel_from_proto,
        )

    async def cancel_all_after(
        self,
        *,
        account: AccountScope | None = None,
        timeout_sec: int,
        sub_account_id: str | None = None,
        symbol: str | None = None,
        side: str | None = None,
        request_id: str | None = None,
    ) -> CancelAllAfterResult:
        if symbol:
            await self._ensure_catalogs()
        proto_request = cancel_all_after_to_proto(
            sub_account_id=self._resolve_sub_account_id(sub_account_id, account=account),
            timeout_sec=timeout_sec,
            symbol_id=resolve_optional_symbol_id(
                self._catalogs, symbol=symbol, label="orders.cancel_all_after symbol"
            ),
            side=side,
            request_id=request_id,
        )
        return await unary_auth_decoded(
            self._transport,
            OrdersServiceClient,
            lambda client, req: client.cancel_all_after(req),
            proto_request,
            cancel_all_after_from_proto,
        )

    async def subscribe(
        self,
        *,
        account_id: str | int | None = None,
    ) -> AsyncSubscription[PrivateOrdersEvent]:
        """Stream an account's live orders over the private WebSocket.

        Returns once the server confirmed the subscription. Iterate the
        events: ``PrivateOrdersSnapshot`` (the full live view; replace local
        state), ``PrivateOrdersUnit`` (changed orders, removed order IDs and
        order events), ``PrivateOrdersReady`` (the stream reflects every order
        read made before the subscribe; wait for it before relying on the
        stream), ``PrivateOrdersStale``, ``PrivateOrdersConnected``,
        ``PrivateOrdersDisconnected`` and ``PrivateOrdersError``. Orders are
        the same ``Order`` model the reads return; keep the copy with the
        higher ``version``. Gaps, expired tokens and reconnects resume from
        the last applied position automatically. A failure that ends the
        stream (for example a refused token) is raised from iteration.
        """
        client = require_realtime(self._realtime)
        resolved = resolve_account_id(account_id, self._default_account_id)
        return await client.subscribe_private_orders(resolved)

    async def wait_for_order_trades_complete(
        self,
        *,
        key: OrderKey,
        account: AccountScope | None = None,
        sub_account_id: str | None = None,
        timeout: float = 10.0,
        poll_interval: float = 0.1,
    ) -> GetOrderResult:
        """Poll ``get`` until projected trade qtys sum to order ``cum_qty`` or timeout.

        GetOrder can report lineage-cumulative ``cum_qty`` before every fill is
        visible on the trades list (eventual consistency). This helper pages
        execution history and does not treat an empty page as a watermark.
        """
        return await wait_for_order_trades_complete(
            self,
            key=key,
            account=account,
            sub_account_id=sub_account_id,
            timeout=timeout,
            poll_interval=poll_interval,
        )


async def wait_for_order_trades_complete(
    orders: AsyncOrdersService,
    *,
    key: OrderKey,
    account: AccountScope | None = None,
    sub_account_id: str | None = None,
    timeout: float = 10.0,
    poll_interval: float = 0.1,
) -> GetOrderResult:
    """Poll until ``sum(trade.qty) == order.cum_qty`` or ``timeout`` elapses."""
    deadline = time.monotonic() + max(timeout, 0.0)
    last: GetOrderResult | None = None
    while True:
        last = await _get_order_execution_pages(
            orders,
            key=key,
            account=account,
            sub_account_id=sub_account_id,
        )
        if _order_trades_projection_complete(last):
            return last
        if time.monotonic() >= deadline:
            raise PolyesterTransportError(
                f"timed out waiting for order trades to match cum_qty (key={key!r})"
            )
        await asyncio.sleep(max(poll_interval, 0.0))


async def _get_order_execution_pages(
    orders: AsyncOrdersService,
    *,
    key: OrderKey,
    account: AccountScope | None = None,
    sub_account_id: str | None = None,
) -> GetOrderResult:
    page_token: str | None = None
    trades: list = []
    transfers: list = []
    order = None
    while True:
        page = await orders.get(
            key=key,
            account=account,
            sub_account_id=sub_account_id,
            include_execution_history=True,
            page_token=page_token,
        )
        if page.order is not None:
            order = page.order
        trades.extend(page.trades)
        transfers.extend(page.transfers)
        if not page.next_page_token:
            return GetOrderResult(
                order=order,
                trades=trades,
                transfers=transfers,
                next_page_token="",
                executions_complete=page.executions_complete,
            )
        page_token = page.next_page_token


def _order_trades_projection_complete(result: GetOrderResult) -> bool:
    order = result.order
    if order is None or order.cum_qty is None:
        return False
    cum = order.cum_qty.scaled
    if cum == 0:
        return True
    trade_sum = 0
    for trade in result.trades:
        if trade.qty is None:
            return False
        trade_sum += trade.qty.scaled
    return trade_sum == cum


def is_batch_replace_settled(status: BatchReplaceStatusResult) -> bool:
    """Whether every replacement has left admission and reached a stable phase.

    ``terminal`` means the successor's lifecycle is terminal, not necessarily
    that the original replacement request failed. Poll status to reconcile
    predecessor/successor IDs and phases; do not infer finality from admission.
    """
    return bool(status.items) and all(
        item.phase in {"working", "rejected", "terminal"} for item in status.items
    )
