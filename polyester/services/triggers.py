from __future__ import annotations

from collections.abc import Awaitable, Callable, Sequence
from decimal import Decimal

from polyester.catalogs import CatalogManager
from polyester.codecs.decode.triggers import (
    get_trigger_from_proto,
    trigger_events_list_from_proto,
    trigger_mutation_from_proto,
    trigger_status_from_label,
    triggers_list_from_proto,
)
from polyester.codecs.orders import parse_optional_subaccount_id, resolve_quantity_scale
from polyester.codecs.realtime_decode import decode_trigger_bytes, decode_trigger_event_batch_bytes
from polyester.codecs.scalars import id_to_int
from polyester.codecs.triggers import (
    create_trigger_to_proto,
    modify_trigger_to_proto,
)
from polyester.gen.triggers.v1.triggers_connect import TriggersServiceClient
from polyester.gen.triggers.v1.triggers_pb2 import (
    CancelTriggerRequest,
    GetTriggerRequest,
    ListTriggerEventsRequest,
    ListTriggersRequest,
    PauseTriggerRequest,
    ResumeTriggerRequest,
    TriggerEventType,
)
from polyester.models import (
    Trigger,
    TriggerEvent,
    TriggerEventsList,
    TriggerMutationResult,
    TriggersList,
)
from polyester.realtime.client import AsyncRealtimeClient, AsyncSubscription
from polyester.services._base import BaseService
from polyester.services._generated import unary_auth_decoded
from polyester.services._realtime_subscribe import (
    subscribe_account_proto,
    subscribe_account_proto_batch,
)
from polyester.services._scope import AccountScope, ScopedSubAccountMixin
from polyester.services._symbols import resolve_optional_symbol_id, resolve_symbol_id
from polyester.services._validation import validate_limit
from polyester.types.money import Price


