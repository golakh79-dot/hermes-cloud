from __future__ import annotations

from datetime import datetime
from typing import Any

import msgspec

from polyester.models.order_key import OrderKey
from polyester.models.ratelimit import RateLimitDetail
from polyester.types.money import AssetAmount, Price, Quantity


class Order(msgspec.Struct, kw_only=True, omit_defaults=True):
    """Spot order snapshot.

    ``orig_qty`` is the current accepted total quantity and changes after a
    successful modify. ``cum_qty`` and ``avg_px`` are cumulative execution
    values across the lineage through the returned generation, not values
    limited to one physical order. ``leaves_qty`` is remaining working
    quantity. Retain the first submitted quantity separately if you need it.
    ``inherited_cum_qty`` is the part of ``cum_qty`` carried over from
    predecessors when a replacement was accepted; zero for an order never
    replaced.
    """

    order_id: str
    symbol_id: int
    client_order_id: str = ""
    side: str = ""
    status: str = ""
    order_type: str = ""
    tif: str = ""
    orig_qty: Quantity | None = None
    cum_qty: Quantity | None = None
    inherited_cum_qty: Quantity | None = None
    leaves_qty: Quantity | None = None
    price: Price | None = None
    avg_px: Price | None = None
    created_ts_ns: str = ""
    version: int = 0
    post_only: bool = False
    fee_asset: str = ""
    submitted_max_quote_debit_scaled: str = ""
    attached_risk: AttachedRisk | None = None
    lineage: OrderLineage | None = None
    # RFC3339 UTC expiry for GTD orders; omitted for every other TIF.
    expire_at: str | None = None
    # Why a ``rejected`` order was refused: the Orders API error code for the
    # same refusal, without its ``ERROR_CODE_`` prefix (for example
    # ``POST_ONLY_CROSS``). ``None`` for every other status.
    reject_reason: str | None = None
    # Why a ``canceled`` order ended, without the ``CANCEL_REASON_`` prefix
    # (for example ``USER_REQUEST`` or ``REPLACED``). ``None`` for every other
    # status. A number this SDK does not know reads ``UNKNOWN_CANCEL_REASON(n)``.
    cancel_reason: str | None = None


class OrderLineage(msgspec.Struct, kw_only=True, omit_defaults=True):
    """Stable replacement-chain identity for an order or execution.

    ``id`` is the first generation's public order ID and stays stable across
    accepted replacements. ``generation`` is one-based and identifies the
    accepted replacement generation, not per-order state ``version``.
    """

    id: str = ""
    generation: int = 0


class OrderTransfer(msgspec.Struct, kw_only=True, omit_defaults=True):
    """Settlement leg linked to a match on an order or user-trades page.

    Identify a match by ``(symbol_id, match_id)``. Deduplicate repeated
    settlement legs across pages by ``tx_id``.
    """

    match_id: str = ""
    symbol_id: int = 0
    asset_id: int = 0
    amount_e18: str = "0"
    is_debit: bool = False
    transfer_code: int = 0
    account_code: int = 0
    ts_ns: str = ""
    tx_id: str = ""


class AttachedRiskLegState(msgspec.Struct, kw_only=True, omit_defaults=True):
    """Runtime state for one attached take-profit, stop-loss, or trailing leg."""

    status: str = ""
    armed_ts_ns: str = ""
    terminal_ts_ns: str = ""
    trigger_id: str = ""
    child_order_id: str = ""


class RiskLeg(msgspec.Struct, kw_only=True, omit_defaults=True):
    trigger_price: Price | None = None
    trigger_price_source: str = ""
    order_type: str = ""
    limit_price: Price | None = None
    state: AttachedRiskLegState | None = None


