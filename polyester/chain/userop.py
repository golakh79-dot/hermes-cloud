"""ERC-4337 EntryPoint v0.7 Safe UserOperation helpers (Pimlico-compatible)."""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any

from eth_abi import encode
from eth_account import Account
from eth_account.messages import encode_typed_data
from eth_utils import to_checksum_address, to_hex

from polyester.chain.calldata import ChainCall
from polyester.chain.environment import POLYESTER_DEVNET_ENVIRONMENT, PolyesterChainEnvironment
from polyester.chain.rpc import JsonRpcClient
from polyester.chain.safe import predict_safe_address_with_data

USER_OPERATION_GAS_BUFFER_BPS = 2_000
USER_OPERATION_MIN_GAS_BUFFER = 50_000

_EXECUTE_USER_OP_SELECTOR = bytes.fromhex("541d63c8")  # executeUserOpWithErrorString
_GET_NONCE_SELECTOR = bytes.fromhex("35567e1a")  # getNonce(address,uint192)

_STUB_ECDSA_SIGNATURE = bytes.fromhex(
    "fffffffffffffffffffffffffffffff000000000000000000000000000000000"
    "7aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa1c"
)

EIP712_SAFE_OP_V07 = {
    "types": {
        "EIP712Domain": [
            {"name": "chainId", "type": "uint256"},
            {"name": "verifyingContract", "type": "address"},
        ],
        "SafeOp": [
            {"name": "safe", "type": "address"},
            {"name": "nonce", "type": "uint256"},
            {"name": "initCode", "type": "bytes"},
            {"name": "callData", "type": "bytes"},
            {"name": "verificationGasLimit", "type": "uint128"},
            {"name": "callGasLimit", "type": "uint128"},
            {"name": "preVerificationGas", "type": "uint256"},
            {"name": "maxPriorityFeePerGas", "type": "uint128"},
            {"name": "maxFeePerGas", "type": "uint128"},
            {"name": "paymasterAndData", "type": "bytes"},
            {"name": "validAfter", "type": "uint48"},
            {"name": "validUntil", "type": "uint48"},
            {"name": "entryPoint", "type": "address"},
        ],
    },
    "primaryType": "SafeOp",
}


@dataclass(frozen=True, slots=True)
class UserOperationReceipt:
    user_operation_hash: str
    transaction_hash: str
    success: bool
    raw: dict[str, Any]


def add_user_operation_gas_buffer(gas: int) -> int:
    percent = (gas * USER_OPERATION_GAS_BUFFER_BPS) // 10_000
    return gas + max(percent, USER_OPERATION_MIN_GAS_BUFFER)


def encode_execute_user_op_call_data(call: ChainCall) -> bytes:
    """Encode Safe4337Module.executeUserOpWithErrorString for a single call."""
    value = int(call.value or 0)
    return _EXECUTE_USER_OP_SELECTOR + encode(
        ["address", "uint256", "bytes", "uint8"],
        [bytes.fromhex(call.to[2:] if call.to.startswith("0x") else call.to), value, call.data, 0],
    )


def pack_paymaster_and_data(
    *,
    paymaster: str | None,
    paymaster_verification_gas_limit: int = 0,
    paymaster_post_op_gas_limit: int = 0,
    paymaster_data: bytes = b"",
) -> bytes:
    if not paymaster:
        return b""
    addr = bytes.fromhex(paymaster[2:] if paymaster.startswith("0x") else paymaster)
    return (
        addr
        + int(paymaster_verification_gas_limit).to_bytes(16, "big")
        + int(paymaster_post_op_gas_limit).to_bytes(16, "big")
        + paymaster_data
    )


def stub_signature() -> bytes:
    return (0).to_bytes(6, "big") + (0).to_bytes(6, "big") + _STUB_ECDSA_SIGNATURE


def sign_safe_user_operation(
    *,
    owner: Account,
    environment: PolyesterChainEnvironment,
    sender: str,
    nonce: int,
    init_code: bytes,
    call_data: bytes,
    call_gas_limit: int,
    verification_gas_limit: int,
    pre_verification_gas: int,
    max_fee_per_gas: int,
    max_priority_fee_per_gas: int,
    paymaster_and_data: bytes,
    valid_after: int = 0,
    valid_until: int = 0,
) -> bytes:
    """EIP-712 SafeOp signature packed as uint48/uint48/bytes (single EOA owner)."""
    module = environment.account_abstraction.safe.safe_4337_module_address
    typed = {
        **EIP712_SAFE_OP_V07,
        "domain": {
            "chainId": environment.chain_id,
            "verifyingContract": to_checksum_address(module),
        },
        "message": {
            "safe": to_checksum_address(sender),
            "nonce": nonce,
            "initCode": init_code,
            "callData": call_data,
            "verificationGasLimit": verification_gas_limit,
            "callGasLimit": call_gas_limit,
            "preVerificationGas": pre_verification_gas,
            "maxPriorityFeePerGas": max_priority_fee_per_gas,
            "maxFeePerGas": max_fee_per_gas,
            "paymasterAndData": paymaster_and_data,
            "validAfter": valid_after,
            "validUntil": valid_until,
            "entryPoint": to_checksum_address(environment.account_abstraction.entry_point.address),
        },
    }
    signed = owner.sign_message(encode_typed_data(full_message=typed))
    return (
        int(valid_after).to_bytes(6, "big")
        + int(valid_until).to_bytes(6, "big")
        + bytes(signed.signature)
    )


