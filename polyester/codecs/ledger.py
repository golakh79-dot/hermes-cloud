from __future__ import annotations

from typing import Any

from polyester.errors import PolyesterValidationError
from polyester.gen.ledger.read.v1 import ledger_read_pb2

BALANCE_RANGE_TO_PROTO = {
    "1d": ledger_read_pb2.DAY_1,
    "7d": ledger_read_pb2.DAY_7,
    "30d": ledger_read_pb2.DAY_30,
    "90d": ledger_read_pb2.DAY_90,
    "180d": ledger_read_pb2.DAY_180,
    "365d": ledger_read_pb2.DAY_365,
}

EQUITY_GROUP_BY_TO_PROTO = {
    "account": ledger_read_pb2.GROUP_BY_ACCOUNT,
    "asset": ledger_read_pb2.GROUP_BY_ASSET,
}


def resolve_balance_range(range_key: str) -> Any:
    key = range_key.lower().strip()
    if key not in BALANCE_RANGE_TO_PROTO:
        raise PolyesterValidationError(
            "range must be one of '1d', '7d', '30d', '90d', '180d', or '365d'"
        )
    return BALANCE_RANGE_TO_PROTO[key]


def resolve_equity_group_by(group_by: str) -> Any:
    key = group_by.lower().strip()
    if key not in EQUITY_GROUP_BY_TO_PROTO:
        raise PolyesterValidationError("group_by must be 'account' or 'asset'")
    return EQUITY_GROUP_BY_TO_PROTO[key]