class TrailingStop(msgspec.Struct, kw_only=True, omit_defaults=True):
    """Attached trailing-stop projection.

    Create/modify dicts must supply a positive ``trailing_distance_ticks`` or
    ``trailing_distance_bps`` (and positive slippage when set).
    ``trigger_price_source`` is ``last``, ``index`` or ``mark``; unset on a
    write means the last trade price. ``order_type`` is rejected if supplied
    under ``attached_risk.trailing_stop``.

    ``limit_price`` is the most the exit pays per unit when the trailing stop
    buys back: required when the order sells, unset when it buys, and at least
    ``activation_price`` when both are set. Order reads do not return it yet.
    """

    distance_ticks: int = 0
    distance_bps: int = 0
    max_slippage_ticks: int = 0
    max_slippage_bps: int = 0
    activation_price: Price | None = None
    limit_price: Price | None = None
    trigger_price_source: str = ""
    order_type: str = ""
    state: AttachedRiskLegState | None = None


class AttachedRisk(msgspec.Struct, kw_only=True, omit_defaults=True):
    take_profit: RiskLeg | None = None
    stop_loss: RiskLeg | None = None
    trailing_stop: TrailingStop | None = None
    oco: bool = False


class OrdersList(msgspec.Struct, kw_only=True, omit_defaults=True):
    orders: list[Order]
    next_page_token: str = ""


class OrderMutationResult(msgspec.Struct, kw_only=True, omit_defaults=True):
    status: str
    order_id: str = ""
    client_order_id: str = ""
    resolved_base_qty_scaled: str = ""
    resolved_base_qty: Quantity | None = None
    submitted_max_quote_debit_scaled: str = ""
    # Trigger IDs of the attached-risk legs this order configured; empty for a
    # leg the order does not have.
    take_profit_trigger_id: str = ""
    stop_loss_trigger_id: str = ""
    trailing_stop_trigger_id: str = ""


class OrderFieldViolation(msgspec.Struct, kw_only=True, omit_defaults=True):
    field_path: str = ""
    rule_id: str = ""
    message: str = ""


class OrderErrorDetail(msgspec.Struct, kw_only=True, omit_defaults=True):
    code: str = ""
    violations: list[OrderFieldViolation] = []
    rate_limit: RateLimitDetail | None = None


class PreviewOrderResult(msgspec.Struct, kw_only=True, omit_defaults=True):
    admissible: bool | None = None
    rejection: OrderErrorDetail | None = None
    resolved_base_qty_scaled: str = ""
    resolved_base_qty: Quantity | None = None
    # Protective execution boundary (not expected fill price).
    protected_price_bound: Price | None = None
    evaluated_at_ms: int = 0


class GetOrderResult(msgspec.Struct, kw_only=True, omit_defaults=True):
    order: Order | None = None
    trades: list[UserTrade] = []
    transfers: list[OrderTransfer] = []
    next_page_token: str = ""
    # True when the order's trades across every page add up to its filled
    # quantity; false while a recent execution is still being recorded.
    executions_complete: bool = False


class UserTrade(msgspec.Struct, kw_only=True, omit_defaults=True):
    symbol_id: int
    match_id: str = ""
    order_id: str = ""
    side: str = ""
    is_maker: bool = False
    price: Price | None = None
    qty: Quantity | None = None
    fee_amount_e18: str = "0"
    fee_asset: str = ""
    referral_share_amount_e18: str = "0"
    ts_ns: str = ""
    # True when fee_amount_e18 is a rebate credit instead of a fee debit.
    # Proto3 omits false, so sparse wire encoding only sets this for rebates.
    fee_is_rebate: bool = False
    lineage: OrderLineage | None = None


class UserTradesList(msgspec.Struct, kw_only=True, omit_defaults=True):
    trades: list[UserTrade]
    transfers: list[OrderTransfer] = []
    next_page_token: str = ""


class AssetBalance(msgspec.Struct, kw_only=True, omit_defaults=True):
    asset_id: int
    trading: str = "0"
    funding: str = "0"
    reserved: str = "0"
    available: str = "0"
    trading_revision: int = 0
    funding_revision: int = 0


