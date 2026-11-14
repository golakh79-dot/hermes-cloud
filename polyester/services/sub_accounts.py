from __future__ import annotations

from polyester.codecs.decode.sub_accounts import (
    get_subaccount_from_proto,
    subaccount_activity_list_from_proto,
    subaccount_invites_list_from_proto,
    subaccount_members_list_from_proto,
    subaccounts_list_from_proto,
)
from polyester.codecs.orders import parse_optional_subaccount_id
from polyester.codecs.realtime_decode import decode_api_key_bytes, decode_subaccount_bytes
from polyester.codecs.sub_accounts import invite_direction_from_label
from polyester.errors import PolyesterValidationError
from polyester.gen.auth.v1.subaccounts_connect import (
    SubaccountServiceClient,
    SubaccountViewServiceClient,
)
from polyester.gen.auth.v1.subaccounts_pb2 import (
    GetSubaccountRequest,
    ListSubaccountEventsRequest,
    ListSubaccountInvitesRequest,
    ListSubaccountMembersRequest,
    ListSubaccountsRequest,
)
from polyester.models.sub_accounts import (
    GetSubaccountResult,
    SubAccount,
    SubAccountActivityList,
    SubAccountInvitesList,
    SubAccountMembersList,
    SubAccountsList,
)
from polyester.models.trading import ApiKeySummary
from polyester.realtime.client import AsyncRealtimeClient, AsyncSubscription
from polyester.services._base import BaseService
from polyester.services._generated import unary_auth_decoded
from polyester.services._realtime_subscribe import subscribe_account_proto
from polyester.services._scope import AccountScope, ScopedSubAccountMixin
from polyester.services._validation import validate_limit


class AsyncSubAccountsService(ScopedSubAccountMixin, BaseService):
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

    async def list(self) -> SubAccountsList:
        return await unary_auth_decoded(
            self._transport,
            SubaccountServiceClient,
            lambda client, req: client.list_subaccounts(req),
            ListSubaccountsRequest(),
            subaccounts_list_from_proto,
        )

    async def get(
        self,
        *,
        account: AccountScope | None = None,
        sub_account_id: str | None = None,
        include_api_keys: bool = False,
        include_members: bool = False,
        include_invites: bool = False,
        include_policy: bool = False,
        invites_direction: str = "",
    ) -> GetSubaccountResult:
        parsed_sub = parse_optional_subaccount_id(
            self._resolve_sub_account_id(sub_account_id, account=account)
        )
        if parsed_sub is None:
            raise PolyesterValidationError("sub_account_id is required")
        request = GetSubaccountRequest(
            subaccount_id=parsed_sub,
            include_api_keys=include_api_keys,
            include_members=include_members,
            include_invites=include_invites,
            include_policy=include_policy,
            invites_direction=invite_direction_from_label(invites_direction),
        )
        return await unary_auth_decoded(
            self._transport,
            SubaccountViewServiceClient,
            lambda client, req: client.get_subaccount(req),
            request,
            get_subaccount_from_proto,
        )

    async def list_members(
        self,
        *,
        account: AccountScope | None = None,
        sub_account_id: str | None = None,
    ) -> SubAccountMembersList:
        parsed_sub = parse_optional_subaccount_id(
            self._resolve_sub_account_id(sub_account_id, account=account)
        )
        if parsed_sub is None:
            raise PolyesterValidationError("sub_account_id is required")
        return await unary_auth_decoded(
            self._transport,
            SubaccountServiceClient,
            lambda client, req: client.list_subaccount_members(req),
            ListSubaccountMembersRequest(subaccount_id=parsed_sub),
            subaccount_members_list_from_proto,
        )

    async def list_invites(self, *, direction: str = "") -> SubAccountInvitesList:
        return await unary_auth_decoded(
            self._transport,
            SubaccountServiceClient,
            lambda client, req: client.list_subaccount_invites(req),
            ListSubaccountInvitesRequest(direction=invite_direction_from_label(direction)),
            subaccount_invites_list_from_proto,
        )

    async def list_activity(
        self,
        *,
        account: AccountScope | None = None,
        sub_account_id: str | None = None,
        limit: int = 50,
        page_token: str | None = None,
    ) -> SubAccountActivityList:
        parsed_sub = parse_optional_subaccount_id(
            self._resolve_sub_account_id(sub_account_id, account=account)
        )
        if parsed_sub is None:
            raise PolyesterValidationError("sub_account_id is required")
        request = ListSubaccountEventsRequest(
            subaccount_id=parsed_sub,
            limit=validate_limit(limit),
        )
        if page_token:
            request.page_token = page_token
        return await unary_auth_decoded(
            self._transport,
            SubaccountViewServiceClient,
            lambda client, req: client.list_subaccount_activity(req),
            request,
            subaccount_activity_list_from_proto,
        )

    async def subscribe(
        self,
        *,
        account_id: str | int | None = None,
    ) -> AsyncSubscription[SubAccount]:
        return await subscribe_account_proto(
            self._realtime,
            channel_template="private:auth:subaccounts:{account_id}:proto",
            account_id=account_id,
            default_account_id=self._default_account_id,
            decode=decode_subaccount_bytes,
        )

    async def subscribe_api_keys(
        self,
        *,
        account_id: str | int | None = None,
    ) -> AsyncSubscription[ApiKeySummary]:
        return await subscribe_account_proto(
            self._realtime,
            channel_template="private:auth:api-keys:{account_id}:proto",
            account_id=account_id,
            default_account_id=self._default_account_id,
            decode=decode_api_key_bytes,
        )
