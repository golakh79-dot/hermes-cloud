from __future__ import annotations

from typing import TypeVar

from polyester.catalogs import CatalogManager
from polyester.codecs.decode.zipper import (
    deposit_withdraw_config_from_proto,
    zipped_asset_supply_batch_from_proto,
)
from polyester.gen.chain.zipper.v1.zipper_connect import ZipperServiceClient
from polyester.gen.chain.zipper.v1.zipper_pb2 import GetDepositWithdrawConfigRequest
from polyester.models.zipper import DepositWithdrawConfig, ZippedAssetSupplyBatch
from polyester.realtime.client import AsyncRealtimeClient, AsyncSubscription
from polyester.services._base import BaseService
from polyester.services._generated import unary_public_decoded
from polyester.services._realtime_subscribe import subscribe_public_proto

T = TypeVar("T")


class AsyncZipperService(BaseService):
    def __init__(
        self,
        transport,
        *,
        catalogs: CatalogManager | None = None,
        realtime: AsyncRealtimeClient | None = None,
    ) -> None:
        super().__init__(transport)
        self._catalogs = catalogs
        self._realtime = realtime

    async def get_deposit_withdraw_config(self) -> DepositWithdrawConfig:
        return await unary_public_decoded(
            self._transport,
            ZipperServiceClient,
            lambda client, request: client.get_deposit_withdraw_config(request),
            GetDepositWithdrawConfigRequest(),
            deposit_withdraw_config_from_proto,
        )

    def _decode_supply_batch(self, payload: bytes) -> ZippedAssetSupplyBatch:
        from polyester.gen.chain.zipper.v1.zipper_pb2 import ZippedAssetSupplyBatch

        msg = ZippedAssetSupplyBatch()
        msg.ParseFromString(payload)
        scale_lookup = None
        if self._catalogs is not None:
            scale_lookup = self._catalogs.quantity_scale_for_zipped_asset_id
        batch = zipped_asset_supply_batch_from_proto(
            msg,
            quantity_scale_for_zipped_asset_id=scale_lookup,
        )
        if self._catalogs is not None:
            self._catalogs.patch_zipper_supply(batch.updates)
        return batch

    async def subscribe_zipped_asset_supply(
        self,
        *,
        patch_catalog: bool = True,
    ) -> AsyncSubscription[ZippedAssetSupplyBatch]:
        decode = self._decode_supply_batch
        if not patch_catalog:

            def decode_without_patch(payload: bytes) -> ZippedAssetSupplyBatch:
                from polyester.gen.chain.zipper.v1 import zipper_pb2

                msg = zipper_pb2.ZippedAssetSupplyBatch()
                msg.ParseFromString(payload)
                scale_lookup = None
                if self._catalogs is not None:
                    scale_lookup = self._catalogs.quantity_scale_for_zipped_asset_id
                return zipped_asset_supply_batch_from_proto(
                    msg,
                    quantity_scale_for_zipped_asset_id=scale_lookup,
                )

            decode = decode_without_patch

        return await subscribe_public_proto(
            self._realtime,
            channel="public:chain:zipped-asset:supply:proto",
            decode=decode,
        )