class BalancesList(msgspec.Struct, kw_only=True, omit_defaults=True):
    balances: list[AssetBalance]


class ZipperReasonDetails(msgspec.Struct, kw_only=True, omit_defaults=True):
    code: int = 0
    reason_id: str = ""
    message: str = ""


class LifecycleFlowSummary(msgspec.Struct, kw_only=True, omit_defaults=True):
    intent_id: str
    flow_kind: str = ""
    latest_step: str = ""
    is_open: bool = False
    is_terminal: bool = False
    owner_account_id: str = ""
    smart_account_address: str = ""
    lifecycle_reason: str = "unspecified"
    zipper_reason: ZipperReasonDetails | None = None
    # True when an open flow has made no progress for well beyond its expected
    # step time. Always false for terminal flows and transaction lookups.
    is_delayed: bool = False


class LifecycleFlowsList(msgspec.Struct, kw_only=True, omit_defaults=True):
    flows: list[LifecycleFlowSummary]
    next_page_token: str = ""


class ModifyOrderResult(msgspec.Struct, kw_only=True, omit_defaults=True):
    action_taken: str = ""
    old_order_id: str = ""
    final_order_id: str = ""
    code: str = ""
    # Trigger IDs of the attached-risk legs this order configured; empty for a
    # leg the order does not have.
    take_profit_trigger_id: str = ""
    stop_loss_trigger_id: str = ""
    trailing_stop_trigger_id: str = ""


class CancelledOrder(msgspec.Struct, kw_only=True, omit_defaults=True):
    """One order whose cancellation a cancel-all requested."""

    order_id: str
    client_order_id: str = ""


class CancelAllOrdersResult(msgspec.Struct, kw_only=True, omit_defaults=True):
    """Cancel-all outcome.

    ``cancelled_orders`` lists up to 200 orders whose cancellation was
    requested, oldest first; ``total_cancelled`` counts all of them and
    ``truncated`` is true when the list is shorter than that. Each order's
    final state comes from the order stream and reads. Empty for a dry run.

    ``listing_status`` is ``included`` when ``cancelled_orders`` is the list
    for this request. A retry with the same ``request_id`` within 120 seconds
    returns the original counts with an empty ``cancelled_orders`` and
    ``not_retained_read_open_orders``: the empty list does not mean nothing
    was cancelled, so read open orders instead. An unknown value keeps its
    number.
    """

    status: str = ""
    matched_orders: int = 0
    submitted_cancels: int = 0
    failed_cancels: int = 0
    cancelled_orders: list[CancelledOrder] = []
    total_cancelled: int = 0
    truncated: bool = False
    listing_status: str = ""


class TriggerStopDetails(msgspec.Struct, kw_only=True, omit_defaults=True):
    trigger_price: Price | None = None
    trigger_price_source: str = ""
    trigger_direction: str = ""


class TriggerTrailingDetails(msgspec.Struct, kw_only=True, omit_defaults=True):
    """Runtime state of a trailing stop; ``trigger_price`` is the current
    threshold, which moves with the peak (sell) or trough (buy)."""

    trigger_price: Price | None = None
    trailing_distance: Price | None = None
    trailing_distance_bps: int = 0
    activation_price: Price | None = None
    peak_price: Price | None = None
    trough_price: Price | None = None
    max_slippage: Price | None = None
    max_slippage_bps: int = 0
    trigger_price_source: str = ""
    trigger_direction: str = ""


class TriggerTwapDetails(msgspec.Struct, kw_only=True, omit_defaults=True):
    twap_duration_ms: int = 0
    twap_slice_interval_ms: int = 0
    slice_idx: int = 0
    slice_count: int = 0
    executed_qty: Quantity | None = None


