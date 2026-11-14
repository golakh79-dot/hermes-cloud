from __future__ import annotations

from google.protobuf.message import Message

from polyester.codecs.proto_helpers import format_uint64_id, has_field, proto_enum_name, u128_to_str
from polyester.gen.ledger.read.v1 import ledger_read_pb2
from polyester.models import (
    AssetBalance,
    BalanceHistory,
    BalanceHistorySeries,
    BalancesList,
    EquityHistory,
    EquityHistorySeries,
    Hold,
    HoldsList,
)

_BALANCE_RANGE_LABELS: dict[int, str] = {
    ledger_read_pb2.DAY_1: "1d",
    ledger_read_pb2.DAY_7: "7d",
    ledger_read_pb2.DAY_30: "30d",
    ledger_read_pb2.DAY_90: "90d",
    ledger_read_pb2.DAY_180: "180d",
    ledger_read_pb2.DAY_365: "365d",
}


def u128_from_proto(msg: Message) -> str:
    return u128_to_str(int(getattr(msg, "hi", 0)), int(getattr(msg, "lo", 0)))


def _balance_range_label(value: int) -> str:
    if value in _BALANCE_RANGE_LABELS:
        return _BALANCE_RANGE_LABELS[value]
    name = proto_enum_name(ledger_read_pb2.BalanceRange, value)
    return name.replace("day_", "") + "d" if name.startswith("day_") else name


def asset_balance_from_proto(msg: ledger_read_pb2.AssetBalance) -> AssetBalance:
    return AssetBalance(
        asset_id=int(msg.asset_id),
        trading=u128_from_proto(msg.trading),
        funding=u128_from_proto(msg.funding),
        reserved=u128_from_proto(msg.reserved),
        available=u128_from_proto(msg.available),
        trading_revision=int(msg.trading_revision),
        funding_revision=int(msg.funding_revision),
    )


def balances_list_from_proto(msg: ledger_read_pb2.GetBalancesResponse) -> BalancesList:
    return BalancesList(balances=[asset_balance_from_proto(item) for item in msg.balances])


def balance_history_series_from_proto(msg: ledger_read_pb2.BalanceSeries) -> BalanceHistorySeries:
    return BalanceHistorySeries(
        asset_id=int(msg.asset_id),
        account_code=int(msg.account_code),
        balance_q=[int(v) for v in msg.balance_q],
    )


def balance_history_from_proto(msg: ledger_read_pb2.GetBalanceHistoryResponse) -> BalanceHistory:
    return BalanceHistory(
        range=_balance_range_label(msg.range),
        bucket=msg.bucket,
        start_ts_sec=int(msg.start_ts_sec),
        end_ts_sec=int(msg.end_ts_sec),
        points=int(msg.points),
        series=[balance_history_series_from_proto(item) for item in msg.series],
    )


def equity_history_series_from_proto(msg: ledger_read_pb2.EquitySeries) -> EquityHistorySeries:
    account_code = 0
    account_name = ""
    asset_id = 0
    asset_symbol = ""
    portfolio_account_id = ""
    portfolio_remaining = False
    if msg.HasField("account"):
        account_code = int(msg.account.account_code)
        account_name = msg.account.name
    elif msg.HasField("asset"):
        asset_id = int(msg.asset.id)
        asset_symbol = msg.asset.symbol
    elif msg.HasField("portfolio_account"):
        grouping = msg.portfolio_account
        if has_field(grouping, "account_id"):
            portfolio_account_id = format_uint64_id(int(grouping.account_id))
        portfolio_remaining = bool(grouping.remaining)
    return EquityHistorySeries(
        account_code=account_code,
        account_name=account_name,
        asset_id=asset_id,
        asset_symbol=asset_symbol,
        portfolio_account_id=portfolio_account_id,
        portfolio_remaining=portfolio_remaining,
        equity_q=[int(v) for v in msg.equity_q],
    )


def equity_history_from_proto(
    msg: ledger_read_pb2.GetEquityHistorySeriesResponse,
) -> EquityHistory:
    return EquityHistory(
        range=_balance_range_label(msg.range),
        bucket=msg.bucket,
        start_ts_sec=int(msg.start_ts_sec),
        end_ts_sec=int(msg.end_ts_sec),
        quote_asset=msg.quote_asset,
        points=int(msg.points),
        series=[equity_history_series_from_proto(item) for item in msg.series],
    )


def hold_from_proto(msg: ledger_read_pb2.HoldRow) -> Hold:
    return Hold(
        hold_id=format_uint64_id(msg.hold_id),
        asset_id=int(msg.asset_id),
        amount_reserved=u128_from_proto(msg.amount_reserved_e18),
        expires_at_ns=str(msg.expires_at_ns),
    )


def holds_list_from_proto(msg: ledger_read_pb2.ListHoldsResponse) -> HoldsList:
    return HoldsList(holds=[hold_from_proto(item) for item in msg.holds])
