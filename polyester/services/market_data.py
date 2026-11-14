from __future__ import annotations

from datetime import datetime

from google.protobuf.timestamp_pb2 import Timestamp

from polyester.catalogs import CatalogManager
from polyester.codecs.decode.market_data import (
    candles_columns_from_proto,
    candles_from_proto,
    market_trades_from_proto,
)
from polyester.codecs.realtime_decode import decode_candle_point_bytes
from polyester.codecs.scalars import UINT64_MAX
from polyester.codecs.spot_config import spot_config_from_dict
from polyester.errors import PolyesterValidationError
from polyester.gen.marketdata.v1 import marketdata_pb2
from polyester.gen.marketdata.v1.marketdata_connect import MarketDataServiceClient
from polyester.gen.marketdata.v1.marketdata_pb2 import (
    GetCandlesRequest,
    GetSpotConfigRequest,
    GetTradesRequest,
)
from polyester.models import Candle, CandlesResult, MarketTradesResult, SpotConfig
from polyester.realtime.client import AsyncRealtimeClient, AsyncSubscription
from polyester.services._base import BaseService
from polyester.services._generated import unary_public, unary_public_decoded
from polyester.services._realtime_subscribe import subscribe_public_proto
from polyester.services._symbols import resolve_symbol_id
from polyester.services._validation import validate_limit

TIMEFRAME_ALIASES: dict[str, str] = {
    "1s": "SEC_1",
    "1m": "MIN_1",
    "5m": "MIN_5",
    "15m": "MIN_15",
    "30m": "MIN_30",
    "1h": "HOUR_1",
    "4h": "HOUR_4",
    "12h": "HOUR_12",
    "1d": "DAY_1",
    "1w": "WEEK_1",
    "1mo": "MONTH_1",
    "3m": "MIN_3",
    "2h": "HOUR_2",
    "6h": "HOUR_6",
    "8h": "HOUR_8",
    "3d": "DAY_3",
}

_TRADE_SIDE_FILTERS: dict[str, marketdata_pb2.SideFilter] = {
    "buy": marketdata_pb2.BUY,
    "sell": marketdata_pb2.SELL,
}
# Live Centrifugo channels use human labels (`1m`), not REST enum names (`MIN_1`).
_CHANNEL_TIMEFRAME_ALIASES: dict[str, str] = {}
for _label, _enum_name in TIMEFRAME_ALIASES.items():
    _CHANNEL_TIMEFRAME_ALIASES[_label] = _label
    _CHANNEL_TIMEFRAME_ALIASES[_enum_name] = _label
    _CHANNEL_TIMEFRAME_ALIASES[_enum_name.lower()] = _label
    _CHANNEL_TIMEFRAME_ALIASES[_enum_name.replace("_", "").lower()] = _label