class TriggerLadderDetails(msgspec.Struct, kw_only=True, omit_defaults=True):
    ladder_price_min: Price | None = None
    ladder_price_max: Price | None = None
    ladder_levels: int = 0
    ladder_distribution: str = ""
    executed_levels: int = 0
    executed_qty: Quantity | None = None


class TriggerDetails(msgspec.Struct, kw_only=True, omit_defaults=True):
    """Discriminated trigger strategy payload. ``case`` is stop|trailing|twap|ladder."""

    case: str
    stop: TriggerStopDetails | None = None
    trailing: TriggerTrailingDetails | None = None
    twap: TriggerTwapDetails | None = None
    ladder: TriggerLadderDetails | None = None


class Trigger(msgspec.Struct, kw_only=True, omit_defaults=True):
    trigger_id: str = ""
    subaccount_id: str = ""
    symbol_id: int = 0
    symbol: str = ""
    trigger_type: str = ""
    status: str = ""
    parent_order_id: str = ""
    side: str = ""
    order_type: str = ""
    time_in_force: str = ""
    qty: Quantity | None = None
    limit_price: Price | None = None
    # Slippage cap of a stop-loss or take-profit market child: ``max_slippage``
    # in ticks (as a Price delta) or ``max_slippage_bps``; both unset means the
    # pair's default market slippage. Trailing stops report theirs on
    # ``details.trailing``.
    max_slippage: Price | None = None
    max_slippage_bps: int = 0
    fee_asset: str = ""
    self_trade_prevention_mode: str = ""
    post_only: bool = False
    trigger_price: Price | None = None
    # Price a stop-loss, take-profit or trailing stop watches: ``last``,
    # ``index`` or ``mark``. Pass it to ``triggers.create`` unchanged.
    trigger_price_source: str = ""
    client_trigger_id: str = ""
    created_at: datetime | None = None
    updated_at: datetime | None = None
    armed_at: datetime | None = None
    completed_at: datetime | None = None
    details: TriggerDetails | None = None
    cancel_reason: str = ""
    failure_reason: str = ""
    # 1 for the first state, higher for every later state change. Reads and
    # realtime updates carry the same version for the same state: keep the
    # copy with the highest version and ignore any copy that is not higher.
    # 0 from a server that does not send it.
    version: int = 0


class TriggersList(msgspec.Struct, kw_only=True, omit_defaults=True):
    triggers: list[Trigger]
    total: int = 0
    next_page_token: str = ""


class TriggerMutationResult(msgspec.Struct, kw_only=True, omit_defaults=True):
    trigger_id: str = ""
    status: str = ""


class TransferSide(msgspec.Struct, kw_only=True, omit_defaults=True):
    """One display side of a ledger transfer.

    ``kind`` is a snake_case label (funding_account, trading_account,
    external_address, private_counterparty, fee_account, system_account).
    ``chain_id`` is the Zipper ``ChainConfig.chain_id`` for external-address
    sides, not an EIP-155 or Polyester chain id.
    """

    kind: str = ""
    account_id: str = ""
    address: str = ""
    chain_id: int | None = None


class LedgerTransfer(msgspec.Struct, kw_only=True, omit_defaults=True):
    asset_id: int = 0
    amount: str = "0"
    transfer_type: int = 0
    account_code: int = 0
    timestamp: int = 0
    pending: bool = False
    tx_id: str = ""
    is_debit: bool = False
    source: TransferSide | None = None
    destination: TransferSide | None = None
    # Unsigned 128-bit decimal shared by both legs of one transfer; with
    # ``account_code`` it identifies a leg, so a repeated leg replaces the earlier copy.
    transfer_id: str = ""


class TransfersList(msgspec.Struct, kw_only=True, omit_defaults=True):
    transfers: list[LedgerTransfer]
    next_cursor: int | None = None


class InternalTransferResult(msgspec.Struct, kw_only=True, omit_defaults=True):
    request_id: str = ""
    transfer_id: str = ""
    asset_id: int = 0
    asset_code: str = ""
    quantity: AssetAmount | None = None


