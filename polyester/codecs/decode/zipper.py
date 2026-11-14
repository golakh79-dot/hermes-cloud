from __future__ import annotations

from collections.abc import Callable

from polyester.codecs.ledger_amounts import format_ledger_u128
from polyester.errors import PolyesterValidationError
from polyester.gen.chain.zipper.v1 import zipper_pb2
from polyester.models.zipper import (
    DepositWithdrawConfig,
    ZippedAssetSupplyBatch,
    ZippedAssetSupplyUpdate,
    ZipperAssetChainVariant,
    ZipperAssetConfig,
    ZipperChainConfig,
    ZipperChainContractConfig,
    ZipperTokenConfig,
)


def _token_config(address: str, decimals: int) -> ZipperTokenConfig:
    return ZipperTokenConfig(
        address=address or "",
        decimals=int(decimals) if decimals else 18,
    )


def _variant_from_proto(
    msg: zipper_pb2.AssetChainVariant,
    *,
    quantity_scale: int,
) -> ZipperAssetChainVariant:
    return ZipperAssetChainVariant(
        zipped_asset_id=int(msg.zipped_asset_id),
        chain_id=int(msg.chain_id),
        is_native_asset=bool(msg.is_native_asset),
        network_fee=msg.network_fee or "0",
        network_fee_ts_sec=0,
        deposit_min_amount=msg.deposit_min_amount or "",
        withdraw_min_amount=msg.withdraw_min_amount or "",
        supply=format_ledger_u128(msg.supply_q, scale=quantity_scale),
        source_token=_token_config(msg.source_address, msg.source_decimals),
        z_token=_token_config(msg.ztoken_address, msg.ztoken_decimals),
    )


def deposit_withdraw_config_from_proto(
    msg: zipper_pb2.GetDepositWithdrawConfigResponse,
) -> DepositWithdrawConfig:
    chains = [
        ZipperChainConfig(
            chain_id=int(item.chain_id),
            code=item.code,
            name=item.name,
            native_chain_id=item.native_chain_id,
            native_currency_symbol=item.native_currency_symbol,
            explorer_url=item.explorer_url,
            icon=item.icon,
            required_confirmations=int(item.required_confirmations),
            confirmation_time_seconds=int(item.confirmation_time_seconds),
            is_case_sensitive=bool(item.is_case_sensitive),
            min_address_length=int(item.min_address_length),
            max_address_length=int(item.max_address_length),
        )
        for item in msg.chains
    ]
    assets = [
        ZipperAssetConfig(
            asset=item.asset,
            ledger_id=int(item.ledger_id),
            name=item.name,
            icon=item.icon,
            quantity_scale=int(item.quantity_scale),
            quantity_display_decimals=int(item.quantity_display_decimals),
            u_asset_id=item.u_asset_id,
            variants=[
                _variant_from_proto(variant, quantity_scale=int(item.quantity_scale))
                for variant in item.variants
            ],
        )
        for item in msg.assets
    ]
    contracts = [
        ZipperChainContractConfig(
            name=item.name,
            address=item.address,
            type=item.type,
            description=item.description,
            version=int(item.version),
        )
        for item in msg.contracts
    ]
    ts_ms = int(msg.ts_sec) * 1000 if msg.ts_sec else 0
    return DepositWithdrawConfig(
        chains=chains,
        assets=assets,
        contracts=contracts,
        ts_ms=ts_ms,
    )


def zipped_asset_supply_batch_from_proto(
    msg: zipper_pb2.ZippedAssetSupplyBatch,
    *,
    quantity_scale_for_zipped_asset_id: Callable[[int], int | None] | None = None,
) -> ZippedAssetSupplyBatch:
    if quantity_scale_for_zipped_asset_id is None:
        raise PolyesterValidationError(
            "zipped asset supply decoding requires a hydrated catalog scale"
        )
    updates: list[ZippedAssetSupplyUpdate] = []
    for item in msg.updates:
        scale = quantity_scale_for_zipped_asset_id(int(item.zipped_asset_id))
        if scale is None:
            raise PolyesterValidationError(
                f"unknown quantity scale for zipped_asset_id {int(item.zipped_asset_id)}"
            )
        updates.append(
            ZippedAssetSupplyUpdate(
                zipped_asset_id=int(item.zipped_asset_id),
                supply=format_ledger_u128(item.supply_q, scale=scale),
            )
        )
    return ZippedAssetSupplyBatch(updates=updates)