class AsyncTriggersService(ScopedSubAccountMixin, BaseService):
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

    async def _optional_control_symbol_id(
        self, *, symbol: str | None, symbol_id: int | None, label: str
    ) -> int:
        """Symbol ID for modify/resume; ``0`` targets the trigger's own market."""
        if symbol is not None:
            await self._ensure_catalogs()
        return (
            resolve_optional_symbol_id(
                self._catalogs, symbol=symbol, symbol_id=symbol_id, label=label
            )
            or 0
        )

    async def _ensure_catalogs(self) -> None:
        if self._wait_for_catalogs is not None:
            await self._wait_for_catalogs()

    async def list(
        self,
        *,
        account: AccountScope | None = None,
        sub_account_id: str | None = None,
        symbol: str | None = None,
        status: str | Sequence[str] | None = None,
        limit: int = 50,
        page_token: str | None = None,
    ) -> TriggersList:
        """List triggers.

        ``status`` accepts one or more of: created, armed, running, completed,
        cancelled, failed, paused. Unknown values raise ``PolyesterValidationError``.
        """
        validated_limit = validate_limit(limit)
        request = ListTriggersRequest(limit=validated_limit)
        if page_token:
            request.page_token = page_token
        parsed_sub = parse_optional_subaccount_id(
            self._resolve_sub_account_id(sub_account_id, account=account)
        )
        if parsed_sub is not None:
            request.subaccount_id = parsed_sub
        if symbol:
            await self._ensure_catalogs()
            request.symbol_id = resolve_optional_symbol_id(
                self._catalogs, symbol=symbol, label="triggers.list symbol"
            ) or 0
        if status is not None:
            labels = [status] if isinstance(status, str) else list(status)
            request.status.extend(trigger_status_from_label(label) for label in labels)
        return await unary_auth_decoded(
            self._transport,
            TriggersServiceClient,
            lambda client, req: client.list_triggers(req),
            request,
            triggers_list_from_proto,
        )

    async def get(
        self,
        *,
        account: AccountScope | None = None,
        trigger_id: str | int,
        sub_account_id: str | None = None,
    ) -> Trigger | None:
        request = GetTriggerRequest(trigger_id=id_to_int(trigger_id, "trigger_id"))
        parsed_sub = parse_optional_subaccount_id(
            self._resolve_sub_account_id(sub_account_id, account=account)
        )
        if parsed_sub is not None:
            request.subaccount_id = parsed_sub
        return await unary_auth_decoded(
            self._transport,
            TriggersServiceClient,
            lambda client, req: client.get_trigger(req),
            request,
            get_trigger_from_proto,
        )

    async def create(
        self,
        *,
        account: AccountScope | None = None,
        symbol: str,
        trigger_type: str,
        side: str,
        qty: str,
        trigger_price: str | None = None,
        order_type: str = "market",
        limit_price: str | Decimal | Price | None = None,
        trigger_price_source: str | None = None,
        tif: str = "gtc",
        sub_account_id: str | None = None,
        client_trigger_id: str | None = None,
        post_only: bool = False,
        fee_asset: str | None = None,
        self_trade_prevention_mode: str | None = None,
        trailing_distance_ticks: int | None = None,
        trailing_distance_bps: int | None = None,
        activation_price: str | None = None,
        max_slippage_ticks: int | None = None,
        max_slippage_bps: int | None = None,
        twap_duration_ms: int | None = None,
        twap_slice_interval_ms: int | None = None,
        ladder_price_min: str | None = None,
        ladder_price_max: str | None = None,
        ladder_levels: int | None = None,
        ladder_distribution: str | None = None,
    ) -> TriggerMutationResult:
        """Create a standalone trigger.

        ``limit_price`` is the child's limit price for a limit stop-loss or
        take-profit. For ``trigger_type="trailing_stop"`` with ``side="buy"`` it
        is the required maximum price, the most the child pays per unit (a
        9-decimal string or ``Decimal``, or ``Price.from_ticks`` for ticks);
        a sell trailing stop takes none. The maximum price is fixed at create.

        ``trigger_price_source`` (``last``, ``index`` or ``mark``) sets the
        price a stop-loss, take-profit or trailing stop watches; unset means
        the last trade price.
        """
        await self._ensure_catalogs()
        scale = resolve_quantity_scale(self._catalogs, symbol, qty)
        request = create_trigger_to_proto(
            symbol=symbol,
            symbol_id=resolve_symbol_id(
                self._catalogs, symbol=symbol, symbol_id=None, label="triggers.create"
            ),
            trigger_type=trigger_type,
            trigger_price=trigger_price,
            side=side,
            qty=qty,
            order_type=order_type,
            limit_price=limit_price,
            trigger_price_source=trigger_price_source,
            tif=tif,
            sub_account_id=self._resolve_sub_account_id(sub_account_id, account=account),
            client_trigger_id=client_trigger_id,
            post_only=post_only,
            fee_asset=fee_asset,
            self_trade_prevention_mode=self_trade_prevention_mode,
            trailing_distance_ticks=trailing_distance_ticks,
            trailing_distance_bps=trailing_distance_bps,
            activation_price=activation_price,
            max_slippage_ticks=max_slippage_ticks,
            max_slippage_bps=max_slippage_bps,
            twap_duration_ms=twap_duration_ms,
            twap_slice_interval_ms=twap_slice_interval_ms,
            ladder_price_min=ladder_price_min,
            ladder_price_max=ladder_price_max,
            ladder_levels=ladder_levels,
            ladder_distribution=ladder_distribution,
            quantity_scale=scale,
        )
        return await unary_auth_decoded(
            self._transport,
            TriggersServiceClient,
            lambda client, req: client.create_trigger(req),
            request,
            trigger_mutation_from_proto,
        )

    async def cancel(
        self,
        *,
        account: AccountScope | None = None,
        trigger_id: str | int,
        sub_account_id: str | None = None,
    ) -> TriggerMutationResult:
        request = CancelTriggerRequest(trigger_id=id_to_int(trigger_id, "trigger_id"))
        parsed_sub = parse_optional_subaccount_id(
            self._resolve_sub_account_id(sub_account_id, account=account)
        )
        if parsed_sub is not None:
            request.subaccount_id = parsed_sub
        return await unary_auth_decoded(
            self._transport,
            TriggersServiceClient,
            lambda client, req: client.cancel_trigger(req),
            request,
            trigger_mutation_from_proto,
        )

    async def modify(
        self,
        *,
        account: AccountScope | None = None,
        trigger_id: str | int,
        symbol: str | None = None,
        symbol_id: int | None = None,
        sub_account_id: str | None = None,
        trigger_price: str | None = None,
        trailing_distance_ticks: int | None = None,
        trailing_distance_bps: int | None = None,
        activation_price: str | None = None,
        max_slippage_ticks: int | None = None,
        max_slippage_bps: int | None = None,
    ) -> TriggerMutationResult:
        """Patch a live trigger; omitted fields stay unchanged.

        Without ``symbol``/``symbol_id`` the trigger's own market is used; when
        given, it must be that market, and an API key limited to specific
        markets must give it. A child's limit price is fixed at creation:
        cancel the trigger and create a new one to change it.
        ``max_slippage_bps`` is 1 to 9999; ``0`` clears a cap (ticks or bps)
        and a market child falls back to the pair's default slippage.
        """
        request = modify_trigger_to_proto(
            trigger_id=trigger_id,
            symbol_id=await self._optional_control_symbol_id(
                symbol=symbol, symbol_id=symbol_id, label="triggers.modify"
            ),
            sub_account_id=self._resolve_sub_account_id(sub_account_id, account=account),
            trigger_price=trigger_price,
            trailing_distance_ticks=trailing_distance_ticks,
            trailing_distance_bps=trailing_distance_bps,
            activation_price=activation_price,
            max_slippage_ticks=max_slippage_ticks,
            max_slippage_bps=max_slippage_bps,
        )
        return await unary_auth_decoded(
            self._transport,
            TriggersServiceClient,
            lambda client, req: client.modify_trigger(req),
            request,
            trigger_mutation_from_proto,
        )

    async def pause(
        self,
        *,
        account: AccountScope | None = None,
        trigger_id: str | int,
        sub_account_id: str | None = None,
    ) -> TriggerMutationResult:
        request = PauseTriggerRequest(trigger_id=id_to_int(trigger_id, "trigger_id"))
        parsed_sub = parse_optional_subaccount_id(
            self._resolve_sub_account_id(sub_account_id, account=account)
        )
        if parsed_sub is not None:
            request.subaccount_id = parsed_sub
        return await unary_auth_decoded(
            self._transport,
            TriggersServiceClient,
            lambda client, req: client.pause_trigger(req),
            request,
            trigger_mutation_from_proto,
        )

    async def resume(
        self,
        *,
        account: AccountScope | None = None,
        trigger_id: str | int,
        symbol: str | None = None,
        symbol_id: int | None = None,
        sub_account_id: str | None = None,
    ) -> TriggerMutationResult:
        """Resume a paused trigger; ``symbol`` is optional as for :meth:`modify`."""
        request = ResumeTriggerRequest(
            trigger_id=id_to_int(trigger_id, "trigger_id"),
            symbol_id=await self._optional_control_symbol_id(
                symbol=symbol, symbol_id=symbol_id, label="triggers.resume"
            ),
        )
        parsed_sub = parse_optional_subaccount_id(
            self._resolve_sub_account_id(sub_account_id, account=account)
        )
        if parsed_sub is not None:
            request.subaccount_id = parsed_sub
        return await unary_auth_decoded(
            self._transport,
            TriggersServiceClient,
            lambda client, req: client.resume_trigger(req),
            request,
            trigger_mutation_from_proto,
        )

    async def list_events(
        self,
        *,
        account: AccountScope | None = None,
        trigger_id: str | int,
        sub_account_id: str | None = None,
        limit: int = 50,
        event_type: str | None = None,
        page_token: str | None = None,
    ) -> TriggerEventsList:
        from typing import cast

        from polyester.codecs.decode.triggers import trigger_event_type_from_label

        validated_limit = validate_limit(limit)
        request = ListTriggerEventsRequest(
            trigger_id=id_to_int(trigger_id, "trigger_id"),
            limit=validated_limit,
        )
        parsed_sub = parse_optional_subaccount_id(
            self._resolve_sub_account_id(sub_account_id, account=account)
        )
        if parsed_sub is not None:
            request.subaccount_id = parsed_sub
        if event_type:
            request.event_type = cast(TriggerEventType, trigger_event_type_from_label(event_type))
        if page_token:
            request.page_token = page_token
        return await unary_auth_decoded(
            self._transport,
            TriggersServiceClient,
            lambda client, req: client.list_trigger_events(req),
            request,
            trigger_events_list_from_proto,
        )

    async def subscribe(
        self,
        *,
        account_id: str | int | None = None,
    ) -> AsyncSubscription[Trigger]:
        return await subscribe_account_proto(
            self._realtime,
            channel_template="private:spot:triggers:{account_id}:proto",
            account_id=account_id,
            default_account_id=self._default_account_id,
            decode=decode_trigger_bytes,
        )

    async def subscribe_events(
        self,
        *,
        account_id: str | int | None = None,
    ) -> AsyncSubscription[TriggerEvent]:
        return await subscribe_account_proto_batch(
            self._realtime,
            channel_template="private:spot:triggers:events:{account_id}:proto",
            account_id=account_id,
            default_account_id=self._default_account_id,
            decode_batch=decode_trigger_event_batch_bytes,
        )
