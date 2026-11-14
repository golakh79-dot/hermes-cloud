"""ABI calldata encoders matching TypeScript polyester-features chain-actions.

Reference:
- fabric-apps/packages/polyester-features/src/contracts/trading-gateway-abi.ts
- fabric-apps/packages/polyester-features/src/contracts/funding-account-abi.ts
- fabric-apps/packages/polyester-features/src/chain-actions/funding-account.ts
"""

from __future__ import annotations

from dataclasses import dataclass

from polyester.chain._deps import require_eth_abi
from polyester.errors import PolyesterValidationError


@dataclass(frozen=True, slots=True)
class ChainCall:
    """Contract call payload for a smart-account UserOperation."""

    to: str
    data: bytes
    value: int = 0


@dataclass(frozen=True, slots=True)
class GuardApproval:
    """Guard approval tuple ``(uint192 nonceSpace, uint256 deadline, bytes signature)``."""

    nonce_space: int = 0
    deadline: int = 0
    signature: bytes = b""


def _normalize_address(value: str, *, field: str) -> str:
    addr = value.strip()
    if not addr.startswith("0x") or len(addr) != 42:
        raise PolyesterValidationError(f"{field} must be a 20-byte 0x-prefixed address")
    try:
        int(addr[2:], 16)
    except ValueError as exc:
        raise PolyesterValidationError(f"{field} is not a valid hex address") from exc
    return addr.lower()


def _normalize_bytes32(value: str | bytes, *, field: str) -> bytes:
    if isinstance(value, bytes):
        raw = value
    else:
        text = value.strip()
        if text.startswith("0x"):
            text = text[2:]
        if len(text) != 64:
            raise PolyesterValidationError(f"{field} must be 32 bytes (64 hex chars)")
        try:
            raw = bytes.fromhex(text)
        except ValueError as exc:
            raise PolyesterValidationError(f"{field} is not valid hex") from exc
    if len(raw) != 32:
        raise PolyesterValidationError(f"{field} must be exactly 32 bytes")
    return raw


def _parse_bytes(value: bytes | str, *, field: str) -> bytes:
    if isinstance(value, bytes):
        return value
    text = value.strip()
    if text.startswith("0x"):
        text = text[2:]
    try:
        return bytes.fromhex(text)
    except ValueError as exc:
        raise PolyesterValidationError(f"{field} is not valid hex") from exc


def _encode(signature: str, types: list[str], args: list[object]) -> bytes:
    require_eth_abi()
    from eth_abi import encode
    from eth_utils import function_signature_to_4byte_selector

    selector = function_signature_to_4byte_selector(signature)
    return selector + encode(types, args)


def encode_trading_gateway_deposit(
    *,
    trading_gateway: str,
    u_asset_id: str | bytes,
    quantity_scaled: int,
) -> ChainCall:
    """Encode ``TradingGateway.deposit(bytes32 uAssetId, uint256 uAmount)``.

    Funding → Trading for the caller's own smart account.
    """
    if quantity_scaled <= 0:
        raise PolyesterValidationError("quantity_scaled must be > 0")
    to = _normalize_address(trading_gateway, field="trading_gateway")
    asset = _normalize_bytes32(u_asset_id, field="u_asset_id")
    data = _encode(
        "deposit(bytes32,uint256)",
        ["bytes32", "uint256"],
        [asset, quantity_scaled],
    )
    return ChainCall(to=to, data=data, value=0)


def encode_trading_gateway_deposit_to(
    *,
    trading_gateway: str,
    to_account: str,
    u_asset_id: str | bytes,
    quantity_scaled: int,
) -> ChainCall:
    """Encode ``TradingGateway.depositTo(address,bytes32,uint256)``."""
    if quantity_scaled <= 0:
        raise PolyesterValidationError("quantity_scaled must be > 0")
    to = _normalize_address(trading_gateway, field="trading_gateway")
    account = _normalize_address(to_account, field="to_account")
    asset = _normalize_bytes32(u_asset_id, field="u_asset_id")
    data = _encode(
        "depositTo(address,bytes32,uint256)",
        ["address", "bytes32", "uint256"],
        [account, asset, quantity_scaled],
    )
    return ChainCall(to=to, data=data, value=0)


