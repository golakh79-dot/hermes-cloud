"""Zipper fee quoting for Funding → external withdraws."""

from __future__ import annotations

from dataclasses import dataclass

from eth_abi import encode
from eth_utils import function_signature_to_4byte_selector, to_hex

from polyester.chain.environment import POLYESTER_DEVNET_ENVIRONMENT, PolyesterChainEnvironment
from polyester.chain.rpc import JsonRpcClient
from polyester.errors import PolyesterValidationError


@dataclass(frozen=True, slots=True)
class ZipperFeeQuote:
    fee: int
    z_token_decimals: int
    fee_factory: str
    zipper_endpoint: str


def quote_zipper_fee(
    *,
    chain_id: int,
    z_token: str,
    zipper_endpoint: str,
    environment: PolyesterChainEnvironment | None = None,
    rpc: JsonRpcClient | None = None,
) -> ZipperFeeQuote:
    """Quote Zipper network fee via ``feeFactory.getFee(uint16,address)``.

    Use the returned ``fee`` (or a small buffer above it) as ``max_fee`` for
    ``encode_funding_withdraw_to_chain``.
    """
    if chain_id <= 0 or chain_id > 65_535:
        raise PolyesterValidationError("chain_id must be a uint16 > 0")
    token = z_token.strip()
    if not token.startswith("0x") or len(token) != 42:
        raise PolyesterValidationError("z_token must be a 20-byte 0x-prefixed address")
    endpoint = zipper_endpoint.strip()
    if not endpoint.startswith("0x") or len(endpoint) != 42:
        raise PolyesterValidationError("zipper_endpoint must be a 20-byte 0x-prefixed address")

    env = environment or POLYESTER_DEVNET_ENVIRONMENT
    client = rpc or JsonRpcClient(env.rpc_url)
    fee_factory_sel = function_signature_to_4byte_selector("feeFactory()")
    ff_raw = client.request(
        "eth_call",
        [{"to": endpoint, "data": to_hex(fee_factory_sel)}, "latest"],
    )
    fee_factory = "0x" + ff_raw[-40:]

    decimals_sel = function_signature_to_4byte_selector("decimals()")
    decimals_raw = client.request(
        "eth_call",
        [{"to": token, "data": to_hex(decimals_sel)}, "latest"],
    )
    decimals = int(decimals_raw, 16)

    get_fee_sel = function_signature_to_4byte_selector("getFee(uint16,address)")
    fee_raw = client.request(
        "eth_call",
        [
            {
                "to": fee_factory,
                "data": to_hex(
                    get_fee_sel
                    + encode(
                        ["uint16", "address"],
                        [chain_id, bytes.fromhex(token[2:])],
                    )
                ),
            },
            "latest",
        ],
    )
    return ZipperFeeQuote(
        fee=int(fee_raw, 16),
        z_token_decimals=decimals,
        fee_factory=fee_factory,
        zipper_endpoint=endpoint.lower(),
    )
