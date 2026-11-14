from __future__ import annotations

import msgspec


class SpotFeeRate(msgspec.Struct, kw_only=True, omit_defaults=True):
    """Effective maker/taker rates for one spot market and account target."""

    symbol_id: int = 0
    symbol: str = ""
    maker_fee_rate_percent: str = ""
    taker_fee_rate_percent: str = ""
    vip_tier: int = 0


class SpotFeeRatesList(msgspec.Struct, kw_only=True, omit_defaults=True):
    """Effective spot fee rows ordered by numeric market identifier."""

    fee_rates: list[SpotFeeRate]