class DepositAddress(msgspec.Struct, kw_only=True, omit_defaults=True):
    chain_id: int = 0
    deposit_address: str = ""


class DepositAddressesList(msgspec.Struct, kw_only=True, omit_defaults=True):
    addresses: list[DepositAddress]


class TriggerEvent(msgspec.Struct, kw_only=True, omit_defaults=True):
    trigger_id: str = ""
    subaccount_id: str = ""
    symbol_id: int = 0
    trigger_type: str = ""
    event_type: str = ""
    ts_ns: str = ""
    child_seq: int = 0
    child_order_id: str = ""
    fire_price: Price | None = None
    cancel_reason: str = ""
    failure_reason: str = ""


class TriggerEventsList(msgspec.Struct, kw_only=True, omit_defaults=True):
    events: list[TriggerEvent]
    next_page_token: str = ""


class BalanceHistorySeries(msgspec.Struct, kw_only=True, omit_defaults=True):
    asset_id: int = 0
    account_code: int = 0
    balance_q: list[int] = []


class BalanceHistory(msgspec.Struct, kw_only=True, omit_defaults=True):
    range: str = ""
    bucket: str = ""
    start_ts_sec: int = 0
    end_ts_sec: int = 0
    points: int = 0
    series: list[BalanceHistorySeries] = []


class EquityHistorySeries(msgspec.Struct, kw_only=True, omit_defaults=True):
    account_code: int = 0
    account_name: str = ""
    asset_id: int = 0
    asset_symbol: str = ""
    portfolio_account_id: str = ""
    portfolio_remaining: bool = False
    equity_q: list[int] = []


class EquityHistory(msgspec.Struct, kw_only=True, omit_defaults=True):
    range: str = ""
    bucket: str = ""
    start_ts_sec: int = 0
    end_ts_sec: int = 0
    quote_asset: str = ""
    points: int = 0
    series: list[EquityHistorySeries] = []


class Hold(msgspec.Struct, kw_only=True, omit_defaults=True):
    hold_id: str = ""
    asset_id: int = 0
    amount_reserved: str = "0"
    expires_at_ns: str = "0"


class HoldsList(msgspec.Struct, kw_only=True, omit_defaults=True):
    holds: list[Hold]


class BucketTransferResult(msgspec.Struct, kw_only=True, omit_defaults=True):
    transfer_id: str = ""
    timestamp_ns: str = "0"


class ApiKeySummary(msgspec.Struct, kw_only=True, omit_defaults=True):
    key_id: str = ""
    label: str = ""
    status: str = ""
    subaccount_id: str = ""
    created_at: datetime | None = None
    last_used_at: datetime | None = None
    updated_at: datetime | None = None
    revision: int = 0


class ApiKeysList(msgspec.Struct, kw_only=True, omit_defaults=True):
    api_keys: list[ApiKeySummary]


class ResolvedAccount(msgspec.Struct, kw_only=True, omit_defaults=True):
    smart_account_address: str = ""
    kind: str = ""
    root_username: str = ""
    subaccount_label: str = ""
    account_id: str = ""


class ResolvedAccountsList(msgspec.Struct, kw_only=True, omit_defaults=True):
    matches: list[ResolvedAccount]


class TransferDestination(msgspec.Struct, kw_only=True, omit_defaults=True):
    account_id: str = ""
    subaccount_id: str = ""
    label: str = ""
    smart_account_address: str = ""


class TransferDestinationsList(msgspec.Struct, kw_only=True, omit_defaults=True):
    destinations: list[TransferDestination]


class BatchReplaceItem(msgspec.Struct, kw_only=True, omit_defaults=True):
    key: OrderKey
    new_price: Any | None = None
    new_qty: Any | None = None
    new_client_order_id: str | None = None