def encode_funding_withdraw_to_chain(
    *,
    funding_account: str,
    chain_id: int,
    z_token: str,
    withdraw_destination: bytes | str,
    z_amount: int,
    max_fee: int,
) -> ChainCall:
    """Encode ``FundingAccount.withdrawToChain((uint16,address,bytes,uint256,uint256))``.

    Funding → external chain withdraw. Destination bytes must already be encoded
    for the target chain (same as TS ``encodeWithdrawDestinationForChain``).
    """
    if chain_id <= 0 or chain_id > 65_535:
        raise PolyesterValidationError("chain_id must be a uint16 > 0")
    if z_amount <= 0:
        raise PolyesterValidationError("z_amount must be > 0")
    if max_fee < 0:
        raise PolyesterValidationError("max_fee must be >= 0")
    if z_amount <= max_fee:
        raise PolyesterValidationError("z_amount must be greater than max_fee")

    to = _normalize_address(funding_account, field="funding_account")
    token = _normalize_address(z_token, field="z_token")
    destination = _parse_bytes(withdraw_destination, field="withdraw_destination")
    if not destination:
        raise PolyesterValidationError("withdraw_destination must not be empty")

    # tuple components match FUNDING_ACCOUNT_WITHDRAW_TO_CHAIN_ABI (uint16 chainId)
    data = _encode(
        "withdrawToChain((uint16,address,bytes,uint256,uint256))",
        ["(uint16,address,bytes,uint256,uint256)"],
        [(chain_id, token, destination, z_amount, max_fee)],
    )
    return ChainCall(to=to, data=data, value=0)


def _guard_tuple(approval: GuardApproval | None) -> tuple[int, int, bytes]:
    guard = approval or GuardApproval()
    if guard.nonce_space < 0:
        raise PolyesterValidationError("approval.nonce_space must be >= 0")
    if guard.deadline < 0:
        raise PolyesterValidationError("approval.deadline must be >= 0")
    return (guard.nonce_space, guard.deadline, guard.signature or b"")


def encode_set_external_destination_allowlist_required(
    *,
    funding_account: str,
    required: bool,
    approval: GuardApproval | None = None,
) -> ChainCall:
    """Encode ``setExternalDestinationAllowlistRequired(bool,(uint192,uint256,bytes))``.

    When ``required`` is true, ``approval`` may be omitted (empty guard tuple).
    When ``required`` is false, pass a real Guard approval.
    """
    to = _normalize_address(funding_account, field="funding_account")
    data = _encode(
        "setExternalDestinationAllowlistRequired(bool,(uint192,uint256,bytes))",
        ["bool", "(uint192,uint256,bytes)"],
        [required, _guard_tuple(approval)],
    )
    return ChainCall(to=to, data=data, value=0)


def encode_set_internal_account_allowlist_required(
    *,
    funding_account: str,
    required: bool,
    approval: GuardApproval | None = None,
) -> ChainCall:
    """Encode ``setInternalAccountAllowlistRequired(bool,(uint192,uint256,bytes))``."""
    to = _normalize_address(funding_account, field="funding_account")
    data = _encode(
        "setInternalAccountAllowlistRequired(bool,(uint192,uint256,bytes))",
        ["bool", "(uint192,uint256,bytes)"],
        [required, _guard_tuple(approval)],
    )
    return ChainCall(to=to, data=data, value=0)


def encode_add_allowed_external_destinations(
    *,
    funding_account: str,
    chain_id: int,
    destinations: list[bytes | str],
    approval: GuardApproval | None = None,
) -> ChainCall:
    """Encode ``addAllowedExternalDestinations(uint16,bytes[],(uint192,uint256,bytes))``."""
    return _encode_external_destinations(
        "addAllowedExternalDestinations(uint16,bytes[],(uint192,uint256,bytes))",
        funding_account=funding_account,
        chain_id=chain_id,
        destinations=destinations,
        approval=approval,
    )