class AsyncMarketDataService(BaseService):
    def __init__(
        self,
        transport,
        catalogs: CatalogManager | None = None,
        *,
        realtime: AsyncRealtimeClient | None = None,
    ) -> None:
        super().__init__(transport)
        self._catalogs = catalogs
        self._realtime = realtime

    async def get_spot_config(self) -> SpotConfig:
        data = await unary_public(
            self._transport,
            MarketDataServiceClient,
            lambda client, request: client.get_spot_config(request),
            GetSpotConfigRequest(),
        )
        return spot_config_from_dict(data)

    async def get_trades(
        self,
        *,
        symbol: str | None = None,
        symbol_id: int | None = None,
        limit: int = 100,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        side: str | None = None,
        page_token: str | None = None,
        after_trade_id: int | None = None,
    ) -> MarketTradesResult:
        """List public trades for one market.

        By default trades come newest first; ``start_time`` / ``end_time``
        (inclusive), ``side`` (``"buy"`` or ``"sell"`` aggressor) and
        ``page_token`` (the previous result's ``next_page_token``) narrow and
        page them.

        With ``after_trade_id`` the call instead walks the market's trades by
        trade ID, oldest first and gap-free, to backfill trades a live stream
        missed: pass ``0`` to start from the first trade, then the result's
        ``next_after_trade_id``. Every trade up to ``complete_through_trade_id``
        is returned; when ``next_after_trade_id`` equals the ``after_trade_id``
        you sent, nothing newer is available yet, so retry later with backoff.
        ``after_trade_id`` cannot be combined with the time range, side or
        page token.
        """
        validated_limit = validate_limit(limit)
        if after_trade_id is not None:
            if isinstance(after_trade_id, bool) or not isinstance(after_trade_id, int):
                raise PolyesterValidationError("get_trades after_trade_id must be an integer")
            if after_trade_id < 0 or after_trade_id > UINT64_MAX:
                raise PolyesterValidationError("get_trades after_trade_id exceeds uint64 range")
            if start_time is not None or end_time is not None or side or page_token:
                raise PolyesterValidationError(
                    "get_trades after_trade_id cannot be combined with "
                    "start_time, end_time, side or page_token"
                )
        resolved_symbol_id = resolve_symbol_id(
            self._catalogs,
            symbol=symbol,
            symbol_id=symbol_id,
            label="get_trades",
        )
        quantity_scale = _quantity_scale_for_symbol_id(
            self._catalogs, resolved_symbol_id, label="get_trades"
        )
        request = GetTradesRequest(symbol_id=resolved_symbol_id, limit=validated_limit)
        if start_time is not None:
            request.start_time.CopyFrom(_datetime_to_timestamp(start_time))
        if end_time is not None:
            request.end_time.CopyFrom(_datetime_to_timestamp(end_time))
        if side:
            side_key = side.lower()
            if side_key not in _TRADE_SIDE_FILTERS:
                raise PolyesterValidationError("get_trades side must be 'buy' or 'sell'")
            request.side = _TRADE_SIDE_FILTERS[side_key]
        if page_token:
            request.page_token = page_token
        if after_trade_id is not None:
            request.after_trade_id = after_trade_id
        return await unary_public_decoded(
            self._transport,
            MarketDataServiceClient,
            lambda client, req: client.get_trades(req),
            request,
            lambda msg: market_trades_from_proto(msg, quantity_scale=quantity_scale),
        )

    async def get_current_candle(
        self,
        *,
        symbol: str | None = None,
        symbol_id: int | None = None,
        timeframe: str = "1m",
    ) -> Candle | None:
        result = await self.get_candles(
            symbol=symbol,
            symbol_id=symbol_id,
            timeframe=timeframe,
            limit=1,
            include_incomplete=True,
        )
        if result.candles:
            # GetCandles rows are newest-first; an open candle is prepended.
            return result.candles[0]
        return None

    async def get_candles(
        self,
        *,
        symbol: str | None = None,
        symbol_id: int | None = None,
        timeframe: str = "1m",
        limit: int = 100,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        include_incomplete: bool = False,
        include_reference: bool = False,
    ) -> CandlesResult:
        request = _build_candles_request(
            self._catalogs,
            symbol=symbol,
            symbol_id=symbol_id,
            timeframe=timeframe,
            limit=limit,
            start_time=start_time,
            end_time=end_time,
            include_incomplete=include_incomplete,
            include_reference=include_reference,
        )
        volume_scale = _volume_scale_for_symbol_id(self._catalogs, request.symbol_id)
        reference_price_scale = _reference_price_scale_for_symbol_id(
            self._catalogs, request.symbol_id, required=include_reference
        )
        return await unary_public_decoded(
            self._transport,
            MarketDataServiceClient,
            lambda client, req: client.get_candles(req),
            request,
            lambda msg: candles_from_proto(
                msg,
                volume_scale=volume_scale,
                reference_price_scale=reference_price_scale,
            ),
        )

    async def get_candles_columns(
        self,
        *,
        symbol: str | None = None,
        symbol_id: int | None = None,
        timeframe: str = "1m",
        limit: int = 100,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        include_incomplete: bool = False,
        include_reference: bool = False,
    ) -> CandlesResult:
        request = _build_candles_request(
            self._catalogs,
            symbol=symbol,
            symbol_id=symbol_id,
            timeframe=timeframe,
            limit=limit,
            start_time=start_time,
            end_time=end_time,
            include_incomplete=include_incomplete,
            include_reference=include_reference,
        )
        volume_scale = _volume_scale_for_symbol_id(self._catalogs, request.symbol_id)
        reference_price_scale = _reference_price_scale_for_symbol_id(
            self._catalogs, request.symbol_id, required=include_reference
        )
        return await unary_public_decoded(
            self._transport,
            MarketDataServiceClient,
            lambda client, req: client.get_candles_columns(req),
            request,
            lambda msg: candles_columns_from_proto(
                msg,
                volume_scale=volume_scale,
                reference_price_scale=reference_price_scale,
            ),
        )

    def subscribe_trades(
        self,
        *,
        symbol: str | None = None,
        symbol_id: int | None = None,
    ):
        if self._realtime is None:
            from polyester.errors import PolyesterRealtimeError

            raise PolyesterRealtimeError(
                "Realtime client is not configured on this Polyester instance"
            )
        resolved_symbol_id = resolve_symbol_id(
            self._catalogs,
            symbol=symbol,
            symbol_id=symbol_id,
            label="subscribe_trades",
        )
        quantity_scale = _quantity_scale_for_symbol_id(
            self._catalogs, resolved_symbol_id, label="subscribe_trades"
        )
        return self._realtime.subscribe_market_trades(
            resolved_symbol_id, quantity_scale=quantity_scale
        )

    async def subscribe_candles(
        self,
        *,
        symbol: str | None = None,
        symbol_id: int | None = None,
        timeframe: str = "1m",
    ) -> AsyncSubscription[Candle]:
        resolved_symbol_id = resolve_symbol_id(
            self._catalogs,
            symbol=symbol,
            symbol_id=symbol_id,
            label="subscribe_candles",
        )
        channel_timeframe = _resolve_candle_channel_timeframe(timeframe)
        channel = f"public:spot:market:candles:{channel_timeframe}:{resolved_symbol_id}:proto"
        volume_scale = _volume_scale_for_symbol_id(self._catalogs, resolved_symbol_id)
        return await subscribe_public_proto(
            self._realtime,
            channel=channel,
            decode=decode_candle_point_bytes(
                symbol_id=resolved_symbol_id,
                timeframe=channel_timeframe,
                volume_scale=volume_scale,
            ),
        )


