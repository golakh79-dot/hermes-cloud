from __future__ import annotations

from polyester.catalogs import CatalogManager
from polyester.codecs.decode.internal_transfers import internal_transfer_from_proto
from polyester.codecs.ledger_amounts import LEDGER_SCALE
from polyester.codecs.orders import parse_optional_subaccount_id
from polyester.codecs.scalars import id_to_int
from polyester.codecs.withdraw import str_to_u128_proto
from polyester.errors import PolyesterValidationError
from polyester.gen.transfer.v1.internal_transfer_connect import InternalTransferServiceClient
from polyester.gen.transfer.v1.internal_transfer_pb2 import CreateInternalTransferRequest
from polyester.models import InternalTransferResult
from polyester.services._base import BaseService
from polyester.services._generated import unary_auth_decoded
from polyester.services._scope import AccountScope, ScopedSubAccountMixin
from polyester.types.money import AssetAmount


class AsyncInternalTransfersService(ScopedSubAccountMixin, BaseService):
    def __init__(
        self,
        transport,
        catalogs: CatalogManager,
        default_sub_account_id: str | None,
    ) -> None:
        super().__init__(transport)
        self._catalogs = catalogs
        self._default_sub_account_id = default_sub_account_id

    async def create(
        self,
        *,
        asset_id: int,
        quantity: str | AssetAmount,
        idempotency_key: str,
        account: AccountScope | None = None,
        sub_account_id: str | None = None,
        destination_account_id: str | int | None = None,
        destination_subaccount_id: str | int | None = None,
        destination_smart_account_address: str | None = None,
        quantity_scale: int | None = None,
    ) -> InternalTransferResult:
        destination_count = sum(
            (
                destination_account_id is not None,
                destination_subaccount_id is not None,
                bool(destination_smart_account_address),
            )
        )
        if destination_count != 1:
            raise PolyesterValidationError(
                "create requires exactly one of destination_account_id, "
                "destination_subaccount_id, or destination_smart_account_address"
            )
        if not idempotency_key.strip():
            raise PolyesterValidationError(
                "create requires a non-empty idempotency_key reused across retries"
            )
        scale = quantity_scale if quantity_scale is not None else LEDGER_SCALE
        request = CreateInternalTransferRequest(
            asset_id=asset_id,
            amount_e18=str_to_u128_proto(quantity, scale=scale, asset_id=asset_id),
            idempotency_key=idempotency_key,
        )
        parsed_sub = parse_optional_subaccount_id(
            self._resolve_sub_account_id(sub_account_id, account=account)
        )
        if parsed_sub is not None:
            request.subaccount_id = parsed_sub
        if destination_account_id is not None:
            request.destination_account_id = id_to_int(
                destination_account_id, "destination_account_id"
            )
        if destination_subaccount_id is not None:
            request.destination_subaccount_id = id_to_int(
                destination_subaccount_id, "destination_subaccount_id"
            )
        if destination_smart_account_address:
            request.destination_smart_account_address = destination_smart_account_address
        return await unary_auth_decoded(
            self._transport,
            InternalTransferServiceClient,
            lambda client, req: client.create_internal_transfer(req),
            request,
            internal_transfer_from_proto,
        )