def encode_remove_allowed_external_destinations(
    *,
    funding_account: str,
    chain_id: int,
    destinations: list[bytes | str],
    approval: GuardApproval | None = None,
) -> ChainCall:
    """Encode ``removeAllowedExternalDestinations(uint16,bytes[],(uint192,uint256,bytes))``."""
    return _encode_external_destinations(
        "removeAllowedExternalDestinations(uint16,bytes[],(uint192,uint256,bytes))",
        funding_account=funding_account,
        chain_id=chain_id,
        destinations=destinations,
        approval=approval,
    )


def _encode_external_destinations(
    signature: str,
    *,
    funding_account: str,
    chain_id: int,
    destinations: list[bytes | str],
    approval: GuardApproval | None,
) -> ChainCall:
    if chain_id <= 0 or chain_id > 65_535:
        raise PolyesterValidationError("chain_id must be a uint16 > 0")
    if not destinations:
        raise PolyesterValidationError("destinations must be non-empty")
    to = _normalize_address(funding_account, field="funding_account")
    dest_bytes = [_parse_bytes(d, field="destinations") for d in destinations]
    if any(len(d) == 0 for d in dest_bytes):
        raise PolyesterValidationError("destinations entries must not be empty")
    data = _encode(
        signature,
        ["uint16", "bytes[]", "(uint192,uint256,bytes)"],
        [chain_id, dest_bytes, _guard_tuple(approval)],
    )
    return ChainCall(to=to, data=data, value=0)


def encode_add_allowed_internal_accounts(
    *,
    funding_account: str,
    accounts: list[str],
    approval: GuardApproval | None = None,
) -> ChainCall:
    """Encode ``addAllowedInternalAccounts(address[],(uint192,uint256,bytes))``."""
    return _encode_internal_accounts(
        "addAllowedInternalAccounts(address[],(uint192,uint256,bytes))",
        funding_account=funding_account,
        accounts=accounts,
        approval=approval,
    )


def encode_remove_allowed_internal_accounts(
    *,
    funding_account: str,
    accounts: list[str],
    approval: GuardApproval | None = None,
) -> ChainCall:
    """Encode ``removeAllowedInternalAccounts(address[],(uint192,uint256,bytes))``."""
    return _encode_internal_accounts(
        "removeAllowedInternalAccounts(address[],(uint192,uint256,bytes))",
        funding_account=funding_account,
        accounts=accounts,
        approval=approval,
    )


def _encode_internal_accounts(
    signature: str,
    *,
    funding_account: str,
    accounts: list[str],
    approval: GuardApproval | None,
) -> ChainCall:
    if not accounts:
        raise PolyesterValidationError("accounts must be non-empty")
    to = _normalize_address(funding_account, field="funding_account")
    addrs = [_normalize_address(a, field="accounts") for a in accounts]
    data = _encode(
        signature,
        ["address[]", "(uint192,uint256,bytes)"],
        [addrs, _guard_tuple(approval)],
    )
    return ChainCall(to=to, data=data, value=0)


def encode_initialize_guard_signer(*, guard_registry: str, signer: str) -> ChainCall:
    """Encode ``GuardRegistry.initializeSigner(address)``."""
    to = _normalize_address(guard_registry, field="guard_registry")
    signer_addr = _normalize_address(signer, field="signer")
    data = _encode("initializeSigner(address)", ["address"], [signer_addr])
    return ChainCall(to=to, data=data, value=0)


def encode_rotate_guard_signer(
    *,
    guard_registry: str,
    new_signer: str,
    approval: GuardApproval | None = None,
) -> ChainCall:
    """Encode ``GuardRegistry.rotateSigner(address,(uint192,uint256,bytes))``."""
    to = _normalize_address(guard_registry, field="guard_registry")
    signer_addr = _normalize_address(new_signer, field="new_signer")
    data = _encode(
        "rotateSigner(address,(uint192,uint256,bytes))",
        ["address", "(uint192,uint256,bytes)"],
        [signer_addr, _guard_tuple(approval)],
    )
    return ChainCall(to=to, data=data, value=0)
