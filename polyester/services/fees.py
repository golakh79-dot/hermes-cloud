from __future__ import annotations

from collections.abc import Sequence

from polyester.catalogs import CatalogManager
from polyester.codecs.decode.fees import spot_fee_rates_list_from_proto
from polyester.codecs.orders import parse_optional_subaccount_id
from polyester.gen.fees.v1.fees_connect import FeeServiceClient
from polyester.gen.fees.v1.fees_pb2 import GetSpotFeeRatesRequest
from polyester.models.fees import SpotFeeRatesList
from polyester.services._base import BaseService
from polyester.services._generated import unary_auth_decoded
from polyester.services._scope import AccountScope, ScopedSubAccountMixin


class AsyncFeeService(ScopedSubAccountMixin, BaseService):
    def __init__(
        self,
        transport,
        default_sub_account_id: str | None,
        catalogs: CatalogManager | None = None,
    ) -> None:
        super().__init__(transport)
        self._default_sub_account_id = default_sub_account_id
        self._catalogs = catalogs or CatalogManager()

    async def get_spot_fee_rates(
        self,
        *,
        account: AccountScope | None = None,
        sub_account_id: str | None = None,
        symbol_id: int | Sequence[int] | None = None,
    ) -> SpotFeeRatesList:
        request = GetSpotFeeRatesRequest()
        parsed_sub = parse_optional_subaccount_id(
            self._resolve_sub_account_id(sub_account_id, account=account)
        )
        if parsed_sub is not None:
            request.subaccount_id = parsed_sub
        if symbol_id is not None:
            ids = [symbol_id] if isinstance(symbol_id, int) else list(symbol_id)
            request.symbol_id.extend(int(item) for item in ids)
        return await unary_auth_decoded(
            self._transport,
            FeeServiceClient,
            lambda client, req: client.get_spot_fee_rates(req),
            request,
            lambda msg: spot_fee_rates_list_from_proto(msg, self._catalogs),
        )
