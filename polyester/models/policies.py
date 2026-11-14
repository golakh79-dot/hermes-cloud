from __future__ import annotations

from datetime import datetime

import msgspec


class SpotMarketRule(msgspec.Struct, kw_only=True, omit_defaults=True):
    symbol_id: int = 0
    symbol: str = ""


class SubaccountPolicy(msgspec.Struct, kw_only=True, omit_defaults=True):
    id: str = ""
    name: str = ""
    description: str = ""
    spot_markets: list[SpotMarketRule] = []
    spot_market_scope: str = ""
    actions: list[str] = []
    is_template: bool = False
    source_template_id: str = ""
    max_order_notional: int = 0
    max_open_orders: int = 0
    trading_halted: bool = False
    locked: bool = False
    review_at: datetime | None = None
    expires_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    revision: int = 0


class ApiPolicy(msgspec.Struct, kw_only=True, omit_defaults=True):
    id: str = ""
    name: str = ""
    description: str = ""
    spot_markets: list[SpotMarketRule] = []
    actions: list[str] = []
    spot_market_scope: str = ""
    is_template: bool = False
    source_template_id: str = ""
    created_at: datetime | None = None
    updated_at: datetime | None = None
    revision: int = 0


class SubaccountPoliciesList(msgspec.Struct, kw_only=True, omit_defaults=True):
    policies: list[SubaccountPolicy]


class ApiPoliciesList(msgspec.Struct, kw_only=True, omit_defaults=True):
    policies: list[ApiPolicy]
