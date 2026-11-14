from __future__ import annotations

from dataclasses import dataclass, field

from google.protobuf.message import DecodeError

from polyester.auth import ApiKeyCredentials
from polyester.codecs.decode.withdraw import (
    withdraw_destination_validation_from_proto,
    withdraw_intent_from_proto,
)
from polyester.codecs.orders import parse_optional_subaccount_id
from polyester.codecs.withdraw import (
    new_trading_withdraw_nonce,
    trading_withdraw_payload_to_proto,
)
from polyester.errors import PolyesterAuthError, PolyesterValidationError
from polyester.gen.chain.withdraw.v1 import withdraw_pb2
from polyester.gen.chain.withdraw.v1.withdraw_connect import WithdrawServiceClient
from polyester.models import WithdrawDestinationValidation, WithdrawIntentResult
from polyester.services._base import BaseService
from polyester.services._generated import unary_auth_decoded
from polyester.services._scope import AccountScope, ScopedSubAccountMixin
from polyester.types.money import AssetAmount


def _u128_value(value) -> int:
    return (int(value.hi) << 64) | int(value.lo)


def _validate_prepared_request(request: withdraw_pb2.CreateTradingWithdrawRequest) -> None:
    if not request.HasField("payload"):
        raise PolyesterValidationError("prepared withdraw request is missing payload")
    if not request.payload_signature:
        raise PolyesterValidationError("prepared withdraw request is missing payload_signature")
    payload = request.payload
    if payload.action not in (withdraw_pb2.TO_FUNDING, withdraw_pb2.TO_EXTERNAL_CHAIN):
        raise PolyesterValidationError("prepared withdraw request has unknown action")
    if payload.asset_id <= 0:
        raise PolyesterValidationError("prepared withdraw request has invalid asset_id")
    if not payload.HasField("amount_e18") or _u128_value(payload.amount_e18) <= 0:
        raise PolyesterValidationError("prepared withdraw request has invalid amount_e18")
    if payload.deadline_ts_sec <= 0:
        raise PolyesterValidationError("prepared withdraw request has invalid deadline_ts_sec")
    if not payload.HasField("nonce") or _u128_value(payload.nonce) <= 0:
        raise PolyesterValidationError("prepared withdraw request has invalid nonce")
    if not payload.idempotency_key.strip():
        raise PolyesterValidationError("prepared withdraw request is missing idempotency_key")
    if payload.action == withdraw_pb2.TO_FUNDING and payload.destination_chain_id != 0:
        raise PolyesterValidationError(
            "prepared funding withdraw must have destination_chain_id=0"
        )
    if payload.action == withdraw_pb2.TO_EXTERNAL_CHAIN:
        if payload.destination_chain_id <= 0:
            raise PolyesterValidationError(
                "prepared external withdraw has invalid destination_chain_id"
            )
        if not payload.destination_address.strip():
            raise PolyesterValidationError(
                "prepared external withdraw is missing destination_address"
            )


@dataclass(frozen=True, slots=True)
class PreparedTradingWithdraw:
    """Immutable, persistable API-key-signed trading withdraw request."""

    _request_bytes: bytes = field(repr=False)

    @classmethod
    def from_request_bytes(cls, request_bytes: bytes) -> PreparedTradingWithdraw:
        if not isinstance(request_bytes, bytes):
            raise TypeError("request_bytes must be bytes")
        request = withdraw_pb2.CreateTradingWithdrawRequest()
        try:
            request.ParseFromString(request_bytes)
        except DecodeError as exc:
            raise PolyesterValidationError(
                f"invalid prepared withdraw bytes: {exc}"
            ) from exc
        _validate_prepared_request(request)
        return cls(request.SerializeToString(deterministic=True))

    @classmethod
    def _from_request(
        cls, request: withdraw_pb2.CreateTradingWithdrawRequest
    ) -> PreparedTradingWithdraw:
        _validate_prepared_request(request)
        return cls(request.SerializeToString(deterministic=True))

    def _request(self) -> withdraw_pb2.CreateTradingWithdrawRequest:
        request = withdraw_pb2.CreateTradingWithdrawRequest()
        request.ParseFromString(self._request_bytes)
        return request

    @property
    def request_bytes(self) -> bytes:
        return self._request_bytes

    @property
    def deterministic_payload_bytes(self) -> bytes:
        return self._request().payload.SerializeToString(deterministic=True)

    @property
    def payload_signature(self) -> bytes:
        return bytes(self._request().payload_signature)


