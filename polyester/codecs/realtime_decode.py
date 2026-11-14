from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any, TypeVar

from polyester.catalogs import CatalogManager
from polyester.codecs.decode.api_keys import api_key_from_proto
from polyester.codecs.decode.balances import asset_balance_from_proto
from polyester.codecs.decode.lifecycle import flow_detail_from_proto, flow_summary_from_proto
from polyester.codecs.decode.market_data import candle_point_from_proto
from polyester.codecs.decode.market_overview import market_overview_entry_from_proto
from polyester.codecs.decode.orders import user_trade_from_proto
from polyester.codecs.decode.policies import api_policy_from_proto, subaccount_policy_from_proto
from polyester.codecs.decode.sub_accounts import subaccount_from_proto
from polyester.codecs.decode.transfers import ledger_transfer_from_proto
from polyester.codecs.decode.triggers import trigger_event_from_proto, trigger_from_proto
from polyester.codecs.scalars import format_id
from polyester.errors import PolyesterRealtimeError
from polyester.models import ApiData, AssetBalance, LedgerTransfer, UserTrade
from polyester.models.auth import AccountIdentity
from polyester.models.market import Candle, MarketOverviewList, MarketTrade
from polyester.models.policies import ApiPolicy, SubaccountPolicy
from polyester.models.realtime import AddressBookViewInvalidation, OrderBookDeltaUpdate
from polyester.models.sub_accounts import SubAccount
from polyester.models.trading import ApiKeySummary, LifecycleFlowSummary, Trigger, TriggerEvent

T = TypeVar("T")
MAX_REALTIME_MESSAGE_BYTES = 4 * 1024 * 1024


def _parse_proto(payload: bytes, message_cls):
    if not payload:
        raise PolyesterRealtimeError("proto decode: empty publication payload")
    if len(payload) > MAX_REALTIME_MESSAGE_BYTES:
        raise PolyesterRealtimeError(
            f"proto decode: publication exceeds {MAX_REALTIME_MESSAGE_BYTES} bytes"
        )
    message = message_cls()
    try:
        message.ParseFromString(payload)
    except Exception as exc:
        raise PolyesterRealtimeError(f"proto decode: {exc}") from exc
    return message


def _decode_batch_members(
    events: Iterable[Any], decode: Callable[[Any], T]
) -> list[T | PolyesterRealtimeError]:
    """Decode every event of a batch publication in order.

    A member that fails to decode becomes a ``PolyesterRealtimeError`` in its
    slot, so one malformed event never drops the rest of its batch.
    """
    members: list[T | PolyesterRealtimeError] = []
    for index, event in enumerate(events):
        try:
            members.append(decode(event))
        except Exception as exc:
            error = PolyesterRealtimeError(f"batch event {index}: {exc}")
            error.__cause__ = exc
            members.append(error)
    return members


def decode_asset_balance_bytes(payload: bytes) -> AssetBalance:
    from polyester.gen.ledger.read.v1.ledger_read_pb2 import AssetBalance as AssetBalancePb

    return asset_balance_from_proto(_parse_proto(payload, AssetBalancePb))


def decode_user_trade_bytes(payload: bytes) -> UserTrade:
    from polyester.gen.orders.v1.orders_read_pb2 import UserTrade as UserTradePb

    return user_trade_from_proto(_parse_proto(payload, UserTradePb))


def decode_user_trade_batch_bytes(payload: bytes) -> list[UserTrade | PolyesterRealtimeError]:
    from polyester.gen.orders.v1.orders_read_pb2 import UserTradeBatch

    batch = _parse_proto(payload, UserTradeBatch)
    return _decode_batch_members(batch.events, user_trade_from_proto)


def decode_ledger_transfer_bytes(payload: bytes) -> LedgerTransfer:
    from polyester.gen.ledger.read.v1.ledger_read_pb2 import TransferRow

    return ledger_transfer_from_proto(_parse_proto(payload, TransferRow))


def decode_ledger_transfer_batch_bytes(
    payload: bytes,
) -> list[LedgerTransfer | PolyesterRealtimeError]:
    from polyester.gen.ledger.read.v1.ledger_read_pb2 import TransferRowBatch

    batch = _parse_proto(payload, TransferRowBatch)
    return _decode_batch_members(batch.events, ledger_transfer_from_proto)


def decode_trigger_bytes(payload: bytes) -> Trigger:
    from polyester.gen.triggers.v1.triggers_pb2 import Trigger as TriggerPb

    return trigger_from_proto(_parse_proto(payload, TriggerPb))


def decode_trigger_event_bytes(payload: bytes) -> TriggerEvent:
    from polyester.gen.triggers.v1.triggers_pb2 import TriggerEvent as TriggerEventPb

    return trigger_event_from_proto(_parse_proto(payload, TriggerEventPb))


def decode_trigger_event_batch_bytes(
    payload: bytes,
) -> list[TriggerEvent | PolyesterRealtimeError]:
    from polyester.gen.triggers.v1.triggers_pb2 import TriggerEventBatch

    batch = _parse_proto(payload, TriggerEventBatch)
    return _decode_batch_members(batch.events, trigger_event_from_proto)


