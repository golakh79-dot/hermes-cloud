from __future__ import annotations

from polyester.codecs.proto_helpers import has_field, proto_enum_name
from polyester.errors import PolyesterTransportError
from polyester.gen.chain.lifecycle.v1 import lifecycle_read_pb2, types_pb2
from polyester.gen.chain.zipper.v1 import reason_pb2
from polyester.models import LifecycleFlowsList, LifecycleFlowSummary, ZipperReasonDetails
from polyester.services._scope import lifecycle_account_fields

FlowDetailView = lifecycle_read_pb2.FlowDetailView
FlowSummaryView = lifecycle_read_pb2.FlowSummaryView
FlowTxMatchView = lifecycle_read_pb2.FlowTxMatchView

# Explicit catalog keyed by wire int (matches TS LifecycleFlowReasonCodec).
# Proto3 enums are open; unknown codes must not fail the whole flow payload.
_LIFECYCLE_REASON_BY_CODE: dict[int, str] = {
    int(types_pb2.REASON_UNSPECIFIED): "unspecified",
    int(types_pb2.ZIPPER_VALIDATION_REJECTED): "zipper_validation_rejected",
    int(types_pb2.ZIPPER_EXECUTION_REJECTED): "zipper_execution_rejected",
    int(types_pb2.ZIPPER_WITHDRAW_EXECUTION_FAILED): "zipper_withdraw_execution_failed",
    int(types_pb2.ZIPPER_DEPOSIT_REFUND_FAILED): "zipper_deposit_refund_failed",
    int(types_pb2.LEDGER_MIRROR_REJECTED): "ledger_mirror_rejected",
    int(types_pb2.LEDGER_MIRROR_TRANSFER_EXCEEDS_CREDITS): (
        "ledger_mirror_transfer_exceeds_credits"
    ),
    int(types_pb2.LEDGER_MIRROR_TRANSFER_EXISTS): "ledger_mirror_transfer_exists",
    int(types_pb2.LEDGER_MIRROR_PENDING_TRANSFER_NOT_FOUND): (
        "ledger_mirror_pending_transfer_not_found"
    ),
    int(types_pb2.LEDGER_MIRROR_TRANSFER_ID_ALREADY_FAILED): (
        "ledger_mirror_transfer_id_already_failed"
    ),
    int(types_pb2.TRADING_WITHDRAW_POLICY_DENIED): "trading_withdraw_policy_denied",
    int(types_pb2.TRADING_WITHDRAW_CONTRACT_REVERTED): (
        "trading_withdraw_contract_reverted"
    ),
    int(types_pb2.TRADING_WITHDRAW_EXECUTION_FAILED): (
        "trading_withdraw_execution_failed"
    ),
    int(types_pb2.DEPOSIT_SOURCE_NOT_CONFIRMED): "deposit_source_not_confirmed",
}


def lifecycle_reason_from_code(code: int) -> str:
    return _LIFECYCLE_REASON_BY_CODE.get(int(code), f"unknown_reason_{int(code)}")


def _flow_kind_label(code: int) -> str:
    return proto_enum_name(types_pb2.FlowKind, code) or "unspecified"


def _flow_step_label(code: int) -> str:
    return proto_enum_name(lifecycle_read_pb2.FlowStep, code) or "unspecified"


def _zipper_reason_from_proto(msg: reason_pb2.ZipperReasonDetails) -> ZipperReasonDetails:
    return ZipperReasonDetails(
        code=int(msg.code),
        reason_id=str(msg.reason_id or ""),
        message=str(msg.message or ""),
    )


def _zipper_reason_if_present(msg) -> ZipperReasonDetails | None:
    if has_field(msg, "zipper_reason"):
        return _zipper_reason_from_proto(msg.zipper_reason)
    return None


def _summary_from_detail(msg: FlowDetailView) -> FlowSummaryView:
    if msg.HasField("summary"):
        return msg.summary
    raise PolyesterTransportError("flow detail response is missing summary")


def flow_summary_from_proto(msg: lifecycle_read_pb2.FlowSummaryView) -> LifecycleFlowSummary:
    account_fields = lifecycle_account_fields(msg)
    return LifecycleFlowSummary(
        intent_id=msg.flow_id,
        flow_kind=_flow_kind_label(msg.flow_kind),
        latest_step=_flow_step_label(msg.current_step),
        is_open=bool(msg.is_open),
        is_terminal=bool(msg.is_terminal),
        owner_account_id=account_fields.get("owner_account_id", ""),
        smart_account_address=account_fields.get("smart_account_address", ""),
        lifecycle_reason=lifecycle_reason_from_code(int(msg.lifecycle_reason)),
        zipper_reason=_zipper_reason_if_present(msg),
        is_delayed=bool(msg.is_delayed),
    )


def flow_tx_match_from_proto(msg: FlowTxMatchView) -> LifecycleFlowSummary:
    account_fields = lifecycle_account_fields(msg)
    return LifecycleFlowSummary(
        intent_id=msg.flow_id,
        flow_kind=_flow_kind_label(msg.flow_kind),
        latest_step=_flow_step_label(msg.current_step),
        is_open=bool(msg.is_open),
        is_terminal=bool(msg.is_terminal),
        owner_account_id=account_fields.get("owner_account_id", ""),
        smart_account_address=account_fields.get("smart_account_address", ""),
        lifecycle_reason=lifecycle_reason_from_code(int(msg.lifecycle_reason)),
        zipper_reason=_zipper_reason_if_present(msg),
    )


def flow_detail_from_proto(msg: lifecycle_read_pb2.FlowDetailView) -> LifecycleFlowSummary:
    return flow_summary_from_proto(_summary_from_detail(msg))


def flows_list_from_proto(msg: lifecycle_read_pb2.ListFlowsResponse) -> LifecycleFlowsList:
    return LifecycleFlowsList(
        flows=[flow_summary_from_proto(item) for item in msg.flows],
        next_page_token=msg.next_page_token,
    )


def flows_by_tx_list_from_proto(
    msg: lifecycle_read_pb2.ListFlowsByTxResponse,
) -> LifecycleFlowsList:
    return LifecycleFlowsList(
        flows=[flow_tx_match_from_proto(item) for item in msg.matches],
        next_page_token=msg.next_page_token,
    )


def flow_from_get_response(msg: lifecycle_read_pb2.GetFlowResponse) -> LifecycleFlowSummary:
    if msg.HasField("flow"):
        return flow_detail_from_proto(msg.flow)
    raise PolyesterTransportError("get flow response is missing flow")


def flow_from_get_by_tx_response(
    msg: lifecycle_read_pb2.ListFlowsByTxResponse,
) -> LifecycleFlowsList:
    """Decode every flow in a transaction lookup response.

    The legacy helper name is retained for compatibility, but transaction
    lookups are one-to-many and must not silently discard bundled flows.
    """
    return flows_by_tx_list_from_proto(msg)
