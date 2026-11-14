from __future__ import annotations

from typing import Any

from polyester.codecs.decode.guard_signer import (
    batch_sign_from_proto,
    create_wallet_from_proto,
    export_wallet_from_proto,
    rotate_wallet_from_proto,
    sign_protected_action_from_proto,
    status_from_proto,
)
from polyester.codecs.guard_signer import (
    protected_action_args_to_proto,
    protected_action_from_label,
)
from polyester.codecs.orders import parse_optional_subaccount_id
from polyester.gen.chain.guard.v1.guard_signer_connect import GuardSignerServiceClient
from polyester.gen.chain.guard.v1.guard_signer_pb2 import (
    BatchSignProtectedActionItem,
    BatchSignProtectedActionsRequest,
    CreateGuardSignerWalletRequest,
    ExportGuardSignerWalletRequest,
    GetGuardSignerStatusRequest,
    RotateGuardSignerWalletRequest,
    SignProtectedActionRequest,
)
from polyester.models.guard_signer import (
    BatchSignProtectedActionsResult,
    CreateGuardSignerWalletResult,
    ExportGuardSignerWalletResult,
    GuardApproval,
    GuardSignerStatus,
    RotateGuardSignerWalletResult,
)
from polyester.services._base import BaseService
from polyester.services._generated import unary_auth_decoded
from polyester.services._scope import AccountScope, ScopedSubAccountMixin


class AsyncGuardSignerService(ScopedSubAccountMixin, BaseService):
    def __init__(self, transport, default_sub_account_id: str | None) -> None:
        super().__init__(transport)
        self._default_sub_account_id = default_sub_account_id

    async def create_wallet(
        self,
        *,
        account: AccountScope | None = None,
        sub_account_id: str | None = None,
    ) -> CreateGuardSignerWalletResult:
        request = CreateGuardSignerWalletRequest()
        parsed_sub = parse_optional_subaccount_id(
            self._resolve_sub_account_id(sub_account_id, account=account)
        )
        if parsed_sub is not None:
            request.subaccount_id = parsed_sub
        return await unary_auth_decoded(
            self._transport,
            GuardSignerServiceClient,
            lambda client, req: client.create_guard_signer_wallet(req),
            request,
            create_wallet_from_proto,
        )

    async def get_status(
        self,
        *,
        account: AccountScope | None = None,
        sub_account_id: str | None = None,
    ) -> GuardSignerStatus | None:
        request = GetGuardSignerStatusRequest()
        parsed_sub = parse_optional_subaccount_id(
            self._resolve_sub_account_id(sub_account_id, account=account)
        )
        if parsed_sub is not None:
            request.subaccount_id = parsed_sub
        return await unary_auth_decoded(
            self._transport,
            GuardSignerServiceClient,
            lambda client, req: client.get_guard_signer_status(req),
            request,
            status_from_proto,
        )

    async def sign_protected_action(
        self,
        *,
        action: str,
        account: AccountScope | None = None,
        sub_account_id: str | None = None,
        external_polychain_chain_id: int | None = None,
        external_addresses: list[str] | None = None,
        internal_addresses: list[str] | None = None,
        whitelist_required: bool | None = None,
    ) -> GuardApproval | None:
        request = SignProtectedActionRequest(
            action=protected_action_from_label(action),
            args=protected_action_args_to_proto(
                external_polychain_chain_id=external_polychain_chain_id,
                external_addresses=external_addresses,
                internal_addresses=internal_addresses,
                whitelist_required=whitelist_required,
            ),
        )
        parsed_sub = parse_optional_subaccount_id(
            self._resolve_sub_account_id(sub_account_id, account=account)
        )
        if parsed_sub is not None:
            request.subaccount_id = parsed_sub
        return await unary_auth_decoded(
            self._transport,
            GuardSignerServiceClient,
            lambda client, req: client.sign_protected_action(req),
            request,
            sign_protected_action_from_proto,
        )

    async def batch_sign_protected_actions(
        self,
        *,
        actions: list[dict[str, Any]],
        account: AccountScope | None = None,
        sub_account_id: str | None = None,
    ) -> BatchSignProtectedActionsResult:
        items = []
        for item in actions:
            items.append(
                BatchSignProtectedActionItem(
                    action=protected_action_from_label(str(item["action"])),
                    args=protected_action_args_to_proto(
                        external_polychain_chain_id=item.get("external_polychain_chain_id"),
                        external_addresses=item.get("external_addresses"),
                        internal_addresses=item.get("internal_addresses"),
                        whitelist_required=item.get("whitelist_required"),
                    ),
                )
            )
        request = BatchSignProtectedActionsRequest(actions=items)
        parsed_sub = parse_optional_subaccount_id(
            self._resolve_sub_account_id(sub_account_id, account=account)
        )
        if parsed_sub is not None:
            request.subaccount_id = parsed_sub
        return await unary_auth_decoded(
            self._transport,
            GuardSignerServiceClient,
            lambda client, req: client.batch_sign_protected_actions(req),
            request,
            batch_sign_from_proto,
        )

    async def rotate_wallet(
        self,
        *,
        account: AccountScope | None = None,
        sub_account_id: str | None = None,
    ) -> RotateGuardSignerWalletResult:
        request = RotateGuardSignerWalletRequest()
        parsed_sub = parse_optional_subaccount_id(
            self._resolve_sub_account_id(sub_account_id, account=account)
        )
        if parsed_sub is not None:
            request.subaccount_id = parsed_sub
        return await unary_auth_decoded(
            self._transport,
            GuardSignerServiceClient,
            lambda client, req: client.rotate_guard_signer_wallet(req),
            request,
            rotate_wallet_from_proto,
        )

    async def export_wallet(
        self,
        *,
        account: AccountScope | None = None,
        sub_account_id: str | None = None,
    ) -> ExportGuardSignerWalletResult:
        request = ExportGuardSignerWalletRequest()
        parsed_sub = parse_optional_subaccount_id(
            self._resolve_sub_account_id(sub_account_id, account=account)
        )
        if parsed_sub is not None:
            request.subaccount_id = parsed_sub
        return await unary_auth_decoded(
            self._transport,
            GuardSignerServiceClient,
            lambda client, req: client.export_guard_signer_wallet(req),
            request,
            export_wallet_from_proto,
        )