def _hex_int(value: int) -> str:
    return hex(value)


def _as_int(value: Any) -> int:
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        return int(value, 16) if value.startswith("0x") else int(value)
    raise TypeError(f"cannot convert {type(value)} to int")


class PolyesterSmartAccount:
    """Owner-key smart account: derive Safe, build/sign/submit Funding UserOps."""

    def __init__(
        self,
        *,
        owner_private_key: str,
        environment: PolyesterChainEnvironment | None = None,
        salt_nonce: int = 0,
        timeout: float = 60.0,
    ) -> None:
        key = owner_private_key if owner_private_key.startswith("0x") else f"0x{owner_private_key}"
        self._owner = Account.from_key(key)
        self.environment = environment or POLYESTER_DEVNET_ENVIRONMENT
        self.salt_nonce = salt_nonce
        predicted = predict_safe_address_with_data(
            owners=[self._owner.address],
            salt_nonce=salt_nonce,
            environment=self.environment,
        )
        self.address = predicted.address
        self.owner_address = self._owner.address
        self._initializer = predicted.initializer
        self._factory_calldata = predicted.factory_calldata
        aa = self.environment.account_abstraction
        self._rpc = JsonRpcClient(self.environment.rpc_url, timeout=timeout)
        self._bundler = JsonRpcClient(aa.bundler_url, timeout=timeout)
        self._paymaster = JsonRpcClient(aa.paymaster_url, timeout=timeout)

    def is_deployed(self) -> bool:
        code = self._rpc.request("eth_getCode", [self.address, "latest"])
        return isinstance(code, str) and code not in ("0x", "0x0", "")

    def get_nonce(self, *, key: int | None = None) -> int:
        """Return the next EntryPoint nonce.

        Matches viem/permissionless: when ``key`` is omitted, use a fresh
        timestamp-based nonce key (``Date.now()``) so ops are not stuck on
        key ``0`` (Polyester's bundler rejects some key-0 mempool submissions).
        """
        nonce_key = int(time.time() * 1000) if key is None else int(key)
        # uint192 key fits; keep within 2^192-1.
        if nonce_key < 0 or nonce_key >= (1 << 192):
            raise ValueError("nonce key out of uint192 range")
        ep = self.environment.account_abstraction.entry_point.address
        data = _GET_NONCE_SELECTOR + encode(
            ["address", "uint192"],
            [bytes.fromhex(self.address[2:]), nonce_key],
        )
        result = self._rpc.request(
            "eth_call",
            [{"to": ep, "data": to_hex(data)}, "latest"],
        )
        return int(result, 16)

    def send_calls(
        self,
        calls: list[ChainCall],
        *,
        wait: bool = True,
        receipt_timeout_s: float = 30.0,
    ) -> UserOperationReceipt | str:
        if not calls:
            raise ValueError("at least one call is required")
        if len(calls) != 1:
            raise NotImplementedError(
                "multi-call UserOps are not implemented yet; submit one ChainCall at a time"
            )
        call_data = encode_execute_user_op_call_data(calls[0])
        deployed = self.is_deployed()
        factory = None
        factory_data = None
        init_code = b""
        if not deployed:
            factory = self.environment.account_abstraction.safe.safe_proxy_factory_address
            factory_data = self._factory_calldata
            init_code = bytes.fromhex(factory[2:]) + factory_data

        nonce = self.get_nonce()
        gas_price = self._paymaster.request("pimlico_getUserOperationGasPrice", [])
        fast = gas_price["fast"]
        max_fee = _as_int(fast["maxFeePerGas"])
        max_prio = _as_int(fast["maxPriorityFeePerGas"])

        user_op: dict[str, Any] = {
            "sender": self.address,
            "nonce": _hex_int(nonce),
            "callData": to_hex(call_data),
            "callGasLimit": _hex_int(0),
            "verificationGasLimit": _hex_int(0),
            "preVerificationGas": _hex_int(0),
            "maxFeePerGas": _hex_int(max_fee),
            "maxPriorityFeePerGas": _hex_int(max_prio),
            "signature": to_hex(stub_signature()),
        }
        if factory is not None and factory_data is not None:
            user_op["factory"] = to_checksum_address(factory)
            user_op["factoryData"] = to_hex(factory_data)

        entry_point = self.environment.account_abstraction.entry_point.address

        # Sponsor once for estimates, buffer gas (incl. paymaster), then re-sponsor so
        # paymasterData matches the final limits. Polyester's paymaster often returns
        # paymasterPostOpGasLimit=1; without a floor the bundler accepts then rejects.
        sponsored = self._paymaster.request(
            "pm_sponsorUserOperation",
            [user_op, entry_point],
        )
        call_gas = add_user_operation_gas_buffer(_as_int(sponsored["callGasLimit"]))
        verification_gas = add_user_operation_gas_buffer(_as_int(sponsored["verificationGasLimit"]))
        pre_verification = add_user_operation_gas_buffer(_as_int(sponsored["preVerificationGas"]))
        pm_ver = max(
            add_user_operation_gas_buffer(
                _as_int(sponsored.get("paymasterVerificationGasLimit", 0))
            ),
            USER_OPERATION_MIN_GAS_BUFFER,
        )
        pm_post = max(
            add_user_operation_gas_buffer(_as_int(sponsored.get("paymasterPostOpGasLimit", 0))),
            USER_OPERATION_MIN_GAS_BUFFER * 2,
        )

        buffered_op = {
            **user_op,
            "callGasLimit": _hex_int(call_gas),
            "verificationGasLimit": _hex_int(verification_gas),
            "preVerificationGas": _hex_int(pre_verification),
            "paymasterVerificationGasLimit": _hex_int(pm_ver),
            "paymasterPostOpGasLimit": _hex_int(pm_post),
        }
        sponsored = self._paymaster.request(
            "pm_sponsorUserOperation",
            [buffered_op, entry_point],
        )
        # Keep the exact buffered limits we asked the paymaster to cover. Taking
        # higher sponsor-returned callGas without re-signing paymasterData causes
        # bundler accept-then-reject.
        paymaster = sponsored.get("paymaster")
        pm_data = sponsored.get("paymasterData", "0x")
        if isinstance(pm_data, str):
            pm_data_bytes = bytes.fromhex(pm_data[2:] if pm_data.startswith("0x") else pm_data)
        else:
            pm_data_bytes = b""

        paymaster_and_data = pack_paymaster_and_data(
            paymaster=paymaster,
            paymaster_verification_gas_limit=pm_ver,
            paymaster_post_op_gas_limit=pm_post,
            paymaster_data=pm_data_bytes,
        )
        signature = sign_safe_user_operation(
            owner=self._owner,
            environment=self.environment,
            sender=self.address,
            nonce=nonce,
            init_code=init_code,
            call_data=call_data,
            call_gas_limit=call_gas,
            verification_gas_limit=verification_gas,
            pre_verification_gas=pre_verification,
            max_fee_per_gas=max_fee,
            max_priority_fee_per_gas=max_prio,
            paymaster_and_data=paymaster_and_data,
        )

        final_op: dict[str, Any] = {
            "sender": self.address,
            "nonce": _hex_int(nonce),
            "callData": to_hex(call_data),
            "callGasLimit": _hex_int(call_gas),
            "verificationGasLimit": _hex_int(verification_gas),
            "preVerificationGas": _hex_int(pre_verification),
            "maxFeePerGas": _hex_int(max_fee),
            "maxPriorityFeePerGas": _hex_int(max_prio),
            "signature": to_hex(signature),
        }
        if factory is not None and factory_data is not None:
            final_op["factory"] = to_checksum_address(factory)
            final_op["factoryData"] = to_hex(factory_data)
        if paymaster:
            final_op["paymaster"] = to_checksum_address(paymaster)
            final_op["paymasterVerificationGasLimit"] = _hex_int(pm_ver)
            final_op["paymasterPostOpGasLimit"] = _hex_int(pm_post)
            final_op["paymasterData"] = to_hex(pm_data_bytes)

        user_op_hash = self._bundler.request(
            "eth_sendUserOperation",
            [final_op, entry_point],
        )
        if not wait:
            return str(user_op_hash)
        return self.wait_for_receipt(str(user_op_hash), timeout_s=receipt_timeout_s)

    def wait_for_receipt(
        self,
        user_operation_hash: str,
        *,
        timeout_s: float = 30.0,
        poll_interval_s: float = 1.0,
    ) -> UserOperationReceipt:
        deadline = time.time() + timeout_s
        while time.time() < deadline:
            raw = self._bundler.request(
                "eth_getUserOperationReceipt",
                [user_operation_hash],
            )
            if raw:
                receipt = raw.get("receipt") or {}
                success = bool(raw.get("success", receipt.get("status") in (1, "0x1", "0x01")))
                tx_hash = receipt.get("transactionHash") or raw.get("transactionHash") or ""
                return UserOperationReceipt(
                    user_operation_hash=user_operation_hash,
                    transaction_hash=str(tx_hash),
                    success=success,
                    raw=raw,
                )
            try:
                status = self._bundler.request(
                    "pimlico_getUserOperationStatus",
                    [user_operation_hash],
                )
            except Exception:
                status = None
            if isinstance(status, dict) and status.get("status") == "rejected":
                raise RuntimeError(
                    f"bundler rejected UserOperation {user_operation_hash}: {status}"
                )
            time.sleep(poll_interval_s)
        raise TimeoutError(f"timed out waiting for UserOperation receipt {user_operation_hash}")