def decode_market_trade_batch_bytes(
    payload: bytes, *, quantity_scale: int
) -> list[MarketTrade | PolyesterRealtimeError]:
    from polyester._wire import protobuf_to_public_dict
    from polyester.codecs.wire_decode import decode_market_trade
    from polyester.gen.marketdata.v1.marketdata_pb2 import MarketTradeBatch

    batch = _parse_proto(payload, MarketTradeBatch)
    return _decode_batch_members(
        batch.events,
        lambda event: decode_market_trade(
            protobuf_to_public_dict(event), quantity_scale=quantity_scale
        ),
    )


def decode_api_key_bytes(payload: bytes) -> ApiKeySummary:
    from polyester.gen.auth.v1.api_keys_pb2 import ApiKey

    return api_key_from_proto(_parse_proto(payload, ApiKey))


def decode_subaccount_bytes(payload: bytes) -> SubAccount:
    from polyester.gen.auth.v1.subaccounts_pb2 import Subaccount

    return subaccount_from_proto(_parse_proto(payload, Subaccount))


def decode_subaccount_policy_bytes(payload: bytes) -> SubaccountPolicy:
    from polyester.gen.auth.v1.policies_pb2 import SubaccountPolicyView

    return subaccount_policy_from_proto(_parse_proto(payload, SubaccountPolicyView))


def decode_api_policy_bytes(payload: bytes) -> ApiPolicy:
    from polyester.gen.auth.v1.policies_pb2 import ApiPolicyView

    return api_policy_from_proto(_parse_proto(payload, ApiPolicyView))


def decode_flow_summary_bytes(payload: bytes) -> LifecycleFlowSummary:
    from polyester.gen.chain.lifecycle.v1.lifecycle_read_pb2 import FlowSummaryView

    return flow_summary_from_proto(_parse_proto(payload, FlowSummaryView))


def decode_flow_detail_bytes(payload: bytes) -> LifecycleFlowSummary:
    from polyester.gen.chain.lifecycle.v1.lifecycle_read_pb2 import FlowDetailView

    return flow_detail_from_proto(_parse_proto(payload, FlowDetailView))


def decode_market_overview_batch_bytes(
    payload: bytes, catalogs: CatalogManager | None = None
) -> MarketOverviewList:
    from polyester.gen.marketoverview.v1.marketoverview_pb2 import MarketOverviewBatch

    batch = _parse_proto(payload, MarketOverviewBatch)
    markets = [market_overview_entry_from_proto(item, catalogs) for item in batch.markets]
    return MarketOverviewList(markets=markets, total=len(markets))


def decode_account_identity_bytes(payload: bytes) -> AccountIdentity:
    from polyester.gen.auth.v1.profile_pb2 import AccountIdentity as AccountIdentityPb

    msg = _parse_proto(payload, AccountIdentityPb)
    return AccountIdentity(
        account_id=format_id(int(msg.account_id)),
        username=msg.username,
        avatar_url=msg.avatar_url,
        root_smart_account_address=msg.root_smart_account_address,
    )


def decode_address_book_invalidation_bytes(payload: bytes) -> AddressBookViewInvalidation:
    from polyester.gen.auth.v1.address_book_pb2 import AddressBookViewInvalidated

    msg = _parse_proto(payload, AddressBookViewInvalidated)
    scope = ""
    if msg.HasField("scope"):
        scope = format_id(int(msg.scope.root_account_id)) if msg.scope.root_account_id else ""
    invalidated_at = ""
    if msg.HasField("invalidated_at"):
        invalidated_at = msg.invalidated_at.ToJsonString()
    return AddressBookViewInvalidation(
        scope=scope,
        invalidated_at=invalidated_at,
        view_revision=int(msg.view_revision),
    )


def decode_orderbook_delta_bytes(payload: bytes) -> OrderBookDeltaUpdate:
    from polyester.gen.orderbook.v1.orderbook_pb2 import OrderBookDelta

    msg = _parse_proto(payload, OrderBookDelta)
    return OrderBookDeltaUpdate(
        symbol_id=int(msg.symbol_id),
        book_seq_start=str(msg.book_seq_start),
        book_seq_end=str(msg.book_seq_end),
        reset=bool(msg.reset),
        bids=[(str(level.price_ticks), str(level.qty_scaled)) for level in msg.bids],
        asks=[(str(level.price_ticks), str(level.qty_scaled)) for level in msg.asks],
    )


def decode_candle_point_bytes(
    *,
    symbol_id: int,
    timeframe: str,
    volume_scale: int,
) -> Callable[[bytes], Candle]:
    from polyester.gen.marketdata.v1.marketdata_pb2 import CandlePoint

    def decode(payload: bytes) -> Candle:
        point = _parse_proto(payload, CandlePoint)
        return candle_point_from_proto(point, volume_scale=volume_scale)

    _ = (symbol_id, timeframe)
    return decode


def decode_heatmap_live_bucket_bytes(payload: bytes) -> ApiData:
    from polyester._wire import protobuf_to_public_dict
    from polyester.gen.marketdata.v1.heatmap_pb2 import HeatmapLiveBucket

    msg = _parse_proto(payload, HeatmapLiveBucket)
    return ApiData(raw=protobuf_to_public_dict(msg))


def decode_zipped_asset_supply_batch_bytes(payload: bytes) -> ApiData:
    from polyester._wire import protobuf_to_public_dict
    from polyester.gen.chain.zipper.v1.zipper_pb2 import ZippedAssetSupplyBatch

    msg = _parse_proto(payload, ZippedAssetSupplyBatch)
    return ApiData(raw=protobuf_to_public_dict(msg))
