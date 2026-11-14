"""Protobuf response decoders (proto Message ? public msgspec models)."""

from polyester.codecs.decode.api_keys import (
    api_key_from_proto,
    api_keys_list_from_proto,
    get_api_key_from_proto,
)
from polyester.codecs.decode.balances import (
    balance_history_from_proto,
    balances_list_from_proto,
    equity_history_from_proto,
    holds_list_from_proto,
)
from polyester.codecs.decode.common import api_data_from_proto
from polyester.codecs.decode.deposit import (
    create_deposit_address_from_proto,
    deposit_address_from_proto,
    deposit_addresses_list_from_proto,
)
from polyester.codecs.decode.fees import spot_fee_rates_list_from_proto
from polyester.codecs.decode.heatmap import heatmap_from_proto
from polyester.codecs.decode.internal_transfers import internal_transfer_from_proto
from polyester.codecs.decode.lifecycle import (
    flow_from_get_by_tx_response,
    flow_from_get_response,
    flows_list_from_proto,
)
from polyester.codecs.decode.market_data import (
    candles_columns_from_proto,
    candles_from_proto,
    market_trades_from_proto,
)
from polyester.codecs.decode.market_overview import (
    market_overview_list_from_proto,
    spot_volume_history_from_proto,
)
from polyester.codecs.decode.orderbook import orderbook_from_proto
from polyester.codecs.decode.orders import (
    batch_replace_from_proto,
    batch_replace_status_from_proto,
    cancel_all_from_proto,
    get_order_from_proto,
    modify_order_from_proto,
    order_mutation_from_proto,
    orders_list_from_proto,
    preview_order_from_proto,
    user_trades_list_from_proto,
)
from polyester.codecs.decode.resolve import resolved_accounts_from_proto
from polyester.codecs.decode.trading_rate_limits import (
    rate_limit_config_from_proto,
    trading_rate_limits_from_proto,
)
from polyester.codecs.decode.transfers import transfers_list_from_proto
from polyester.codecs.decode.triggers import (
    get_trigger_from_proto,
    trigger_events_list_from_proto,
    trigger_from_proto,
    trigger_mutation_from_proto,
    triggers_list_from_proto,
)
from polyester.codecs.decode.vip import vip_status_from_proto, vip_tiers_list_from_proto
from polyester.codecs.decode.withdraw import withdraw_intent_from_proto
from polyester.codecs.decode.zipper import deposit_withdraw_config_from_proto

__all__ = [
    "api_data_from_proto",
    "api_key_from_proto",
    "api_keys_list_from_proto",
    "balance_history_from_proto",
    "balances_list_from_proto",
    "batch_replace_from_proto",
    "batch_replace_status_from_proto",
    "cancel_all_from_proto",
    "candles_columns_from_proto",
    "candles_from_proto",
    "create_deposit_address_from_proto",
    "deposit_address_from_proto",
    "deposit_addresses_list_from_proto",
    "deposit_withdraw_config_from_proto",
    "equity_history_from_proto",
    "flow_from_get_by_tx_response",
    "flow_from_get_response",
    "flows_list_from_proto",
    "rate_limit_config_from_proto",
    "spot_fee_rates_list_from_proto",
    "trading_rate_limits_from_proto",
    "vip_status_from_proto",
    "vip_tiers_list_from_proto",
    "get_api_key_from_proto",
    "get_order_from_proto",
    "get_trigger_from_proto",
    "heatmap_from_proto",
    "holds_list_from_proto",
    "internal_transfer_from_proto",
    "market_overview_list_from_proto",
    "spot_volume_history_from_proto",
    "market_trades_from_proto",
    "modify_order_from_proto",
    "order_mutation_from_proto",
    "orderbook_from_proto",
    "orders_list_from_proto",
    "preview_order_from_proto",
    "resolved_accounts_from_proto",
    "transfers_list_from_proto",
    "trigger_events_list_from_proto",
    "trigger_from_proto",
    "trigger_mutation_from_proto",
    "triggers_list_from_proto",
    "user_trades_list_from_proto",
    "withdraw_intent_from_proto",
]
