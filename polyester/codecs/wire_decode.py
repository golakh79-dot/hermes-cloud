from __future__ import annotations

from typing import Any

from polyester.codecs.decode.invariants import (
    ts_ns_from_response,
    ts_ns_string_from_response,
)
from polyester.codecs.decode.lifecycle import lifecycle_reason_from_code
from polyester.codecs.decode.market_data import _decode_price_field, _decode_volume_field
from polyester.codecs.scalars import format_id
from polyester.gen.chain.zipper.v1 import reason_pb2
from polyester.models.market import (
    Candle,
    CandlesResult,
    MarketOverviewEntry,
    MarketOverviewList,
    MarketTrade,
)
from polyester.models.trading import (
    ApiKeysList,
    ApiKeySummary,
    AssetBalance,
    BalanceHistory,
    BalanceHistorySeries,
    BalancesList,
    BatchReplaceAdmissionItem,
    BatchReplaceOrdersResult,
    BatchReplaceStatusItem,
    BatchReplaceStatusResult,
    BucketTransferResult,
    CancelAllOrdersResult,
    DepositAddress,
    DepositAddressesList,
    EquityHistory,
    EquityHistorySeries,
    GetOrderResult,
    Hold,
    HoldsList,
    InternalTransferResult,
    LedgerTransfer,
    LifecycleFlowsList,
    LifecycleFlowSummary,
    ModifyOrderResult,
    Order,
    OrderMutationResult,
    OrdersList,
    ResolvedAccount,
    ResolvedAccountsList,
    TransferDestination,
    TransferDestinationsList,
    TransferSide,
    TransfersList,
    Trigger,
    TriggerEvent,
    TriggerEventsList,
    TriggerMutationResult,
    TriggersList,
    UserTrade,
    UserTradesList,
    WithdrawIntentResult,
    ZipperReasonDetails,
)


def _field(data: dict[str, Any], *keys: str, default: Any = None) -> Any:
    for key in keys:
        if key in data:
            return data[key]
    return default


def _optional_scaled_field(data: dict[str, Any], *keys: str) -> str | None:
    for key in keys:
        if key in data and data[key] is not None and data[key] != "":
            return str(data[key])
    return None


_WIRE_ENUM_PREFIXES = (
    "SIDE_",
    "ORDER_TYPE_",
    "ORDER_STATUS_",
    "TIF_",
    "FLOW_STEP_",
    "FLOW_KIND_",
    "KIND_",
    "TIME_IN_FORCE_",
)


