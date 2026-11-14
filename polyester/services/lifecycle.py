from __future__ import annotations

from polyester.codecs.decode.lifecycle import (
    flow_from_get_response,
    flows_by_tx_list_from_proto,
    flows_list_from_proto,
)
from polyester.codecs.realtime_decode import decode_flow_detail_bytes, decode_flow_summary_bytes
from polyester.codecs.scalars import id_to_int
from polyester.errors import PolyesterValidationError
from polyester.gen.chain.lifecycle.v1.lifecycle_read_connect import LifecycleReadServiceClient
from polyester.gen.chain.lifecycle.v1.lifecycle_read_pb2 import (
    GetFlowByIdRequest,
    ListFlowsByTxRequest,
    ListFlowsRequest,
)
from polyester.models import LifecycleFlowsList, LifecycleFlowSummary
from polyester.realtime.client import AsyncRealtimeClient, AsyncSubscription
from polyester.services._base import BaseService
from polyester.services._generated import unary_public_decoded
from polyester.services._realtime_subscribe import subscribe_account_proto, subscribe_public_proto
from polyester.services._validation import validate_limit


class AsyncLifecycleService(BaseService):
    def __init__(self, transport, *, realtime: AsyncRealtimeClient | None = None) -> None:
        super().__init__(transport)
        self._realtime = realtime

    async def list_flows(
        self,
        *,
        limit: int = 50,
        page_token: str | None = None,
        scope: str | None = None,
        owner_account_id: str | int | None = None,
        smart_account_address: str | None = None,
        reversed: bool = False,
    ) -> LifecycleFlowsList:
        from polyester.gen.chain.lifecycle.v1 import lifecycle_read_pb2

        request = ListFlowsRequest(limit=validate_limit(limit))
        if reversed:
            request.sort = lifecycle_read_pb2.SORT_OLDEST
        else:
            request.sort = lifecycle_read_pb2.SORT_NEWEST
        if page_token:
            request.page_token = page_token
        if scope:
            scope_name = scope.upper()
            if not scope_name.startswith("LIST_"):
                scope_name = f"LIST_{scope_name}"
            scope_enum = getattr(lifecycle_read_pb2, scope_name, None)
            if scope_enum is None:
                raise PolyesterValidationError(
                    "scope must be one of 'all', 'open_only', or 'terminal_only'"
                )
            request.scope = scope_enum
        if owner_account_id is not None:
            request.owner_account_id = id_to_int(owner_account_id, "owner_account_id")
        if smart_account_address:
            request.smart_account_address = smart_account_address

        return await unary_public_decoded(
            self._transport,
            LifecycleReadServiceClient,
            lambda client, req: client.list_flows(req),
            request,
            flows_list_from_proto,
        )

    async def get_flow(
        self,
        *,
        intent_id: str | None = None,
        flow_id: str | None = None,
    ) -> LifecycleFlowSummary:
        resolved_flow_id = flow_id or intent_id
        if not resolved_flow_id:
            raise PolyesterValidationError("flow_id or intent_id is required")
        return await unary_public_decoded(
            self._transport,
            LifecycleReadServiceClient,
            lambda client, req: client.get_flow_by_id(req),
            GetFlowByIdRequest(flow_id=resolved_flow_id),
            flow_from_get_response,
        )

    async def get_flow_by_tx(
        self,
        *,
        tx_hash: str,
        lookup_kind: str = "any",
        limit: int = 50,
    ) -> LifecycleFlowsList:
        """Return all matches in the first page for a transaction lookup.

        A chain transaction can contain multiple bundled lifecycle flows.
        Use ``list_flows_by_tx`` directly when following pagination tokens.
        """
        return await self.list_flows_by_tx(
            tx_hash=tx_hash,
            lookup_kind=lookup_kind,
            limit=limit,
        )

    async def list_flows_by_tx(
        self,
        *,
        tx_hash: str,
        lookup_kind: str = "any",
        limit: int = 50,
        page_token: str | None = None,
    ) -> LifecycleFlowsList:
        from polyester.gen.chain.lifecycle.v1 import lifecycle_read_pb2

        kind_name = lookup_kind.upper()
        if not kind_name.startswith("TX_"):
            kind_name = f"TX_{kind_name}"
        lookup_enum = getattr(lifecycle_read_pb2, kind_name, lifecycle_read_pb2.TX_ANY)
        request = ListFlowsByTxRequest(
            tx_hash=tx_hash,
            lookup_kind=lookup_enum,
            limit=validate_limit(limit),
        )
        if page_token:
            request.page_token = page_token
        return await unary_public_decoded(
            self._transport,
            LifecycleReadServiceClient,
            lambda client, req: client.list_flows_by_tx(req),
            request,
            flows_by_tx_list_from_proto,
        )

    async def subscribe_open_flows(
        self,
        *,
        account_id: str | int | None = None,
    ) -> AsyncSubscription[LifecycleFlowSummary]:
        if account_id is not None and str(account_id).strip():
            return await subscribe_account_proto(
                self._realtime,
                channel_template="private:chain:lifecycle:flows:{account_id}:proto",
                account_id=account_id,
                default_account_id=None,
                decode=decode_flow_summary_bytes,
            )
        return await subscribe_public_proto(
            self._realtime,
            channel="public:chain:lifecycle:flows:proto",
            decode=decode_flow_summary_bytes,
        )

    async def subscribe_flow_detail(
        self,
        *,
        flow_id: str,
    ) -> AsyncSubscription[LifecycleFlowSummary]:
        if not flow_id.strip():
            raise PolyesterValidationError("flow_id is required")
        channel = f"public:chain:lifecycle:flow:{flow_id}:proto"
        return await subscribe_public_proto(
            self._realtime,
            channel=channel,
            decode=decode_flow_detail_bytes,
        )
