"""CREATE2 Polyester Safe address prediction (permissionless / TS parity)."""

from __future__ import annotations

from dataclasses import dataclass

from eth_abi import encode
from eth_hash.auto import keccak
from eth_utils import to_canonical_address, to_checksum_address

from polyester.chain._deps import require_eth_abi
from polyester.chain.environment import (
    POLYESTER_DEVNET_ENVIRONMENT,
    PolyesterChainEnvironment,
    SafeDeploymentConfig,
)

# SafeProxy creation bytecode from @safe-global/safe-contracts v1.4.1
# (must match SafeProxyFactory.proxyCreationCode on Polyester).
SAFE_PROXY_CREATION_CODE = bytes.fromhex(
    "608060405234801561001057600080fd5b506040516101e63803806101e68339818101604052602081101561003357600080fd5b"
    "8101908080519060200190929190505050600073ffffffffffffffffffffffffffffffffffffffff168173ffffffffffffffff"
    "ffffffffffffffffffffffff1614156100ca576040517f08c379a0000000000000000000000000000000000000000000000000"
    "0000000081526004018080602001828103825260228152602001806101c46022913960400191505060405180910390fd5b8060"
    "00806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffff"
    "ffffffffff1602179055505060ab806101196000396000f3fe608060405273ffffffffffffffffffffffffffffffffffffffff"
    "600054167fa619486e000000000000000000000000000000000000000000000000000000006000351415605057806000526020"
    "6000f35b3660008037600080366000845af43d6000803e60008114156070573d6000fd5b3d6000f3fea2646970667358221220"
    "03d1488ee65e08fa41e58e888a9865554c535f2c77126a82cb4c0f917f31441364736f6c63430007060033496e76616c696420"
    "73696e676c65746f6e20616464726573732070726f7669646564"
)

_SETUP_SELECTOR = bytes.fromhex("b63e800d")
_ENABLE_MODULES_SELECTOR = bytes.fromhex("8d0dc49f")
_MULTISEND_SELECTOR = bytes.fromhex("8d80ff0a")
_CREATE_PROXY_SELECTOR = bytes.fromhex("1688f0b9")


@dataclass(frozen=True, slots=True)
class PredictedSafe:
    address: str
    initializer: bytes
    factory_calldata: bytes


def _addr(value: str) -> bytes:
    return to_canonical_address(value)


def _encode_internal_tx(*, to: str, data: bytes, value: int = 0, operation: int = 0) -> bytes:
    return (
        bytes([operation])
        + _addr(to)
        + int(value).to_bytes(32, "big")
        + len(data).to_bytes(32, "big")
        + data
    )


def _encode_multi_send(txs: list[bytes]) -> bytes:
    packed = b"".join(txs)
    return _MULTISEND_SELECTOR + encode(["bytes"], [packed])


def _get_initializer(
    *,
    owners: list[str],
    threshold: int,
    safe: SafeDeploymentConfig,
) -> bytes:
    enable_modules = _ENABLE_MODULES_SELECTOR + encode(
        ["address[]"],
        [[_addr(safe.safe_4337_module_address)]],
    )
    multi_calls = [
        _encode_internal_tx(
            to=safe.safe_module_setup_address,
            data=enable_modules,
            operation=1,
        )
    ]
    multi_send_calldata = _encode_multi_send(multi_calls)
    return _SETUP_SELECTOR + encode(
        [
            "address[]",
            "uint256",
            "address",
            "bytes",
            "address",
            "address",
            "uint256",
            "address",
        ],
        [
            [_addr(o) for o in owners],
            threshold,
            _addr(safe.multi_send_address),
            multi_send_calldata,
            _addr(safe.safe_4337_module_address),
            bytes(20),
            0,
            bytes(20),
        ],
    )


def _create2_address(*, factory: str, salt: bytes, init_code_hash: bytes) -> str:
    # keccak256(0xff ++ factory ++ salt ++ keccak256(deploymentCode))[12:]
    raw = keccak(b"\xff" + _addr(factory) + salt + init_code_hash)
    return to_checksum_address(raw[-20:])


def predict_safe_address_with_data(
    *,
    owners: list[str],
    salt_nonce: int = 0,
    threshold: int | None = None,
    safe: SafeDeploymentConfig | None = None,
    environment: PolyesterChainEnvironment | None = None,
) -> PredictedSafe:
    """Deterministic CREATE2 Safe address + factory deploy data (zero RPC)."""
    require_eth_abi()
    if not owners:
        raise ValueError("owners must be non-empty")
    env = environment or POLYESTER_DEVNET_ENVIRONMENT
    cfg = safe or env.account_abstraction.safe
    owners_cs = [to_checksum_address(o) for o in owners]
    thresh = threshold if threshold is not None else len(owners_cs)
    initializer = _get_initializer(owners=owners_cs, threshold=thresh, safe=cfg)
    factory_calldata = _CREATE_PROXY_SELECTOR + encode(
        ["address", "bytes", "uint256"],
        [_addr(cfg.safe_singleton_address), initializer, salt_nonce],
    )
    deployment_code = SAFE_PROXY_CREATION_CODE + int.from_bytes(
        _addr(cfg.safe_singleton_address), "big"
    ).to_bytes(32, "big")
    salt = keccak(keccak(initializer) + int(salt_nonce).to_bytes(32, "big"))
    address = _create2_address(
        factory=cfg.safe_proxy_factory_address,
        salt=salt,
        init_code_hash=keccak(deployment_code),
    )
    return PredictedSafe(
        address=address,
        initializer=initializer,
        factory_calldata=factory_calldata,
    )


def predict_safe_address(
    *,
    owner_address: str,
    salt_nonce: int = 0,
    environment: PolyesterChainEnvironment | None = None,
) -> str:
    """Predict the Polyester Safe for a single owner (main account = salt 0)."""
    return predict_safe_address_with_data(
        owners=[owner_address],
        salt_nonce=salt_nonce,
        environment=environment,
    ).address


def predict_polyester_smart_account_address(
    *,
    owner_address: str,
    salt_nonce: int = 0,
    environment: PolyesterChainEnvironment | None = None,
) -> str:
    """Alias matching the TypeScript ``predictPolyesterSmartAccountAddress`` name."""
    return predict_safe_address(
        owner_address=owner_address,
        salt_nonce=salt_nonce,
        environment=environment,
    )