class BatchReplaceAdmissionItem(msgspec.Struct, kw_only=True, omit_defaults=True):
    """One item of a batch replace receipt.

    ``action_taken`` is ``"replaced"`` when a successor order was admitted and
    ``"amended"`` for a cancel-only outcome with no successor: keep tracking
    ``old_order_id`` until its terminal state is confirmed. Empty when unset.
    """

    item_index: int
    status: str = ""
    client_order_id: str = ""
    old_order_id: str = ""
    replacement_order_id: str = ""
    code: str = ""
    rate_limit: RateLimitDetail | None = None
    action_taken: str = ""


class BatchReplaceOrdersResult(msgspec.Struct, kw_only=True, omit_defaults=True):
    batch_request_id: str
    status: str
    results: list[BatchReplaceAdmissionItem]
    accepted_count: int = 0
    rejected_count: int = 0
    accepted_ts_ns: int = 0


class BatchReplaceStatusItem(msgspec.Struct, kw_only=True, omit_defaults=True):
    """One item of a batch replace status read; ``action_taken`` as on admission."""

    item_index: int
    phase: str
    old_order_id: str = ""
    replacement_order_id: str = ""
    order_status: str = ""
    code: str = ""
    updated_ts_ns: int = 0
    action_taken: str = ""


class BatchReplaceStatusResult(msgspec.Struct, kw_only=True, omit_defaults=True):
    batch_request_id: str
    admission_status: str
    items: list[BatchReplaceStatusItem]
    accepted_count: int = 0
    rejected_count: int = 0
    accepted_ts_ns: int = 0
    updated_ts_ns: int = 0


class BatchCreateResultItem(msgspec.Struct, kw_only=True, omit_defaults=True):
    status: str = ""
    order_id: str = ""
    client_order_id: str = ""
    code: str = ""
    rate_limit: RateLimitDetail | None = None
    # On a duplicate-client-order-ID rejection: the order that already holds the
    # client order ID, when known; empty otherwise.
    existing_order_id: str = ""
    # Trigger IDs of the attached-risk legs this order configured; empty for a
    # leg the order does not have.
    take_profit_trigger_id: str = ""
    stop_loss_trigger_id: str = ""
    trailing_stop_trigger_id: str = ""


class BatchCreateOrdersResult(msgspec.Struct, kw_only=True, omit_defaults=True):
    results: list[BatchCreateResultItem]
    accepted_count: int = 0
    rejected_count: int = 0


class BatchCancelResultItem(msgspec.Struct, kw_only=True, omit_defaults=True):
    status: str = ""
    order_id: str = ""
    client_order_id: str = ""
    code: str = ""
    rate_limit: RateLimitDetail | None = None


class BatchCancelOrdersResult(msgspec.Struct, kw_only=True, omit_defaults=True):
    results: list[BatchCancelResultItem]
    accepted_count: int = 0
    rejected_count: int = 0


class DeadManSwitchScope(msgspec.Struct, kw_only=True, omit_defaults=True):
    """Orders an armed cancel-all-after switch cancels on expiry.

    ``symbol_id`` 0 covers every symbol; an empty ``side`` covers both sides.
    Waiting triggers stay active when the switch expires.
    """

    account_id: str = ""
    symbol_id: int = 0
    side: str = ""


class CancelAllAfterResult(msgspec.Struct, kw_only=True, omit_defaults=True):
    status: str = ""
    effective_timeout_sec: int = 0
    expires_at_ts_ns: str = "0"
    # Scope the armed switch covers; None when the switch is disabled.
    effective_scope: DeadManSwitchScope | None = None


class WithdrawIntentResult(msgspec.Struct, kw_only=True, omit_defaults=True):
    intent_id: str = ""


class WithdrawDestinationValidation(msgspec.Struct, kw_only=True, omit_defaults=True):
    """User-safe outcome of ``WithdrawService.validate_destination``."""

    valid: bool = False
    code: str = "unspecified"
    message: str = ""
    canonical_destination_address: str = ""