def _resolve_candle_channel_timeframe(timeframe: str) -> str:
    """Normalize user timeframe aliases to the live channel label (e.g. MIN_1 → 1m)."""
    label = _CHANNEL_TIMEFRAME_ALIASES.get(timeframe)
    if label is None:
        label = _CHANNEL_TIMEFRAME_ALIASES.get(timeframe.upper())
    if label is None:
        label = _CHANNEL_TIMEFRAME_ALIASES.get(timeframe.lower().replace("_", ""))
    if label is None:
        raise PolyesterValidationError(
            f"Unknown candle timeframe {timeframe!r}; use aliases like '1m', '1h', '1d'"
        )
    return label


def _build_candles_request(
    catalogs: CatalogManager | None,
    *,
    symbol: str | None,
    symbol_id: int | None,
    timeframe: str,
    limit: int,
    start_time: datetime | None,
    end_time: datetime | None,
    include_incomplete: bool,
    include_reference: bool = False,
) -> GetCandlesRequest:
    from polyester.gen.marketdata.v1 import marketdata_pb2

    resolved_symbol_id = resolve_symbol_id(
        catalogs,
        symbol=symbol,
        symbol_id=symbol_id,
        label="get_candles",
    )
    validated_limit = validate_limit(limit)
    timeframe_name = TIMEFRAME_ALIASES.get(timeframe, timeframe.upper())
    timeframe_enum = getattr(marketdata_pb2, timeframe_name, None)
    if timeframe_enum is None:
        raise PolyesterValidationError(
            f"Unknown candle timeframe {timeframe!r}; use aliases like '1m', '1h', '1d'"
        )

    request = GetCandlesRequest(
        symbol_id=resolved_symbol_id,
        timeframe=timeframe_enum,
        limit=validated_limit,
        include_incomplete=include_incomplete,
        include_reference=include_reference,
    )
    if start_time is not None:
        request.start_time.CopyFrom(_datetime_to_timestamp(start_time))
    if end_time is not None:
        request.end_time.CopyFrom(_datetime_to_timestamp(end_time))
    return request


def _datetime_to_timestamp(value: datetime) -> Timestamp:
    ts = Timestamp()
    ts.FromDatetime(value)
    return ts


def _volume_scale_for_symbol_id(catalogs: CatalogManager | None, symbol_id: int) -> int:
    scale = (
        catalogs.market_data_volume_scale_for_symbol_id(symbol_id) if catalogs is not None else None
    )
    if scale is None:
        raise PolyesterValidationError(
            f"candle volume requires a hydrated market_data_volume_scale for symbol_id {symbol_id}"
        )
    return scale


def _reference_price_scale_for_symbol_id(
    catalogs: CatalogManager | None, symbol_id: int, *, required: bool
) -> int | None:
    scale = (
        catalogs.reference_price_scale_for_symbol_id(symbol_id) if catalogs is not None else None
    )
    if scale is None and required:
        raise PolyesterValidationError(
            f"candle reference prices require reference_price_scale for symbol_id {symbol_id}"
        )
    return scale


def _quantity_scale_for_symbol_id(
    catalogs: CatalogManager | None, symbol_id: int, *, label: str
) -> int:
    scale = catalogs.base_quantity_scale_for_symbol_id(symbol_id) if catalogs is not None else None
    if scale is None:
        raise PolyesterValidationError(
            f"{label} requires a hydrated catalog quantity scale for symbol_id {symbol_id}"
        )
    return scale
