from __future__ import annotations

from polyester.catalogs import CatalogManager
from polyester.codecs.proto_helpers import format_uint64_id, proto_enum_name
from polyester.codecs.scalars import timestamp_dict_to_datetime
from polyester.gen.auth.v1 import policies_pb2
from polyester.models.policies import (
    ApiPolicy,
    SpotMarketRule,
    SubaccountPolicy,
)


def _optional_uint64_id(value: int) -> str:
    if value == 0:
        return ""
    return format_uint64_id(value)


def _spot_market_from_proto(
    msg: policies_pb2.SpotMarketRule,
    catalogs: CatalogManager | None = None,
) -> SpotMarketRule:
    symbol_id = int(msg.symbol_id)
    symbol = catalogs.symbol_for_symbol_id(symbol_id) if catalogs is not None else None
    return SpotMarketRule(
        symbol_id=symbol_id,
        symbol=symbol or "",
    )


def _policy_actions_from_proto(actions: list[int]) -> list[str]:
    return [
        proto_enum_name(policies_pb2.PolicyAction, action)
        for action in actions
        if action != policies_pb2.UNSPECIFIED
    ]


def subaccount_policy_from_proto(
    msg: policies_pb2.SubaccountPolicyView,
    catalogs: CatalogManager | None = None,
) -> SubaccountPolicy:
    return SubaccountPolicy(
        id=format_uint64_id(msg.id),
        name=msg.name,
        description=msg.description,
        spot_markets=[_spot_market_from_proto(item, catalogs) for item in msg.spot_markets],
        spot_market_scope=proto_enum_name(policies_pb2.MarketScope.Value, msg.spot_market_scope),
        actions=_policy_actions_from_proto(list(msg.actions)),
        is_template=bool(msg.is_template),
        source_template_id=_optional_uint64_id(msg.source_template_id),
        max_order_notional=int(msg.max_order_notional),
        max_open_orders=int(msg.max_open_orders),
        trading_halted=bool(msg.trading_halted),
        locked=bool(msg.locked),
        review_at=timestamp_dict_to_datetime(msg.review_at),
        expires_at=timestamp_dict_to_datetime(msg.expires_at),
        created_at=timestamp_dict_to_datetime(msg.created_at),
        updated_at=timestamp_dict_to_datetime(msg.updated_at),
        revision=int(msg.revision),
    )


def api_policy_from_proto(
    msg: policies_pb2.ApiPolicyView,
    catalogs: CatalogManager | None = None,
) -> ApiPolicy:
    return ApiPolicy(
        id=format_uint64_id(msg.id),
        name=msg.name,
        description=msg.description,
        spot_markets=[_spot_market_from_proto(item, catalogs) for item in msg.spot_markets],
        actions=_policy_actions_from_proto(list(msg.actions)),
        spot_market_scope=proto_enum_name(policies_pb2.MarketScope.Value, msg.spot_market_scope),
        is_template=bool(msg.is_template),
        source_template_id=_optional_uint64_id(msg.source_template_id),
        created_at=timestamp_dict_to_datetime(msg.created_at),
        updated_at=timestamp_dict_to_datetime(msg.updated_at),
        revision=int(msg.revision),
    )
