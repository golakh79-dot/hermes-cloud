from __future__ import annotations

from polyester.codecs.decode.deposit import (
    create_deposit_address_from_proto,
    deposit_addresses_list_from_proto,
)
from polyester.codecs.orders import parse_optional_subaccount_id
from polyester.gen.chain.deposit.v1.deposit_connect import DepositAddressServiceClient
from polyester.gen.chain.deposit.v1.deposit_pb2 import (
    CreateDepositAddressRequest,
    ListDepositAddressesRequest,
)
from polyester.models import DepositAddress, DepositAddressesList
from polyester.services._base import BaseService
from polyester.services._generated import unary_auth_decoded
from polyester.services._scope import AccountScope, ScopedSubAccountMixin


class AsyncDepositService(ScopedSubAccountMixin, BaseService):
    def __init__(self, transport, default_sub_account_id: str | None) -> None:
        super().__init__(transport)
        self._default_sub_account_id = default_sub_account_id

    async def list_addresses(
        self,
        *,
        chain_id: int,
        account: AccountScope | None = None,
        sub_account_id: str | None = None,
    ) -> DepositAddressesList:
        request = ListDepositAddressesRequest(chain_id=chain_id)
        parsed_sub = parse_optional_subaccount_id(
            self._resolve_sub_account_id(sub_account_id, account=account)
        )
        if parsed_sub is not None:
            request.subaccount_id = parsed_sub
        return await unary_auth_decoded(
            self._transport,
            DepositAddressServiceClient,
            lambda client, req: client.list_deposit_addresses(req),
            request,
            deposit_addresses_list_from_proto,
        )

    async def create_address(
        self,
        *,
        chain_id: int,
        account: AccountScope | None = None,
        sub_account_id: str | None = None,
    ) -> DepositAddress:
        request = CreateDepositAddressRequest(chain_id=chain_id)
        parsed_sub = parse_optional_subaccount_id(
            self._resolve_sub_account_id(sub_account_id, account=account)
        )
        if parsed_sub is not None:
            request.subaccount_id = parsed_sub
        return await unary_auth_decoded(
            self._transport,
            DepositAddressServiceClient,
            lambda client, req: client.create_deposit_address(req),
            request,
            create_deposit_address_from_proto,
        )
