from __future__ import annotations

import msgspec


class ZippedAssetSupplyUpdate(msgspec.Struct, kw_only=True, omit_defaults=True):
    zipped_asset_id: int
    supply: str = "0"


class ZippedAssetSupplyBatch(msgspec.Struct, kw_only=True, omit_defaults=True):
    updates: list[ZippedAssetSupplyUpdate] = msgspec.field(default_factory=list)


class ZipperTokenConfig(msgspec.Struct, kw_only=True, omit_defaults=True):
    address: str = ""
    decimals: int = 18


class ZipperAssetChainVariant(msgspec.Struct, kw_only=True, omit_defaults=True):
    zipped_asset_id: int
    chain_id: int
    is_native_asset: bool = False
    network_fee: str = "0"
    network_fee_ts_sec: int = 0
    deposit_min_amount: str = ""
    withdraw_min_amount: str = ""
    supply: str = "0"
    source_token: ZipperTokenConfig = msgspec.field(default_factory=ZipperTokenConfig)
    z_token: ZipperTokenConfig = msgspec.field(default_factory=ZipperTokenConfig)


class ZipperChainConfig(msgspec.Struct, kw_only=True, omit_defaults=True):
    chain_id: int
    code: str = ""
    name: str = ""
    native_chain_id: str = ""
    native_currency_symbol: str = ""
    explorer_url: str = ""
    icon: str = ""
    required_confirmations: int = 0
    confirmation_time_seconds: int = 0
    is_case_sensitive: bool = False
    min_address_length: int = 0
    max_address_length: int = 0


class ZipperAssetConfig(msgspec.Struct, kw_only=True, omit_defaults=True):
    asset: str = ""
    ledger_id: int = 0
    name: str = ""
    icon: str = ""
    quantity_scale: int = 18
    quantity_display_decimals: int = 0
    u_asset_id: str = ""
    variants: list[ZipperAssetChainVariant] = msgspec.field(default_factory=list)


class ZipperChainContractConfig(msgspec.Struct, kw_only=True, omit_defaults=True):
    name: str = ""
    address: str = ""
    type: str = ""
    description: str = ""
    version: int = 0


class ZipperEnrichedAssetChain(msgspec.Struct, kw_only=True, omit_defaults=True):
    chain_id: int
    code: str = ""
    name: str = ""
    native_chain_id: str = ""
    native_currency_symbol: str = ""
    explorer_url: str = ""
    icon: str = ""
    required_confirmations: int = 0
    confirmation_time_seconds: int = 0
    is_case_sensitive: bool = False
    min_address_length: int = 0
    max_address_length: int = 0
    zipped_asset_id: int = 0
    is_native_asset: bool = False
    network_fee: str = "0"
    network_fee_ts_sec: int = 0
    deposit_min_amount: str = ""
    withdraw_min_amount: str = ""
    supply: str = "0"
    source_token: ZipperTokenConfig = msgspec.field(default_factory=ZipperTokenConfig)
    z_token: ZipperTokenConfig = msgspec.field(default_factory=ZipperTokenConfig)


class ZipperEnrichedAssetConfig(msgspec.Struct, kw_only=True, omit_defaults=True):
    asset: str = ""
    ledger_id: int = 0
    name: str = ""
    icon: str = ""
    quantity_scale: int = 18
    quantity_display_decimals: int = 0
    u_asset_id: str = ""
    chains: list[ZipperEnrichedAssetChain] = msgspec.field(default_factory=list)


class DepositWithdrawConfig(msgspec.Struct, kw_only=True, omit_defaults=True):
    chains: list[ZipperChainConfig] = msgspec.field(default_factory=list)
    assets: list[ZipperAssetConfig] = msgspec.field(default_factory=list)
    contracts: list[ZipperChainContractConfig] = msgspec.field(default_factory=list)
    ts_ms: int = 0


class ZipperCatalogData(msgspec.Struct, kw_only=True, omit_defaults=True):
    chains: list[ZipperChainConfig] = msgspec.field(default_factory=list)
    assets: list[ZipperEnrichedAssetConfig] = msgspec.field(default_factory=list)
    contracts: list[ZipperChainContractConfig] = msgspec.field(default_factory=list)
    ts_ms: int = 0
