from __future__ import annotations

from typing import Any

from polyester.codecs.decode.common import api_data_from_proto
from polyester.codecs.enums import resolve_proto_enum
from polyester.errors import PolyesterValidationError
from polyester.gen.chain.analytics.v1 import analytics_read_pb2
from polyester.gen.chain.analytics.v1.analytics_read_connect import ChainAnalyticsServiceClient
from polyester.models import ApiData
from polyester.services._base import BaseService
from polyester.services._generated import unary_public_decoded

_ANALYTICS_RANGE_ALIASES = {
    "1d": analytics_read_pb2.DAY_1,
    "7d": analytics_read_pb2.DAY_7,
    "30d": analytics_read_pb2.DAY_30,
    "90d": analytics_read_pb2.DAY_90,
    "180d": analytics_read_pb2.DAY_180,
    "365d": analytics_read_pb2.DAY_365,
}


def _analytics_range(value: str) -> Any:
    return resolve_proto_enum(
        analytics_read_pb2,
        value,
        aliases=_ANALYTICS_RANGE_ALIASES,
        field_name="range",
    )


class AsyncChainAnalyticsService(BaseService):
    async def get_zipped_asset_supply(
        self,
        *,
        zipped_asset_id: int,
        range: str,
        bucket: str = "",
        start_ts_sec: int = 0,
        end_ts_sec: int = 0,
    ) -> ApiData:
        request = analytics_read_pb2.GetZippedAssetSupplyRequest(
            zipped_asset_id=zipped_asset_id,
            range=_analytics_range(range),
            bucket=bucket,
            start_ts_sec=start_ts_sec,
            end_ts_sec=end_ts_sec,
        )
        return await unary_public_decoded(
            self._transport,
            ChainAnalyticsServiceClient,
            lambda client, req: client.get_zipped_asset_supply(req),
            request,
            api_data_from_proto,
        )

    async def get_zipped_asset_supply_group(
        self,
        *,
        group_id: str,
        range: str,
        bucket: str = "",
        start_ts_sec: int = 0,
        end_ts_sec: int = 0,
    ) -> ApiData:
        request = analytics_read_pb2.GetZippedAssetSupplyGroupRequest(
            group_id=group_id,
            range=_analytics_range(range),
            bucket=bucket,
            start_ts_sec=start_ts_sec,
            end_ts_sec=end_ts_sec,
        )
        return await unary_public_decoded(
            self._transport,
            ChainAnalyticsServiceClient,
            lambda client, req: client.get_zipped_asset_supply_group(req),
            request,
            api_data_from_proto,
        )

    async def get_unified_asset_balances(
        self,
        *,
        asset_id: int,
        range: str,
        bucket: str = "",
        start_ts_sec: int = 0,
        end_ts_sec: int = 0,
    ) -> ApiData:
        if asset_id <= 0:
            raise PolyesterValidationError("asset_id must be positive")
        request = analytics_read_pb2.GetUnifiedAssetBalancesRequest(
            asset_id=asset_id,
            range=_analytics_range(range),
            bucket=bucket,
            start_ts_sec=start_ts_sec,
            end_ts_sec=end_ts_sec,
        )
        return await unary_public_decoded(
            self._transport,
            ChainAnalyticsServiceClient,
            lambda client, req: client.get_unified_asset_balances(req),
            request,
            api_data_from_proto,
        )
