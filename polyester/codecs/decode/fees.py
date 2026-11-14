from __future__ import annotations

from polyester.catalogs import CatalogManager
from polyester.gen.fees.v1 import fees_pb2
from polyester.models.fees import SpotFeeRate, SpotFeeRatesList


def spot_fee_rate_from_proto(
    msg: fees_pb2.SpotFeeRate,
    catalogs: CatalogManager | None = None,
) -> SpotFeeRate:
    symbol_id = int(msg.symbol_id)
    symbol = catalogs.symbol_for_symbol_id(symbol_id) if catalogs is not None else None
    return SpotFeeRate(
        symbol_id=symbol_id,
        symbol=symbol or "",
        maker_fee_rate_percent=msg.maker_fee_rate_percent or "",
        taker_fee_rate_percent=msg.taker_fee_rate_percent or "",
        vip_tier=int(msg.vip_tier),
    )


def spot_fee_rates_list_from_proto(
    msg: fees_pb2.GetSpotFeeRatesResponse,
    catalogs: CatalogManager | None = None,
) -> SpotFeeRatesList:
    return SpotFeeRatesList(
        fee_rates=[spot_fee_rate_from_proto(item, catalogs) for item in msg.fee_rates]
    )
