"""On-chain Funding / smart-account helpers (POLY-3569).

Encodes FundingAccount / TradingGateway calldata and can submit wallet-signed
UserOperations (owner key → derive Polyester Safe → bundler).

Separate from the API-key Connect surface: Trading withdraw RPCs cannot perform
Funding → external or Funding → Trading.
"""

from __future__ import annotations

from polyester.chain.calldata import (
    ChainCall,
    GuardApproval,
    encode_add_allowed_external_destinations,
    encode_add_allowed_internal_accounts,
    encode_funding_withdraw_to_chain,
    encode_initialize_guard_signer,
    encode_remove_allowed_external_destinations,
    encode_remove_allowed_internal_accounts,
    encode_rotate_guard_signer,
    encode_set_external_destination_allowlist_required,
    encode_set_internal_account_allowlist_required,
    encode_trading_gateway_deposit,
    encode_trading_gateway_deposit_to,
)
from polyester.chain.destination import (
    encode_withdraw_destination,
    encode_withdraw_destination_hex,
)
from polyester.chain.environment import (
    POLYESTER_DEVNET_ENVIRONMENT,
    POLYESTER_TESTNET_ENVIRONMENT,
    AccountAbstractionEnvironment,
    ContractsEnvironment,
    EntryPointConfig,
    PolyesterChainEnvironment,
    PolyesterEnvironment,
    SafeDeploymentConfig,
    create_polyester_environment,
    environment_from_name,
)
from polyester.chain.fees import ZipperFeeQuote, quote_zipper_fee
from polyester.chain.safe import (
    PredictedSafe,
    predict_polyester_smart_account_address,
    predict_safe_address,
    predict_safe_address_with_data,
)
from polyester.chain.userop import PolyesterSmartAccount, UserOperationReceipt

__all__ = [
    "AccountAbstractionEnvironment",
    "ChainCall",
    "ContractsEnvironment",
    "EntryPointConfig",
    "GuardApproval",
    "POLYESTER_DEVNET_ENVIRONMENT",
    "POLYESTER_TESTNET_ENVIRONMENT",
    "PolyesterChainEnvironment",
    "PolyesterEnvironment",
    "create_polyester_environment",
    "environment_from_name",
    "PolyesterSmartAccount",
    "PredictedSafe",
    "SafeDeploymentConfig",
    "UserOperationReceipt",
    "ZipperFeeQuote",
    "encode_add_allowed_external_destinations",
    "encode_add_allowed_internal_accounts",
    "encode_funding_withdraw_to_chain",
    "encode_initialize_guard_signer",
    "encode_remove_allowed_external_destinations",
    "encode_remove_allowed_internal_accounts",
    "encode_rotate_guard_signer",
    "encode_set_external_destination_allowlist_required",
    "encode_set_internal_account_allowlist_required",
    "encode_trading_gateway_deposit",
    "encode_trading_gateway_deposit_to",
    "encode_withdraw_destination",
    "encode_withdraw_destination_hex",
    "predict_polyester_smart_account_address",
    "predict_safe_address",
    "predict_safe_address_with_data",
    "quote_zipper_fee",
]