class AsyncWithdrawService(ScopedSubAccountMixin, BaseService):
    """Trading withdraw intents (trading → funding or external chain)."""

    def __init__(self, transport, default_sub_account_id: str | None) -> None:
        super().__init__(transport)
        self._default_sub_account_id = default_sub_account_id

    def _credentials(self) -> ApiKeyCredentials:
        credentials = getattr(self._transport, "credentials", None)
        if credentials is None:
            raise PolyesterAuthError(
                "Preparing an API-key withdraw requires Polyester API-key credentials"
            )
        return credentials

    def _prepare_api_key(
        self,
        *,
        action: str,
        asset_id: int,
        quantity: str | AssetAmount,
        idempotency_key: str,
        destination_chain_id: int = 0,
        destination_address: str = "",
        amount_scale: int = 18,
        deadline_ts_sec: int | None = None,
        nonce: str | int | None = None,
    ) -> PreparedTradingWithdraw:
        resolved_nonce = new_trading_withdraw_nonce() if nonce is None else nonce
        payload = trading_withdraw_payload_to_proto(
            action=action,
            asset_id=asset_id,
            amount=quantity,
            idempotency_key=idempotency_key,
            destination_chain_id=destination_chain_id,
            deadline_ts_sec=deadline_ts_sec,
            nonce=resolved_nonce,
            destination_address=destination_address,
            amount_scale=amount_scale,
        )
        payload_bytes = payload.SerializeToString(deterministic=True)
        request = withdraw_pb2.CreateTradingWithdrawRequest(
            payload=payload,
            payload_signature=self._credentials().sign_payload(payload_bytes),
        )
        return PreparedTradingWithdraw._from_request(request)

    def prepare_api_key_to_funding(
        self,
        *,
        asset_id: int,
        quantity: str | AssetAmount,
        idempotency_key: str,
        destination_address: str = "",
        amount_scale: int = 18,
        deadline_ts_sec: int | None = None,
        nonce: str | int | None = None,
    ) -> PreparedTradingWithdraw:
        """Build and sign once; persist before submission or retry."""
        return self._prepare_api_key(
            action="to_funding",
            asset_id=asset_id,
            quantity=quantity,
            idempotency_key=idempotency_key,
            destination_address=destination_address,
            amount_scale=amount_scale,
            deadline_ts_sec=deadline_ts_sec,
            nonce=nonce,
        )

    def prepare_api_key_to_external_chain(
        self,
        *,
        asset_id: int,
        quantity: str | AssetAmount,
        destination_chain_id: int,
        destination_address: str,
        idempotency_key: str,
        amount_scale: int = 18,
        deadline_ts_sec: int | None = None,
        nonce: str | int | None = None,
    ) -> PreparedTradingWithdraw:
        if not destination_address.strip():
            raise PolyesterValidationError(
                "destination_address is required for external-chain withdraw"
            )
        return self._prepare_api_key(
            action="to_external_chain",
            asset_id=asset_id,
            quantity=quantity,
            idempotency_key=idempotency_key,
            destination_chain_id=destination_chain_id,
            destination_address=destination_address,
            amount_scale=amount_scale,
            deadline_ts_sec=deadline_ts_sec,
            nonce=nonce,
        )

    prepare_api_key_to_external = prepare_api_key_to_external_chain

    async def submit_prepared(
        self, prepared: PreparedTradingWithdraw
    ) -> WithdrawIntentResult:
        if not isinstance(prepared, PreparedTradingWithdraw):
            raise TypeError("prepared must be PreparedTradingWithdraw")
        return await self._create_trading_withdraw(prepared._request())

    async def create_api_key_to_funding(self, **kwargs) -> WithdrawIntentResult:
        return await self.submit_prepared(self.prepare_api_key_to_funding(**kwargs))

    async def create_api_key_to_external_chain(self, **kwargs) -> WithdrawIntentResult:
        return await self.submit_prepared(
            self.prepare_api_key_to_external_chain(**kwargs)
        )

    create_api_key_to_external = create_api_key_to_external_chain

    async def validate_destination(
        self,
        *,
        destination_chain_id: int,
        destination_address: str,
    ) -> WithdrawDestinationValidation:
        """Check one external-chain destination without creating a withdraw.

        Use for form feedback before Trading → external submission; create RPCs
        remain authoritative.
        """
        if int(destination_chain_id) <= 0:
            raise PolyesterValidationError("destination_chain_id must be non-zero")
        if not str(destination_address or "").strip():
            raise PolyesterValidationError("destination_address is required")
        request = withdraw_pb2.ValidateWithdrawDestinationRequest(
            destination_chain_id=int(destination_chain_id),
            destination_address=str(destination_address),
        )
        return await unary_auth_decoded(
            self._transport,
            WithdrawServiceClient,
            lambda client, req: client.validate_withdraw_destination(req),
            request,
            withdraw_destination_validation_from_proto,
        )

    async def create_to_funding(
        self,
        *,
        asset_id: int,
        quantity: str | AssetAmount,
        payload_signature: bytes,
        idempotency_key: str,
        nonce: str | int,
        account: AccountScope | None = None,
        sub_account_id: str | None = None,
        destination_address: str = "",
        amount_scale: int = 18,
        deadline_ts_sec: int | None = None,
    ) -> WithdrawIntentResult:
        """Move trading balance to funding via a signed withdraw intent."""
        if not payload_signature:
            raise PolyesterValidationError("payload_signature is required for trading withdraw")
        if deadline_ts_sec is None or deadline_ts_sec <= 0:
            raise PolyesterValidationError(
                "deadline_ts_sec is required when payload_signature is precomputed"
            )
        payload = trading_withdraw_payload_to_proto(
            action="to_funding",
            asset_id=asset_id,
            amount=quantity,
            idempotency_key=idempotency_key,
            deadline_ts_sec=deadline_ts_sec,
            nonce=nonce,
            destination_address=destination_address,
            amount_scale=amount_scale,
        )
        request = withdraw_pb2.CreateTradingWithdrawRequest(
            payload=payload,
            payload_signature=payload_signature,
        )
        return await self._create_trading_withdraw(request)

    async def create_to_external_chain(
        self,
        *,
        asset_id: int,
        quantity: str | AssetAmount,
        payload_signature: bytes,
        destination_chain_id: int,
        destination_address: str,
        idempotency_key: str,
        nonce: str | int,
        account: AccountScope | None = None,
        sub_account_id: str | None = None,
        amount_scale: int = 18,
        deadline_ts_sec: int | None = None,
    ) -> WithdrawIntentResult:
        if not payload_signature:
            raise PolyesterValidationError("payload_signature is required for trading withdraw")
        if deadline_ts_sec is None or deadline_ts_sec <= 0:
            raise PolyesterValidationError(
                "deadline_ts_sec is required when payload_signature is precomputed"
            )
        if not destination_address:
            raise PolyesterValidationError(
                "destination_address is required for external-chain withdraw"
            )
        payload = trading_withdraw_payload_to_proto(
            action="to_external_chain",
            asset_id=asset_id,
            amount=quantity,
            idempotency_key=idempotency_key,
            destination_chain_id=destination_chain_id,
            deadline_ts_sec=deadline_ts_sec,
            nonce=nonce,
            destination_address=destination_address,
            amount_scale=amount_scale,
        )
        request = withdraw_pb2.CreateTradingWithdrawRequest(
            payload=payload,
            payload_signature=payload_signature,
        )
        return await self._create_trading_withdraw(request)

    async def create_wallet_trading_withdraw(
        self,
        *,
        action: str,
        asset_id: int,
        amount: str | AssetAmount,
        idempotency_key: str,
        payload_signature: bytes,
        signer_wallet: str,
        account: AccountScope | None = None,
        sub_account_id: str | None = None,
        destination_chain_id: int = 0,
        deadline_ts_sec: int | None = None,
        nonce: str | int,
        destination_address: str = "",
        amount_scale: int = 18,
    ) -> WithdrawIntentResult:
        if not payload_signature:
            raise PolyesterValidationError("payload_signature is required for trading withdraw")
        if deadline_ts_sec is None or deadline_ts_sec <= 0:
            raise PolyesterValidationError(
                "deadline_ts_sec is required when payload_signature is precomputed"
            )
        payload = trading_withdraw_payload_to_proto(
            action=action,
            asset_id=asset_id,
            amount=amount,
            idempotency_key=idempotency_key,
            destination_chain_id=destination_chain_id,
            deadline_ts_sec=deadline_ts_sec,
            nonce=nonce,
            destination_address=destination_address,
            amount_scale=amount_scale,
        )
        request = withdraw_pb2.CreateWalletTradingWithdrawRequest(
            payload=payload,
            signer_wallet=signer_wallet,
            payload_signature=payload_signature,
        )
        parsed_sub = parse_optional_subaccount_id(
            self._resolve_sub_account_id(sub_account_id, account=account)
        )
        if parsed_sub is not None:
            request.subaccount_id = parsed_sub
        return await unary_auth_decoded(
            self._transport,
            WithdrawServiceClient,
            lambda client, req: client.create_wallet_trading_withdraw(req),
            request,
            withdraw_intent_from_proto,
        )

    async def _create_trading_withdraw(
        self,
        request: withdraw_pb2.CreateTradingWithdrawRequest,
    ) -> WithdrawIntentResult:
        return await unary_auth_decoded(
            self._transport,
            WithdrawServiceClient,
            lambda client, req: client.create_trading_withdraw(req),
            request,
            withdraw_intent_from_proto,
        )
