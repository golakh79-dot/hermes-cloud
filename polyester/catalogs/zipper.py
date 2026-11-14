from __future__ import annotations

from polyester.models.zipper import (
    DepositWithdrawConfig,
    ZipperAssetConfig,
    ZipperCatalogData,
    ZipperChainConfig,
    ZipperEnrichedAssetChain,
    ZipperEnrichedAssetConfig,
)


def build_zipper_catalog_data(config: DepositWithdrawConfig) -> ZipperCatalogData:
    chains_by_id = {chain.chain_id: chain for chain in config.chains}
    enriched_assets: list[ZipperEnrichedAssetConfig] = []
    for asset in config.assets:
        enriched_assets.append(
            ZipperEnrichedAssetConfig(
                asset=asset.asset,
                ledger_id=asset.ledger_id,
                name=asset.name,
                icon=asset.icon,
                quantity_scale=asset.quantity_scale,
                quantity_display_decimals=asset.quantity_display_decimals,
                u_asset_id=asset.u_asset_id,
                chains=_enrich_asset_chains(asset, chains_by_id),
            )
        )
    return ZipperCatalogData(
        chains=list(config.chains),
        assets=enriched_assets,
        contracts=list(config.contracts),
        ts_ms=config.ts_ms,
    )


def _enrich_asset_chains(
    asset: ZipperAssetConfig,
    chains_by_id: dict[int, ZipperChainConfig],
) -> list[ZipperEnrichedAssetChain]:
    enriched: list[ZipperEnrichedAssetChain] = []
    for variant in asset.variants:
        chain = chains_by_id.get(variant.chain_id)
        if chain is None:
            continue
        enriched.append(
            ZipperEnrichedAssetChain(
                chain_id=chain.chain_id,
                code=chain.code,
                name=chain.name,
                native_chain_id=chain.native_chain_id,
                native_currency_symbol=chain.native_currency_symbol,
                explorer_url=chain.explorer_url,
                icon=chain.icon,
                required_confirmations=chain.required_confirmations,
                confirmation_time_seconds=chain.confirmation_time_seconds,
                is_case_sensitive=chain.is_case_sensitive,
                min_address_length=chain.min_address_length,
                max_address_length=chain.max_address_length,
                zipped_asset_id=variant.zipped_asset_id,
                is_native_asset=variant.is_native_asset,
                network_fee=variant.network_fee,
                network_fee_ts_sec=variant.network_fee_ts_sec,
                deposit_min_amount=variant.deposit_min_amount,
                withdraw_min_amount=variant.withdraw_min_amount,
                supply=variant.supply,
                source_token=variant.source_token,
                z_token=variant.z_token,
            )
        )
    return enriched
