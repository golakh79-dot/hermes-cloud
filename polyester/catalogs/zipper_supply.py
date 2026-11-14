from __future__ import annotations

import time

from polyester.models.zipper import (
    ZippedAssetSupplyUpdate,
    ZipperCatalogData,
    ZipperEnrichedAssetChain,
    ZipperEnrichedAssetConfig,
)


def patch_zipper_catalog_supply(
    catalog: ZipperCatalogData,
    updates: list[ZippedAssetSupplyUpdate],
) -> ZipperCatalogData:
    if not updates:
        return catalog

    supply_by_id = {item.zipped_asset_id: item.supply for item in updates}
    changed = False
    next_assets: list[ZipperEnrichedAssetConfig] = []

    for asset in catalog.assets:
        asset_changed = False
        next_chains: list[ZipperEnrichedAssetChain] = []
        for chain in asset.chains:
            supply = supply_by_id.get(chain.zipped_asset_id)
            if supply is None or supply == chain.supply:
                next_chains.append(chain)
                continue
            asset_changed = True
            changed = True
            next_chains.append(
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
                    zipped_asset_id=chain.zipped_asset_id,
                    is_native_asset=chain.is_native_asset,
                    network_fee=chain.network_fee,
                    network_fee_ts_sec=chain.network_fee_ts_sec,
                    deposit_min_amount=chain.deposit_min_amount,
                    withdraw_min_amount=chain.withdraw_min_amount,
                    supply=supply,
                    source_token=chain.source_token,
                    z_token=chain.z_token,
                )
            )
        if asset_changed:
            next_assets.append(
                ZipperEnrichedAssetConfig(
                    asset=asset.asset,
                    ledger_id=asset.ledger_id,
                    name=asset.name,
                    icon=asset.icon,
                    quantity_scale=asset.quantity_scale,
                    quantity_display_decimals=asset.quantity_display_decimals,
                    u_asset_id=asset.u_asset_id,
                    chains=next_chains,
                )
            )
        else:
            next_assets.append(asset)

    if not changed:
        return catalog

    ts_ms = int(time.time() * 1000)
    return ZipperCatalogData(
        chains=list(catalog.chains),
        assets=next_assets,
        contracts=list(catalog.contracts),
        ts_ms=ts_ms,
    )