def _enum_name(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        name = value.strip()
        if not name:
            return ""
        for prefix in _WIRE_ENUM_PREFIXES:
            if name.startswith(prefix):
                return name[len(prefix) :].lower()
        # Already-normalized snake labels stay as-is; other SCREAMING names lower.
        if name == name.lower():
            return name
        return name.lower()
    return str(value)


def _id_str(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    try:
        return format_id(int(value))
    except (TypeError, ValueError):
        return str(value)


def decode_order(data: dict[str, Any]) -> Order:
    from polyester.types.money import Price, Quantity

    symbol_id = int(_field(data, "symbolId", "symbol_id", default=0) or 0)

    def _qty(raw: Any) -> Quantity | None:
        if raw is None or raw == "":
            return None
        return Quantity.from_scaled(int(raw), symbol_id=symbol_id)

    def _price(raw: Any) -> Price | None:
        if raw is None or raw == "" or int(raw) == 0:
            return None
        return Price.from_ticks(int(raw))

    return Order(
        order_id=_id_str(_field(data, "orderId", "order_id")),
        symbol_id=symbol_id,
        client_order_id=str(_field(data, "clientOrderId", "client_order_id", default="") or ""),
        side=_enum_name(_field(data, "side")).lower(),
        status=_enum_name(_field(data, "status")),
        order_type=_enum_name(_field(data, "orderType", "order_type")).lower(),
        tif=_enum_name(_field(data, "tif")).lower(),
        orig_qty=_qty(_field(data, "origQty", "orig_qty", default="") or 0),
        cum_qty=_qty(_field(data, "cumQty", "cum_qty", default="") or 0),
        leaves_qty=_qty(_field(data, "leavesQty", "leaves_qty", default="") or 0),
        price=_price(_field(data, "priceTicks", "price_ticks", default=0) or 0),
        avg_px=_price(_field(data, "avgPxTicks", "avg_px_ticks", default=0) or 0),
        created_ts_ns=ts_ns_string_from_response(
            _field(data, "createdTsNs", "created_ts_ns", default=0) or 0,
            context="Order",
            field_name="created_ts_ns",
            empty_when_zero=True,
        ),
        version=int(_field(data, "version", default=0) or 0),
    )


def decode_orders_list(data: dict[str, Any]) -> OrdersList:
    orders = [
        decode_order(item)
        for item in _field(data, "orders", default=[]) or []
        if isinstance(item, dict)
    ]
    return OrdersList(
        orders=orders,
        next_page_token=str(_field(data, "nextPageToken", "next_page_token", default="") or ""),
    )


def decode_order_mutation(data: dict[str, Any]) -> OrderMutationResult:
    return OrderMutationResult(
        status=str(_field(data, "status", default="") or ""),
        order_id=_id_str(_field(data, "orderId", "order_id")),
        client_order_id=str(_field(data, "clientOrderId", "client_order_id", default="") or ""),
    )


def decode_get_order(data: dict[str, Any]) -> GetOrderResult:
    order_raw = _field(data, "order")
    order = decode_order(order_raw) if isinstance(order_raw, dict) else None
    trades = [
        decode_user_trade(item)
        for item in _field(data, "trades", default=[]) or []
        if isinstance(item, dict)
    ]
    return GetOrderResult(order=order, trades=trades)


def decode_user_trade(data: dict[str, Any]) -> UserTrade:
    from polyester.types.money import Price, Quantity

    symbol_id = int(_field(data, "symbolId", "symbol_id", default=0) or 0)
    qty_raw = _field(data, "qtyScaled", "qty_scaled", default=0) or 0
    price_raw = _field(data, "priceTicks", "price_ticks", default=0) or 0
    return UserTrade(
        symbol_id=symbol_id,
        match_id=str(_field(data, "matchId", "match_id", default="") or ""),
        order_id=_id_str(_field(data, "orderId", "order_id")),
        side=_enum_name(_field(data, "side")).lower(),
        is_maker=bool(_field(data, "isMaker", "is_maker", default=False)),
        price=Price.from_ticks(int(price_raw)) if int(price_raw) else None,
        qty=Quantity.from_scaled(int(qty_raw), symbol_id=symbol_id),
        fee_amount_e18=_u128_str(_field(data, "feeAmountE18", "fee_amount_e18")),
        fee_asset=_enum_name(_field(data, "feeAsset", "fee_asset", default="")).lower(),
        referral_share_amount_e18=_u128_str(
            _field(data, "referralShareAmountE18", "referral_share_amount_e18")
        ),
        ts_ns=ts_ns_string_from_response(
            _field(data, "tsNs", "ts_ns", default=0) or 0,
            context="UserTrade",
            empty_when_zero=True,
        ),
        fee_is_rebate=bool(_field(data, "feeIsRebate", "fee_is_rebate", default=False)),
    )


def decode_user_trades_list(data: dict[str, Any]) -> UserTradesList:
    trades = [
        decode_user_trade(item)
        for item in _field(data, "trades", default=[]) or []
        if isinstance(item, dict)
    ]
    return UserTradesList(
        trades=trades,
        next_page_token=str(_field(data, "nextPageToken", "next_page_token", default="") or ""),
    )


def decode_market_trade(data: dict[str, Any], *, quantity_scale: int) -> MarketTrade:
    from polyester.types.money import Price, Quantity

    symbol_id = int(_field(data, "symbolId", "symbol_id", default=0) or 0)
    qty_raw = _field(data, "qtyScaled", "qty_scaled", default=0) or 0
    price_raw = _field(data, "priceTicks", "price_ticks", default=0) or 0
    return MarketTrade(
        symbol_id=symbol_id,
        match_id=str(_field(data, "matchId", "match_id", default="") or ""),
        is_buy=bool(_field(data, "isBuy", "is_buy", default=False)),
        price=Price.from_ticks(int(price_raw)) if int(price_raw) else None,
        qty=Quantity.from_scaled(int(qty_raw), scale=quantity_scale, symbol_id=symbol_id),
        ts_ns=ts_ns_string_from_response(
            _field(data, "tsNs", "ts_ns", default=0) or 0,
            context="MarketTrade",
            empty_when_zero=True,
        ),
    )


def decode_candle(data: dict[str, Any], *, volume_scale: int) -> Candle:
    return Candle(
        ts_sec=int(_field(data, "tsSec", "ts_sec", default=0) or 0),
        open=_decode_price_field(_field(data, "open", default="") or ""),
        high=_decode_price_field(_field(data, "high", default="") or ""),
        low=_decode_price_field(_field(data, "low", default="") or ""),
        close=_decode_price_field(_field(data, "close", default="") or ""),
        volume=_decode_volume_field(
            _field(data, "volume", default="") or "",
            scale=volume_scale,
        ),
        quote_volume=str(_field(data, "quoteVolume", "quote_volume", default="") or ""),
        is_closed=bool(_field(data, "isClosed", "is_closed", default=False)),
    )


def decode_candles_list(data: dict[str, Any], *, volume_scale: int) -> CandlesResult:
    candles = [
        decode_candle(item, volume_scale=volume_scale)
        for item in _field(data, "candles", default=[]) or []
        if isinstance(item, dict)
    ]
    if not candles:
        candles = _decode_columnar_candles(data, volume_scale=volume_scale)
    return CandlesResult(
        symbol_id=int(_field(data, "symbolId", "symbol_id", default=0) or 0),
        timeframe=str(_field(data, "timeframe", default="") or ""),
        candles=candles,
    )


def _decode_columnar_candles(data: dict[str, Any], *, volume_scale: int) -> list[Candle]:
    ts_list = _field(data, "tsSec", "ts_sec", default=[]) or []
    opens = _field(data, "open", default=[]) or []
    highs = _field(data, "high", default=[]) or []
    lows = _field(data, "low", default=[]) or []
    closes = _field(data, "close", default=[]) or []
    volumes = _field(data, "volume", default=[]) or []
    quote_volumes = _field(data, "quoteVolume", "quote_volume", default=[]) or []
    candles: list[Candle] = []
    for index, ts in enumerate(ts_list):
        candles.append(
            Candle(
                ts_sec=int(ts),
                open=_decode_price_field(opens[index]) if index < len(opens) else "",
                high=_decode_price_field(highs[index]) if index < len(highs) else "",
                low=_decode_price_field(lows[index]) if index < len(lows) else "",
                close=_decode_price_field(closes[index]) if index < len(closes) else "",
                volume=_decode_volume_field(
                    volumes[index] if index < len(volumes) else "",
                    scale=volume_scale,
                ),
                quote_volume=str(quote_volumes[index]) if index < len(quote_volumes) else "",
            )
        )
    return candles


def decode_market_overview_entry(data: dict[str, Any]) -> MarketOverviewEntry:
    from polyester.types.money import Price

    ticks = _field(data, "lastPriceTicks", "last_price_ticks", default=0) or 0
    index_ticks = _field(data, "indexPriceTicks", "index_price_ticks", default=0) or 0
    symbol = str(_field(data, "symbol", default="") or "")
    return MarketOverviewEntry(
        symbol_id=int(_field(data, "symbolId", "symbol_id", default=0) or 0),
        symbol=symbol,
        last_price=Price.from_ticks(int(ticks), symbol=symbol or None) if int(ticks) else None,
        index_price=Price.from_ticks(int(index_ticks), symbol=symbol or None)
        if int(index_ticks)
        else None,
        change_24h_bp=str(_field(data, "change24hBp", "change_24h_bp", default="") or ""),
        volume_24h_base_scaled=_optional_scaled_field(
            data, "volume24hBaseScaled", "volume_24h_base_scaled"
        ),
        volume_24h_quote_scaled=_optional_scaled_field(
            data, "volume24hQuoteScaled", "volume_24h_quote_scaled"
        ),
        volume_24h_usd_scaled=_optional_scaled_field(
            data, "volume24hUsdScaled", "volume_24h_usd_scaled"
        ),
    )


def decode_market_overview_list(data: dict[str, Any]) -> MarketOverviewList:
    markets = [
        decode_market_overview_entry(item)
        for item in _field(data, "markets", default=[]) or []
        if isinstance(item, dict)
    ]
    return MarketOverviewList(
        markets=markets,
        total=int(_field(data, "total", default=0) or 0),
    )


def _u128_str(data: dict[str, Any] | None) -> str:
    if not data:
        return "0"
    hi = int(_field(data, "hi", default=0) or 0)
    lo = int(_field(data, "lo", default=0) or 0)
    return str((hi << 64) + lo)


def decode_asset_balance(data: dict[str, Any]) -> AssetBalance:
    return AssetBalance(
        asset_id=int(_field(data, "assetId", "asset_id", default=0) or 0),
        trading=_u128_str(_field(data, "trading")),
        funding=_u128_str(_field(data, "funding")),
        reserved=_u128_str(_field(data, "reserved")),
        available=_u128_str(_field(data, "available")),
        trading_revision=int(_field(data, "tradingRevision", "trading_revision", default=0) or 0),
        funding_revision=int(_field(data, "fundingRevision", "funding_revision", default=0) or 0),
    )


def decode_balances_list(data: dict[str, Any]) -> BalancesList:
    balances = [
        decode_asset_balance(item)
        for item in _field(data, "balances", default=[]) or []
        if isinstance(item, dict)
    ]
    return BalancesList(balances=balances)


def _lifecycle_flow_payload(data: dict[str, Any]) -> dict[str, Any]:
    """Normalize list items (FlowSummaryView) and detail views (FlowDetailView.summary)."""
    summary = _field(data, "summary")
    if isinstance(summary, dict):
        return summary
    return data


def _decode_zipper_reason(value: Any) -> ZipperReasonDetails | None:
    if not isinstance(value, dict):
        return None
    raw_code = _field(value, "code", default=0)
    try:
        if isinstance(raw_code, str) and not raw_code.strip().lstrip("-").isdigit():
            code = int(reason_pb2.ZipperReasonCode.Value(raw_code.strip()))
        else:
            code = int(raw_code or 0)
    except (TypeError, ValueError):
        code = 0
    return ZipperReasonDetails(
        code=code,
        reason_id=str(_field(value, "reasonId", "reason_id", default="") or ""),
        message=str(_field(value, "message", default="") or ""),
    )


def _decode_lifecycle_reason(value: Any) -> str:
    if value is None:
        return "unspecified"
    if isinstance(value, str):
        label = value.strip()
        if not label or label in {"REASON_UNSPECIFIED", "unspecified"}:
            return "unspecified"
        if label.startswith("unknown_reason_"):
            return label
        # Accept already-normalized snake labels or SCREAMING enum names.
        if label == label.lower():
            return label
        if label.startswith("REASON_"):
            label = label.removeprefix("REASON_")
        return label.lower()
    try:
        return lifecycle_reason_from_code(int(value))
    except (TypeError, ValueError):
        return "unspecified"


def decode_lifecycle_flow(data: dict[str, Any]) -> LifecycleFlowSummary:
    payload = _lifecycle_flow_payload(data)
    latest_step = _field(payload, "latestStep", "latest_step", "currentStep", "current_step")
    flow_kind = _field(payload, "flowKind", "flow_kind")
    intent_id = _field(payload, "intentId", "intent_id", "flowId", "flow_id", default="")
    zipper_raw = _field(payload, "zipperReason", "zipper_reason")
    return LifecycleFlowSummary(
        intent_id=str(intent_id or ""),
        flow_kind=_enum_name(flow_kind) if flow_kind is not None else "",
        latest_step=_enum_name(latest_step) if latest_step is not None else "",
        is_open=bool(_field(payload, "isOpen", "is_open", default=False)),
        is_terminal=bool(_field(payload, "isTerminal", "is_terminal", default=False)),
        lifecycle_reason=_decode_lifecycle_reason(
            _field(payload, "lifecycleReason", "lifecycle_reason", "reasonCode", "reason_code")
        ),
        zipper_reason=_decode_zipper_reason(zipper_raw),
    )


def decode_lifecycle_flows_list(data: dict[str, Any]) -> LifecycleFlowsList:
    flows = [
        decode_lifecycle_flow(item)
        for item in _field(data, "flows", default=[]) or []
        if isinstance(item, dict)
    ]
    return LifecycleFlowsList(
        flows=flows,
        next_page_token=str(_field(data, "nextPageToken", "next_page_token", default="") or ""),
    )


def decode_modify_order_result(data: dict[str, Any]) -> ModifyOrderResult:
    return ModifyOrderResult(
        action_taken=str(_field(data, "actionTaken", "action_taken", default="") or ""),
        old_order_id=_id_str(_field(data, "oldOrderId", "old_order_id")),
        final_order_id=_id_str(_field(data, "finalOrderId", "final_order_id")),
        code=str(_field(data, "code", default="") or ""),
    )


def decode_cancel_all_orders_result(data: dict[str, Any]) -> CancelAllOrdersResult:
    return CancelAllOrdersResult(
        status=str(_field(data, "status", default="") or ""),
        matched_orders=int(_field(data, "matchedOrders", "matched_orders", default=0) or 0),
        submitted_cancels=int(
            _field(data, "submittedCancels", "submitted_cancels", default=0) or 0
        ),
        failed_cancels=int(_field(data, "failedCancels", "failed_cancels", default=0) or 0),
    )


def decode_trigger(data: dict[str, Any]) -> Trigger:
    from polyester.types.money import Price, Quantity

    stop = _field(data, "stop")
    trigger_price_ticks = 0
    if isinstance(stop, dict):
        trigger_price_ticks = int(
            _field(stop, "triggerPriceTicks", "trigger_price_ticks", default=0) or 0
        )
    if not trigger_price_ticks:
        trigger_price_ticks = int(
            _field(data, "triggerPriceTicks", "trigger_price_ticks", default=0) or 0
        )
    symbol = str(_field(data, "symbol", default="") or "")
    symbol_id = int(_field(data, "symbolId", "symbol_id", default=0) or 0)
    qty_raw = int(_field(data, "qtyScaled", "qty_scaled", default=0) or 0)
    return Trigger(
        trigger_id=_id_str(_field(data, "triggerId", "trigger_id")),
        symbol_id=symbol_id,
        symbol=symbol,
        trigger_type=_enum_name(_field(data, "triggerType", "trigger_type")).lower(),
        status=_enum_name(_field(data, "status")).lower(),
        side=_enum_name(_field(data, "side")).lower(),
        qty=Quantity.from_scaled(qty_raw, symbol=symbol or None, symbol_id=symbol_id),
        trigger_price=Price.from_ticks(trigger_price_ticks, symbol=symbol or None)
        if trigger_price_ticks
        else None,
        client_trigger_id=str(
            _field(data, "clientTriggerId", "client_trigger_id", default="") or ""
        ),
        cancel_reason=str(
            _field(data, "cancelReason", "cancel_reason", default="") or ""
        ),
        failure_reason=str(
            _field(data, "failureReason", "failure_reason", default="") or ""
        ),
    )


def decode_triggers_list(data: dict[str, Any]) -> TriggersList:
    triggers = [
        decode_trigger(item)
        for item in _field(data, "triggers", default=[]) or []
        if isinstance(item, dict)
    ]
    return TriggersList(
        triggers=triggers,
        total=int(_field(data, "total", default=0) or 0),
        next_page_token=str(_field(data, "nextPageToken", "next_page_token", default="") or ""),
    )


def decode_trigger_mutation(data: dict[str, Any]) -> TriggerMutationResult:
    return TriggerMutationResult(
        trigger_id=_id_str(_field(data, "triggerId", "trigger_id")),
        status=_enum_name(_field(data, "status")).lower(),
    )


def _decode_transfer_side(data: Any) -> TransferSide | None:
    if not isinstance(data, dict):
        return None
    kind = str(_field(data, "kind", default="") or "")
    account_id = str(_field(data, "accountId", "account_id", default="") or "")
    address = str(_field(data, "address", default="") or "")
    raw_chain = _field(data, "chainId", "chain_id")
    chain_id = int(raw_chain) if raw_chain not in (None, "") else None
    if not kind and not account_id and not address and chain_id is None:
        return None
    return TransferSide(kind=kind, account_id=account_id, address=address, chain_id=chain_id)


def decode_ledger_transfer(data: dict[str, Any]) -> LedgerTransfer:
    return LedgerTransfer(
        asset_id=int(_field(data, "assetId", "asset_id", default=0) or 0),
        amount=_u128_str(_field(data, "amount")),
        transfer_type=int(_field(data, "type", default=0) or 0),
        account_code=int(_field(data, "accountCode", "account_code", default=0) or 0),
        timestamp=int(_field(data, "timestamp", default=0) or 0),
        pending=bool(_field(data, "pending", default=False)),
        tx_id=str(_field(data, "txId", "tx_id", default="") or ""),
        is_debit=bool(_field(data, "isDebit", "is_debit", default=False)),
        source=_decode_transfer_side(_field(data, "source")),
        destination=_decode_transfer_side(_field(data, "destination")),
    )


def decode_transfers_list(data: dict[str, Any]) -> TransfersList:
    transfers = [
        decode_ledger_transfer(item)
        for item in _field(data, "transfers", default=[]) or []
        if isinstance(item, dict)
    ]
    cursor = _field(data, "nextCursor", "next_cursor")
    next_cursor = int(cursor) if cursor not in (None, "", 0) else None
    return TransfersList(transfers=transfers, next_cursor=next_cursor)


def decode_internal_transfer_result(data: dict[str, Any]) -> InternalTransferResult:
    from polyester.types.money import AssetAmount, QuantityDomain

    asset_id = int(_field(data, "assetId", "asset_id", default=0) or 0)
    qty_raw = _field(
        data, "quantityScaled", "quantity_scaled", "qtyScaled", "qty_scaled", default=0
    )
    scaled = int(qty_raw or 0)
    return InternalTransferResult(
        request_id=str(_field(data, "requestId", "request_id", default="") or ""),
        transfer_id=str(_field(data, "transferId", "transfer_id", default="") or ""),
        asset_id=asset_id,
        asset_code=str(_field(data, "assetCode", "asset_code", default="") or ""),
        quantity=AssetAmount.from_scaled(scaled, domain=QuantityDomain.ASSET, asset_id=asset_id)
        if scaled
        else None,
    )


def decode_deposit_address(data: dict[str, Any]) -> DepositAddress:
    return DepositAddress(
        chain_id=int(_field(data, "chainId", "chain_id", default=0) or 0),
        deposit_address=str(_field(data, "depositAddress", "deposit_address", default="") or ""),
    )


def decode_deposit_addresses_list(data: dict[str, Any]) -> DepositAddressesList:
    addresses = [
        decode_deposit_address(item)
        for item in _field(data, "depositAddresses", "deposit_addresses", default=[]) or []
        if isinstance(item, dict)
    ]
    return DepositAddressesList(addresses=addresses)


def decode_trigger_event(data: dict[str, Any]) -> TriggerEvent:
    from polyester.types.money import Price

    fire_raw = (
        _field(
            data, "firePriceTicks", "fire_price_ticks", "firePxTicks", "fire_px_ticks", default=0
        )
        or 0
    )
    child_order_raw = _field(data, "childOrderId", "child_order_id", default=0) or 0
    return TriggerEvent(
        trigger_id=_id_str(_field(data, "triggerId", "trigger_id")),
        subaccount_id=_id_str(_field(data, "subaccountId", "subaccount_id")),
        symbol_id=int(_field(data, "symbolId", "symbol_id", default=0) or 0),
        trigger_type=_enum_name(_field(data, "triggerType", "trigger_type")).lower(),
        event_type=_enum_name(_field(data, "eventType", "event_type")).lower(),
        ts_ns=ts_ns_string_from_response(
            _field(data, "tsNs", "ts_ns", default=0) or 0,
            context="TriggerEvent",
            empty_when_zero=True,
        ),
        child_seq=int(_field(data, "childSeq", "child_seq", default=0) or 0),
        child_order_id=_id_str(child_order_raw) if int(child_order_raw) else "",
        fire_price=Price.from_ticks(int(fire_raw)) if int(fire_raw) else None,
        cancel_reason=str(
            _field(data, "cancelReason", "cancel_reason", default="") or ""
        ),
        failure_reason=str(
            _field(data, "failureReason", "failure_reason", default="") or ""
        ),
    )


def decode_trigger_events_list(data: dict[str, Any]) -> TriggerEventsList:
    events = [
        decode_trigger_event(item)
        for item in _field(data, "events", default=[]) or []
        if isinstance(item, dict)
    ]
    return TriggerEventsList(
        events=events,
        next_page_token=str(_field(data, "nextPageToken", "next_page_token", default="") or ""),
    )


def _balance_range_label(value: Any) -> str:
    name = _enum_name(value).upper()
    mapping = {
        "DAY_1": "1d",
        "DAY_7": "7d",
        "DAY_30": "30d",
        "DAY_90": "90d",
        "DAY_180": "180d",
        "DAY_365": "365d",
    }
    return mapping.get(name, name.lower() or "")


def decode_balance_history_series(data: dict[str, Any]) -> BalanceHistorySeries:
    balance_q = _field(data, "balanceQ", "balance_q", default=[]) or []
    return BalanceHistorySeries(
        asset_id=int(_field(data, "assetId", "asset_id", default=0) or 0),
        account_code=int(_field(data, "accountCode", "account_code", default=0) or 0),
        balance_q=[int(v) for v in balance_q],
    )


def decode_balance_history(data: dict[str, Any]) -> BalanceHistory:
    series = [
        decode_balance_history_series(item)
        for item in _field(data, "series", default=[]) or []
        if isinstance(item, dict)
    ]
    return BalanceHistory(
        range=_balance_range_label(_field(data, "range")),
        bucket=str(_field(data, "bucket", default="") or ""),
        start_ts_sec=int(_field(data, "startTsSec", "start_ts_sec", default=0) or 0),
        end_ts_sec=int(_field(data, "endTsSec", "end_ts_sec", default=0) or 0),
        points=int(_field(data, "points", default=0) or 0),
        series=series,
    )


def decode_equity_history_series(data: dict[str, Any]) -> EquityHistorySeries:
    account = _field(data, "account")
    asset = _field(data, "asset")
    portfolio = _field(data, "portfolioAccount", "portfolio_account")
    account_code = 0
    account_name = ""
    asset_id = 0
    asset_symbol = ""
    portfolio_account_id = ""
    portfolio_remaining = False
    if isinstance(account, dict):
        account_code = int(_field(account, "code", default=0) or 0)
        account_name = str(_field(account, "name", default="") or "")
    elif isinstance(asset, dict):
        asset_id = int(_field(asset, "id", default=0) or 0)
        asset_symbol = str(_field(asset, "symbol", default="") or "")
    elif isinstance(portfolio, dict):
        raw_account_id = _field(portfolio, "accountId", "account_id")
        if raw_account_id not in (None, ""):
            portfolio_account_id = _id_str(raw_account_id)
        portfolio_remaining = bool(_field(portfolio, "remaining", default=False))
    equity_q = _field(data, "equityQ", "equity_q", default=[]) or []
    return EquityHistorySeries(
        account_code=account_code,
        account_name=account_name,
        asset_id=asset_id,
        asset_symbol=asset_symbol,
        portfolio_account_id=portfolio_account_id,
        portfolio_remaining=portfolio_remaining,
        equity_q=[int(v) for v in equity_q],
    )


def decode_equity_history(data: dict[str, Any]) -> EquityHistory:
    series = [
        decode_equity_history_series(item)
        for item in _field(data, "series", default=[]) or []
        if isinstance(item, dict)
    ]
    return EquityHistory(
        range=_balance_range_label(_field(data, "range")),
        bucket=str(_field(data, "bucket", default="") or ""),
        start_ts_sec=int(_field(data, "startTsSec", "start_ts_sec", default=0) or 0),
        end_ts_sec=int(_field(data, "endTsSec", "end_ts_sec", default=0) or 0),
        quote_asset=str(_field(data, "quoteAsset", "quote_asset", default="") or ""),
        points=int(_field(data, "points", default=0) or 0),
        series=series,
    )


def decode_hold(data: dict[str, Any]) -> Hold:
    return Hold(
        hold_id=_id_str(_field(data, "holdId", "hold_id")),
        asset_id=int(_field(data, "assetId", "asset_id", default=0) or 0),
        amount_reserved=_u128_str(_field(data, "amountReserved", "amount_reserved")),
        expires_at_ns=str(_field(data, "expiresAtNs", "expires_at_ns", default="") or ""),
    )


def decode_bucket_transfer_result(data: dict[str, Any]) -> BucketTransferResult:
    return BucketTransferResult(
        transfer_id=str(_field(data, "transferId", "transfer_id", default="") or ""),
        timestamp_ns=str(_field(data, "timestamp", default="") or ""),
    )


def decode_holds_list(data: dict[str, Any]) -> HoldsList:
    holds = [
        decode_hold(item)
        for item in _field(data, "holds", default=[]) or []
        if isinstance(item, dict)
    ]
    return HoldsList(holds=holds)


def decode_market_trade_bytes(payload: bytes, *, quantity_scale: int) -> MarketTrade:
    from polyester._wire import protobuf_to_public_dict
    from polyester.gen.marketdata.v1.marketdata_pb2 import MarketTrade as MarketTradePb

    message = MarketTradePb()
    message.ParseFromString(payload)
    return decode_market_trade(protobuf_to_public_dict(message), quantity_scale=quantity_scale)


def decode_api_key(data: dict[str, Any]) -> ApiKeySummary:
    return ApiKeySummary(
        key_id=str(_field(data, "keyId", "key_id", default="") or ""),
        label=str(_field(data, "label", default="") or ""),
        status=_enum_name(_field(data, "status")),
        subaccount_id=_id_str(_field(data, "subaccountId", "subaccount_id")),
        updated_at=None,
        revision=int(_field(data, "revision", default=0) or 0),
    )


def decode_api_keys_list(data: dict[str, Any]) -> ApiKeysList:
    keys = [
        decode_api_key(item)
        for item in _field(data, "apiKeys", "api_keys", default=[]) or []
        if isinstance(item, dict)
    ]
    return ApiKeysList(api_keys=keys)


def decode_resolved_account(data: dict[str, Any]) -> ResolvedAccount:
    return ResolvedAccount(
        smart_account_address=str(
            _field(data, "smartAccountAddress", "smart_account_address", default="") or ""
        ),
        kind=str(_field(data, "kind", default="") or ""),
        root_username=str(_field(data, "rootUsername", "root_username", default="") or ""),
        subaccount_label=str(_field(data, "subaccountLabel", "subaccount_label", default="") or ""),
        account_id=_id_str(_field(data, "accountId", "account_id")),
    )


def decode_resolved_accounts(data: dict[str, Any]) -> ResolvedAccountsList:
    matches = [
        decode_resolved_account(item)
        for item in _field(data, "matches", default=[]) or []
        if isinstance(item, dict)
    ]
    return ResolvedAccountsList(matches=matches)


def decode_transfer_destination(data: dict[str, Any]) -> TransferDestination:
    return TransferDestination(
        account_id=_id_str(_field(data, "accountId", "account_id")),
        subaccount_id=_id_str(_field(data, "subaccountId", "subaccount_id")),
        label=str(_field(data, "label", default="") or ""),
        smart_account_address=str(
            _field(data, "smartAccountAddress", "smart_account_address", default="") or ""
        ),
    )


def decode_transfer_destinations(data: dict[str, Any]) -> TransferDestinationsList:
    destinations = [
        decode_transfer_destination(item)
        for item in _field(data, "destinations", default=[]) or []
        if isinstance(item, dict)
    ]
    return TransferDestinationsList(destinations=destinations)


def decode_batch_replace_result(data: dict[str, Any]) -> BatchReplaceOrdersResult:
    results = [
        BatchReplaceAdmissionItem(
            item_index=int(_field(item, "itemIndex", "item_index", default=0) or 0),
            status=_enum_name(_field(item, "status")).lower(),
            client_order_id=str(_field(item, "clientOrderId", "client_order_id", default="") or ""),
            old_order_id=_id_str(_field(item, "oldOrderId", "old_order_id")),
            replacement_order_id=_id_str(
                _field(item, "replacementOrderId", "replacement_order_id")
            ),
            code=str(_field(item, "code", default="") or ""),
        )
        for item in _field(data, "results", default=[]) or []
        if isinstance(item, dict)
    ]
    return BatchReplaceOrdersResult(
        batch_request_id=_id_str(_field(data, "batchRequestId", "batch_request_id")),
        status=_enum_name(_field(data, "status")).lower(),
        results=results,
        accepted_count=int(_field(data, "acceptedCount", "accepted_count", default=0) or 0),
        rejected_count=int(_field(data, "rejectedCount", "rejected_count", default=0) or 0),
        accepted_ts_ns=ts_ns_from_response(
            _field(data, "acceptedTsNs", "accepted_ts_ns", default=0) or 0,
            context="BatchReplaceOrders",
            field_name="accepted_ts_ns",
        ),
    )


def decode_batch_replace_status(data: dict[str, Any]) -> BatchReplaceStatusResult:
    items = [
        BatchReplaceStatusItem(
            item_index=int(_field(item, "itemIndex", "item_index", default=0) or 0),
            phase=_enum_name(_field(item, "phase")).lower(),
            old_order_id=_id_str(_field(item, "oldOrderId", "old_order_id")),
            replacement_order_id=_id_str(
                _field(item, "replacementOrderId", "replacement_order_id")
            ),
            order_status=_enum_name(_field(item, "orderStatus", "order_status")).lower(),
            code=str(_field(item, "code", default="") or ""),
            updated_ts_ns=ts_ns_from_response(
                _field(item, "updatedTsNs", "updated_ts_ns", default=0) or 0,
                context="GetBatchReplaceStatus",
                field_name="updated_ts_ns",
            ),
        )
        for item in _field(data, "items", default=[]) or []
        if isinstance(item, dict)
    ]
    return BatchReplaceStatusResult(
        batch_request_id=_id_str(_field(data, "batchRequestId", "batch_request_id")),
        admission_status=_enum_name(_field(data, "admissionStatus", "admission_status")).lower(),
        items=items,
        accepted_count=int(_field(data, "acceptedCount", "accepted_count", default=0) or 0),
        rejected_count=int(_field(data, "rejectedCount", "rejected_count", default=0) or 0),
        accepted_ts_ns=ts_ns_from_response(
            _field(data, "acceptedTsNs", "accepted_ts_ns", default=0) or 0,
            context="GetBatchReplaceStatus",
            field_name="accepted_ts_ns",
        ),
        updated_ts_ns=ts_ns_from_response(
            _field(data, "updatedTsNs", "updated_ts_ns", default=0) or 0,
            context="GetBatchReplaceStatus",
            field_name="updated_ts_ns",
        ),
    )


def decode_withdraw_intent(data: dict[str, Any]) -> WithdrawIntentResult:
    return WithdrawIntentResult(
        intent_id=str(_field(data, "intentId", "intent_id", default="") or "")
    )
