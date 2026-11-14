from __future__ import annotations

from polyester.codecs.decode.transfers import transfers_list_from_proto
from polyester.codecs.orders import parse_optional_subaccount_id
from polyester.codecs.realtime_decode import decode_ledger_transfer_batch_bytes
from polyester.gen.ledger.read.v1.ledger_read_connect import LedgerReadServiceClient
from polyester.gen.ledger.read.v1.ledger_read_pb2 import ListTransfersRequest
from polyester.models import LedgerTransfer, TransfersList
from polyester.realtime.client import AsyncRealtimeClient, AsyncSubscription
from polyester.services._base import BaseService
from polyester.services._generated import unary_auth_decoded
from polyester.services._realtime_subscribe import subscribe_account_proto_batch
from polyester.services._scope import AccountScope, ScopedSubAccountMixin
from polyester.services._validation import validate_limit


class AsyncTransfersService(ScopedSubAccountMixin, BaseService):
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
        limit: int = 50,
        reversed: bool = False,
        since: int | None = None,
    ) -> TransfersList:
        request = ListTransfersRequest(limit=validate_limit(limit), reversed=reversed)
        parsed_sub = parse_optional_subaccount_id(
            self._resolve_sub_account_id(sub_account_id, account=account)
        )
        if parsed_sub is not None:
            request.subaccount_id = parsed_sub
        if since is not None:
            request.since = since
        return await unary_auth_decoded(
            self._transport,
            LedgerReadServiceClient,
            lambda client, req: client.list_transfers(req),
            request,
            transfers_list_from_proto,
        )

    async def subscribe(
        self,
        *,
        account_id: str | int | None = None,
    ) -> AsyncSubscription[LedgerTransfer]:
        return await subscribe_account_proto_batch(
            self._realtime,
            channel_template="private:ledger:transfers:{account_id}:proto",
            account_id=account_id,
            default_account_id=self._default_account_id,
            decode_batch=decode_ledger_transfer_batch_bytes,
        )
