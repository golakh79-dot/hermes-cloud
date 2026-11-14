from polyester.gen.buf.validate import validate_pb2 as _validate_pb2
from polyester.gen.chain.lifecycle.v1 import types_pb2 as _types_pb2
from polyester.gen.chain.zipper.v1 import reason_pb2 as _reason_pb2
from polyester.gen.gnostic.openapi.v3 import annotations_pb2 as _annotations_pb2
from polyester.gen.google.api import annotations_pb2 as _annotations_pb2_1
from polyester.gen.polyester.api import options_pb2 as _options_pb2
from polyester.gen.polyester.api.validation.v1 import predefined_string_rules_pb2 as _predefined_string_rules_pb2
from polyester.gen.polyester.type.v1 import u128_pb2 as _u128_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TxLookupKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TX_UNSPECIFIED: _ClassVar[TxLookupKind]
    TX_SOURCE: _ClassVar[TxLookupKind]
    TX_ANY: _ClassVar[TxLookupKind]

class ListScope(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LIST_UNSPECIFIED: _ClassVar[ListScope]
    LIST_ALL: _ClassVar[ListScope]
    LIST_OPEN_ONLY: _ClassVar[ListScope]
    LIST_TERMINAL_ONLY: _ClassVar[ListScope]

class Sort(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SORT_UNSPECIFIED: _ClassVar[Sort]
    SORT_NEWEST: _ClassVar[Sort]
    SORT_OLDEST: _ClassVar[Sort]

class ListOrderBy(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ORDER_BY_UNSPECIFIED: _ClassVar[ListOrderBy]
    ORDER_BY_LAST_ACTIVITY: _ClassVar[ListOrderBy]
    ORDER_BY_STARTED_AT: _ClassVar[ListOrderBy]

class FlowStep(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FLOW_STEP_UNSPECIFIED: _ClassVar[FlowStep]
    FLOW_STEP_SOURCE: _ClassVar[FlowStep]
    FLOW_STEP_TRANSFER: _ClassVar[FlowStep]
    FLOW_STEP_REQUEST: _ClassVar[FlowStep]
    FLOW_STEP_VALIDATION: _ClassVar[FlowStep]
    FLOW_STEP_EXECUTION: _ClassVar[FlowStep]
    FLOW_STEP_BRIDGE_FULFILLMENT: _ClassVar[FlowStep]
    FLOW_STEP_DROPPED: _ClassVar[FlowStep]
    FLOW_STEP_FAILED: _ClassVar[FlowStep]
    FLOW_STEP_REFUNDED: _ClassVar[FlowStep]
    FLOW_STEP_FULFILLING: _ClassVar[FlowStep]
    FLOW_STEP_SETTLEMENT: _ClassVar[FlowStep]

class FlowStepActivityKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ACTIVITY_UNSPECIFIED: _ClassVar[FlowStepActivityKind]
    ACTIVITY_MINTED: _ClassVar[FlowStepActivityKind]
    ACTIVITY_FUNDING: _ClassVar[FlowStepActivityKind]
    ACTIVITY_TRADING: _ClassVar[FlowStepActivityKind]

class FlowTimelineStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TIMELINE_STATUS_UNSPECIFIED: _ClassVar[FlowTimelineStatus]
    TIMELINE_STATUS_COMPLETED: _ClassVar[FlowTimelineStatus]
    TIMELINE_STATUS_CURRENT: _ClassVar[FlowTimelineStatus]
    TIMELINE_STATUS_PLANNED: _ClassVar[FlowTimelineStatus]
TX_UNSPECIFIED: TxLookupKind
TX_SOURCE: TxLookupKind
TX_ANY: TxLookupKind
LIST_UNSPECIFIED: ListScope
LIST_ALL: ListScope
LIST_OPEN_ONLY: ListScope
LIST_TERMINAL_ONLY: ListScope
SORT_UNSPECIFIED: Sort
SORT_NEWEST: Sort
SORT_OLDEST: Sort
ORDER_BY_UNSPECIFIED: ListOrderBy
ORDER_BY_LAST_ACTIVITY: ListOrderBy
ORDER_BY_STARTED_AT: ListOrderBy
FLOW_STEP_UNSPECIFIED: FlowStep
FLOW_STEP_SOURCE: FlowStep
FLOW_STEP_TRANSFER: FlowStep
FLOW_STEP_REQUEST: FlowStep
FLOW_STEP_VALIDATION: FlowStep
FLOW_STEP_EXECUTION: FlowStep
FLOW_STEP_BRIDGE_FULFILLMENT: FlowStep
FLOW_STEP_DROPPED: FlowStep
FLOW_STEP_FAILED: FlowStep
FLOW_STEP_REFUNDED: FlowStep
FLOW_STEP_FULFILLING: FlowStep
FLOW_STEP_SETTLEMENT: FlowStep
ACTIVITY_UNSPECIFIED: FlowStepActivityKind
ACTIVITY_MINTED: FlowStepActivityKind
ACTIVITY_FUNDING: FlowStepActivityKind
ACTIVITY_TRADING: FlowStepActivityKind
TIMELINE_STATUS_UNSPECIFIED: FlowTimelineStatus
TIMELINE_STATUS_COMPLETED: FlowTimelineStatus
TIMELINE_STATUS_CURRENT: FlowTimelineStatus
TIMELINE_STATUS_PLANNED: FlowTimelineStatus

class GetFlowResponse(_message.Message):
    __slots__ = ("flow",)
    FLOW_FIELD_NUMBER: _ClassVar[int]
    flow: FlowDetailView
    def __init__(self, flow: _Optional[_Union[FlowDetailView, _Mapping]] = ...) -> None: ...

class GetFlowByIdRequest(_message.Message):
    __slots__ = ("flow_id",)
    FLOW_ID_FIELD_NUMBER: _ClassVar[int]
    flow_id: str
    def __init__(self, flow_id: _Optional[str] = ...) -> None: ...

class ListFlowsByTxRequest(_message.Message):
    __slots__ = ("tx_hash", "lookup_kind", "limit", "page_token")
    TX_HASH_FIELD_NUMBER: _ClassVar[int]
    LOOKUP_KIND_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    tx_hash: str
    lookup_kind: TxLookupKind
    limit: int
    page_token: str
    def __init__(self, tx_hash: _Optional[str] = ..., lookup_kind: _Optional[_Union[TxLookupKind, str]] = ..., limit: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class ListFlowsRequest(_message.Message):
    __slots__ = ("limit", "sort", "flow_kind", "flow_state", "tx_ref", "scope", "owner_account_id", "smart_account_address", "polyester_chain_ids", "zipped_asset_ids", "unified_asset_ids", "page_token", "order_by")
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    SORT_FIELD_NUMBER: _ClassVar[int]
    FLOW_KIND_FIELD_NUMBER: _ClassVar[int]
    FLOW_STATE_FIELD_NUMBER: _ClassVar[int]
    TX_REF_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    OWNER_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    SMART_ACCOUNT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    POLYESTER_CHAIN_IDS_FIELD_NUMBER: _ClassVar[int]
    ZIPPED_ASSET_IDS_FIELD_NUMBER: _ClassVar[int]
    UNIFIED_ASSET_IDS_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    ORDER_BY_FIELD_NUMBER: _ClassVar[int]
    limit: int
    sort: Sort
    flow_kind: _types_pb2.FlowKind
    flow_state: _types_pb2.FlowState
    tx_ref: str
    scope: ListScope
    owner_account_id: int
    smart_account_address: str
    polyester_chain_ids: _containers.RepeatedScalarFieldContainer[int]
    zipped_asset_ids: _containers.RepeatedScalarFieldContainer[int]
    unified_asset_ids: _containers.RepeatedScalarFieldContainer[int]
    page_token: str
    order_by: ListOrderBy
    def __init__(self, limit: _Optional[int] = ..., sort: _Optional[_Union[Sort, str]] = ..., flow_kind: _Optional[_Union[_types_pb2.FlowKind, str]] = ..., flow_state: _Optional[_Union[_types_pb2.FlowState, str]] = ..., tx_ref: _Optional[str] = ..., scope: _Optional[_Union[ListScope, str]] = ..., owner_account_id: _Optional[int] = ..., smart_account_address: _Optional[str] = ..., polyester_chain_ids: _Optional[_Iterable[int]] = ..., zipped_asset_ids: _Optional[_Iterable[int]] = ..., unified_asset_ids: _Optional[_Iterable[int]] = ..., page_token: _Optional[str] = ..., order_by: _Optional[_Union[ListOrderBy, str]] = ...) -> None: ...

class ListFlowsResponse(_message.Message):
    __slots__ = ("flows", "next_page_token")
    FLOWS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    flows: _containers.RepeatedCompositeFieldContainer[FlowSummaryView]
    next_page_token: str
    def __init__(self, flows: _Optional[_Iterable[_Union[FlowSummaryView, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class FlowTxMatchView(_message.Message):
    __slots__ = ("flow_id", "flow_kind", "source_tx_hash", "latest_tx_ref", "tx_occurrence_index", "source_domain", "destination_domain", "current_step", "is_open", "is_terminal", "asset_ids", "polyester_chain_id", "amount_e18", "source_address", "destination_address", "lifecycle_reason", "last_activity_at_unix_ms", "owner_account_id", "smart_account_address", "zipper_reason")
    FLOW_ID_FIELD_NUMBER: _ClassVar[int]
    FLOW_KIND_FIELD_NUMBER: _ClassVar[int]
    SOURCE_TX_HASH_FIELD_NUMBER: _ClassVar[int]
    LATEST_TX_REF_FIELD_NUMBER: _ClassVar[int]
    TX_OCCURRENCE_INDEX_FIELD_NUMBER: _ClassVar[int]
    SOURCE_DOMAIN_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_DOMAIN_FIELD_NUMBER: _ClassVar[int]
    CURRENT_STEP_FIELD_NUMBER: _ClassVar[int]
    IS_OPEN_FIELD_NUMBER: _ClassVar[int]
    IS_TERMINAL_FIELD_NUMBER: _ClassVar[int]
    ASSET_IDS_FIELD_NUMBER: _ClassVar[int]
    POLYESTER_CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_E18_FIELD_NUMBER: _ClassVar[int]
    SOURCE_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    LIFECYCLE_REASON_FIELD_NUMBER: _ClassVar[int]
    LAST_ACTIVITY_AT_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    OWNER_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    SMART_ACCOUNT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    ZIPPER_REASON_FIELD_NUMBER: _ClassVar[int]
    flow_id: str
    flow_kind: _types_pb2.FlowKind
    source_tx_hash: str
    latest_tx_ref: str
    tx_occurrence_index: int
    source_domain: _types_pb2.FlowDomain
    destination_domain: _types_pb2.FlowDomain
    current_step: FlowStep
    is_open: bool
    is_terminal: bool
    asset_ids: _types_pb2.AssetIds
    polyester_chain_id: int
    amount_e18: _u128_pb2.U128
    source_address: str
    destination_address: str
    lifecycle_reason: _types_pb2.LifecycleReason
    last_activity_at_unix_ms: int
    owner_account_id: int
    smart_account_address: str
    zipper_reason: _reason_pb2.ZipperReasonDetails
    def __init__(self, flow_id: _Optional[str] = ..., flow_kind: _Optional[_Union[_types_pb2.FlowKind, str]] = ..., source_tx_hash: _Optional[str] = ..., latest_tx_ref: _Optional[str] = ..., tx_occurrence_index: _Optional[int] = ..., source_domain: _Optional[_Union[_types_pb2.FlowDomain, str]] = ..., destination_domain: _Optional[_Union[_types_pb2.FlowDomain, str]] = ..., current_step: _Optional[_Union[FlowStep, str]] = ..., is_open: _Optional[bool] = ..., is_terminal: _Optional[bool] = ..., asset_ids: _Optional[_Union[_types_pb2.AssetIds, _Mapping]] = ..., polyester_chain_id: _Optional[int] = ..., amount_e18: _Optional[_Union[_u128_pb2.U128, _Mapping]] = ..., source_address: _Optional[str] = ..., destination_address: _Optional[str] = ..., lifecycle_reason: _Optional[_Union[_types_pb2.LifecycleReason, str]] = ..., last_activity_at_unix_ms: _Optional[int] = ..., owner_account_id: _Optional[int] = ..., smart_account_address: _Optional[str] = ..., zipper_reason: _Optional[_Union[_reason_pb2.ZipperReasonDetails, _Mapping]] = ...) -> None: ...

class ListFlowsByTxResponse(_message.Message):
    __slots__ = ("tx_hash", "matches", "next_page_token")
    TX_HASH_FIELD_NUMBER: _ClassVar[int]
    MATCHES_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    tx_hash: str
    matches: _containers.RepeatedCompositeFieldContainer[FlowTxMatchView]
    next_page_token: str
    def __init__(self, tx_hash: _Optional[str] = ..., matches: _Optional[_Iterable[_Union[FlowTxMatchView, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class FlowSummaryView(_message.Message):
    __slots__ = ("owner_account_id", "smart_account_address", "flow_id", "flow_kind", "current_step", "asset_ids", "polyester_chain_id", "amount_e18", "request_fee", "source_tx_hash", "tx_occurrence_index", "source_address", "destination_address", "latest_tx_ref", "source_domain", "destination_domain", "latest_lifecycle_source", "lifecycle_reason", "zipper_reason", "started_at_unix_ms", "updated_at_unix_ms", "terminal_at_unix_ms", "last_activity_at_unix_ms", "is_open", "is_terminal", "current_step_sequence", "current_progress", "progress_timeline", "estimated_completion_unix_ms", "is_delayed")
    OWNER_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    SMART_ACCOUNT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    FLOW_ID_FIELD_NUMBER: _ClassVar[int]
    FLOW_KIND_FIELD_NUMBER: _ClassVar[int]
    CURRENT_STEP_FIELD_NUMBER: _ClassVar[int]
    ASSET_IDS_FIELD_NUMBER: _ClassVar[int]
    POLYESTER_CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_E18_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FEE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_TX_HASH_FIELD_NUMBER: _ClassVar[int]
    TX_OCCURRENCE_INDEX_FIELD_NUMBER: _ClassVar[int]
    SOURCE_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    LATEST_TX_REF_FIELD_NUMBER: _ClassVar[int]
    SOURCE_DOMAIN_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_DOMAIN_FIELD_NUMBER: _ClassVar[int]
    LATEST_LIFECYCLE_SOURCE_FIELD_NUMBER: _ClassVar[int]
    LIFECYCLE_REASON_FIELD_NUMBER: _ClassVar[int]
    ZIPPER_REASON_FIELD_NUMBER: _ClassVar[int]
    STARTED_AT_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    TERMINAL_AT_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    LAST_ACTIVITY_AT_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    IS_OPEN_FIELD_NUMBER: _ClassVar[int]
    IS_TERMINAL_FIELD_NUMBER: _ClassVar[int]
    CURRENT_STEP_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    CURRENT_PROGRESS_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_TIMELINE_FIELD_NUMBER: _ClassVar[int]
    ESTIMATED_COMPLETION_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    IS_DELAYED_FIELD_NUMBER: _ClassVar[int]
    owner_account_id: int
    smart_account_address: str
    flow_id: str
    flow_kind: _types_pb2.FlowKind
    current_step: FlowStep
    asset_ids: _types_pb2.AssetIds
    polyester_chain_id: int
    amount_e18: _u128_pb2.U128
    request_fee: _types_pb2.RequestFee
    source_tx_hash: str
    tx_occurrence_index: int
    source_address: str
    destination_address: str
    latest_tx_ref: str
    source_domain: _types_pb2.FlowDomain
    destination_domain: _types_pb2.FlowDomain
    latest_lifecycle_source: _types_pb2.LifecycleSource
    lifecycle_reason: _types_pb2.LifecycleReason
    zipper_reason: _reason_pb2.ZipperReasonDetails
    started_at_unix_ms: int
    updated_at_unix_ms: int
    terminal_at_unix_ms: int
    last_activity_at_unix_ms: int
    is_open: bool
    is_terminal: bool
    current_step_sequence: int
    current_progress: FlowSummaryProgressView
    progress_timeline: _containers.RepeatedCompositeFieldContainer[FlowTimelineItemView]
    estimated_completion_unix_ms: int
    is_delayed: bool
    def __init__(self, owner_account_id: _Optional[int] = ..., smart_account_address: _Optional[str] = ..., flow_id: _Optional[str] = ..., flow_kind: _Optional[_Union[_types_pb2.FlowKind, str]] = ..., current_step: _Optional[_Union[FlowStep, str]] = ..., asset_ids: _Optional[_Union[_types_pb2.AssetIds, _Mapping]] = ..., polyester_chain_id: _Optional[int] = ..., amount_e18: _Optional[_Union[_u128_pb2.U128, _Mapping]] = ..., request_fee: _Optional[_Union[_types_pb2.RequestFee, _Mapping]] = ..., source_tx_hash: _Optional[str] = ..., tx_occurrence_index: _Optional[int] = ..., source_address: _Optional[str] = ..., destination_address: _Optional[str] = ..., latest_tx_ref: _Optional[str] = ..., source_domain: _Optional[_Union[_types_pb2.FlowDomain, str]] = ..., destination_domain: _Optional[_Union[_types_pb2.FlowDomain, str]] = ..., latest_lifecycle_source: _Optional[_Union[_types_pb2.LifecycleSource, str]] = ..., lifecycle_reason: _Optional[_Union[_types_pb2.LifecycleReason, str]] = ..., zipper_reason: _Optional[_Union[_reason_pb2.ZipperReasonDetails, _Mapping]] = ..., started_at_unix_ms: _Optional[int] = ..., updated_at_unix_ms: _Optional[int] = ..., terminal_at_unix_ms: _Optional[int] = ..., last_activity_at_unix_ms: _Optional[int] = ..., is_open: _Optional[bool] = ..., is_terminal: _Optional[bool] = ..., current_step_sequence: _Optional[int] = ..., current_progress: _Optional[_Union[FlowSummaryProgressView, _Mapping]] = ..., progress_timeline: _Optional[_Iterable[_Union[FlowTimelineItemView, _Mapping]]] = ..., estimated_completion_unix_ms: _Optional[int] = ..., is_delayed: _Optional[bool] = ...) -> None: ...

class FlowSummaryProgressView(_message.Message):
    __slots__ = ("current_step_started_at_unix_ms", "current_step_expected_duration_ms", "current_confirmations", "required_confirmations", "approve_count", "reject_count", "validator_count", "required_approvals", "required_rejections")
    CURRENT_STEP_STARTED_AT_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    CURRENT_STEP_EXPECTED_DURATION_MS_FIELD_NUMBER: _ClassVar[int]
    CURRENT_CONFIRMATIONS_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_CONFIRMATIONS_FIELD_NUMBER: _ClassVar[int]
    APPROVE_COUNT_FIELD_NUMBER: _ClassVar[int]
    REJECT_COUNT_FIELD_NUMBER: _ClassVar[int]
    VALIDATOR_COUNT_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_APPROVALS_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_REJECTIONS_FIELD_NUMBER: _ClassVar[int]
    current_step_started_at_unix_ms: int
    current_step_expected_duration_ms: int
    current_confirmations: int
    required_confirmations: int
    approve_count: int
    reject_count: int
    validator_count: int
    required_approvals: int
    required_rejections: int
    def __init__(self, current_step_started_at_unix_ms: _Optional[int] = ..., current_step_expected_duration_ms: _Optional[int] = ..., current_confirmations: _Optional[int] = ..., required_confirmations: _Optional[int] = ..., approve_count: _Optional[int] = ..., reject_count: _Optional[int] = ..., validator_count: _Optional[int] = ..., required_approvals: _Optional[int] = ..., required_rejections: _Optional[int] = ...) -> None: ...

class FlowStepView(_message.Message):
    __slots__ = ("sequence", "step", "asset_ids", "polyester_chain_id", "amount_e18", "request_fee", "milestone_tx_ref", "milestone_tx_chain_id", "lifecycle_source", "lifecycle_reason", "zipper_reason", "current_confirmations", "required_confirmations", "approve_count", "reject_count", "validator_count", "required_approvals", "required_rejections", "occurred_at_unix_ms", "block_time_moving_average_ms", "activities")
    SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    STEP_FIELD_NUMBER: _ClassVar[int]
    ASSET_IDS_FIELD_NUMBER: _ClassVar[int]
    POLYESTER_CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_E18_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FEE_FIELD_NUMBER: _ClassVar[int]
    MILESTONE_TX_REF_FIELD_NUMBER: _ClassVar[int]
    MILESTONE_TX_CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    LIFECYCLE_SOURCE_FIELD_NUMBER: _ClassVar[int]
    LIFECYCLE_REASON_FIELD_NUMBER: _ClassVar[int]
    ZIPPER_REASON_FIELD_NUMBER: _ClassVar[int]
    CURRENT_CONFIRMATIONS_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_CONFIRMATIONS_FIELD_NUMBER: _ClassVar[int]
    APPROVE_COUNT_FIELD_NUMBER: _ClassVar[int]
    REJECT_COUNT_FIELD_NUMBER: _ClassVar[int]
    VALIDATOR_COUNT_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_APPROVALS_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_REJECTIONS_FIELD_NUMBER: _ClassVar[int]
    OCCURRED_AT_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    BLOCK_TIME_MOVING_AVERAGE_MS_FIELD_NUMBER: _ClassVar[int]
    ACTIVITIES_FIELD_NUMBER: _ClassVar[int]
    sequence: int
    step: FlowStep
    asset_ids: _types_pb2.AssetIds
    polyester_chain_id: int
    amount_e18: _u128_pb2.U128
    request_fee: _types_pb2.RequestFee
    milestone_tx_ref: str
    milestone_tx_chain_id: int
    lifecycle_source: _types_pb2.LifecycleSource
    lifecycle_reason: _types_pb2.LifecycleReason
    zipper_reason: _reason_pb2.ZipperReasonDetails
    current_confirmations: int
    required_confirmations: int
    approve_count: int
    reject_count: int
    validator_count: int
    required_approvals: int
    required_rejections: int
    occurred_at_unix_ms: int
    block_time_moving_average_ms: int
    activities: _containers.RepeatedCompositeFieldContainer[FlowStepActivityView]
    def __init__(self, sequence: _Optional[int] = ..., step: _Optional[_Union[FlowStep, str]] = ..., asset_ids: _Optional[_Union[_types_pb2.AssetIds, _Mapping]] = ..., polyester_chain_id: _Optional[int] = ..., amount_e18: _Optional[_Union[_u128_pb2.U128, _Mapping]] = ..., request_fee: _Optional[_Union[_types_pb2.RequestFee, _Mapping]] = ..., milestone_tx_ref: _Optional[str] = ..., milestone_tx_chain_id: _Optional[int] = ..., lifecycle_source: _Optional[_Union[_types_pb2.LifecycleSource, str]] = ..., lifecycle_reason: _Optional[_Union[_types_pb2.LifecycleReason, str]] = ..., zipper_reason: _Optional[_Union[_reason_pb2.ZipperReasonDetails, _Mapping]] = ..., current_confirmations: _Optional[int] = ..., required_confirmations: _Optional[int] = ..., approve_count: _Optional[int] = ..., reject_count: _Optional[int] = ..., validator_count: _Optional[int] = ..., required_approvals: _Optional[int] = ..., required_rejections: _Optional[int] = ..., occurred_at_unix_ms: _Optional[int] = ..., block_time_moving_average_ms: _Optional[int] = ..., activities: _Optional[_Iterable[_Union[FlowStepActivityView, _Mapping]]] = ...) -> None: ...

class FlowStepActivityView(_message.Message):
    __slots__ = ("sequence", "tx_ref", "tx_chain_id", "occurred_at_unix_ms", "lifecycle_source", "lifecycle_reason", "zipper_reason", "current_confirmations", "required_confirmations", "approve_count", "reject_count", "validator_count", "kind", "required_approvals", "required_rejections", "amount_e18", "ledger_transfer_id")
    SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    TX_REF_FIELD_NUMBER: _ClassVar[int]
    TX_CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    OCCURRED_AT_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    LIFECYCLE_SOURCE_FIELD_NUMBER: _ClassVar[int]
    LIFECYCLE_REASON_FIELD_NUMBER: _ClassVar[int]
    ZIPPER_REASON_FIELD_NUMBER: _ClassVar[int]
    CURRENT_CONFIRMATIONS_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_CONFIRMATIONS_FIELD_NUMBER: _ClassVar[int]
    APPROVE_COUNT_FIELD_NUMBER: _ClassVar[int]
    REJECT_COUNT_FIELD_NUMBER: _ClassVar[int]
    VALIDATOR_COUNT_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_APPROVALS_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_REJECTIONS_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_E18_FIELD_NUMBER: _ClassVar[int]
    LEDGER_TRANSFER_ID_FIELD_NUMBER: _ClassVar[int]
    sequence: int
    tx_ref: str
    tx_chain_id: int
    occurred_at_unix_ms: int
    lifecycle_source: _types_pb2.LifecycleSource
    lifecycle_reason: _types_pb2.LifecycleReason
    zipper_reason: _reason_pb2.ZipperReasonDetails
    current_confirmations: int
    required_confirmations: int
    approve_count: int
    reject_count: int
    validator_count: int
    kind: FlowStepActivityKind
    required_approvals: int
    required_rejections: int
    amount_e18: _u128_pb2.U128
    ledger_transfer_id: str
    def __init__(self, sequence: _Optional[int] = ..., tx_ref: _Optional[str] = ..., tx_chain_id: _Optional[int] = ..., occurred_at_unix_ms: _Optional[int] = ..., lifecycle_source: _Optional[_Union[_types_pb2.LifecycleSource, str]] = ..., lifecycle_reason: _Optional[_Union[_types_pb2.LifecycleReason, str]] = ..., zipper_reason: _Optional[_Union[_reason_pb2.ZipperReasonDetails, _Mapping]] = ..., current_confirmations: _Optional[int] = ..., required_confirmations: _Optional[int] = ..., approve_count: _Optional[int] = ..., reject_count: _Optional[int] = ..., validator_count: _Optional[int] = ..., kind: _Optional[_Union[FlowStepActivityKind, str]] = ..., required_approvals: _Optional[int] = ..., required_rejections: _Optional[int] = ..., amount_e18: _Optional[_Union[_u128_pb2.U128, _Mapping]] = ..., ledger_transfer_id: _Optional[str] = ...) -> None: ...

class FlowTimelineItemView(_message.Message):
    __slots__ = ("sequence", "step", "status", "expected_duration_ms")
    SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    STEP_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_DURATION_MS_FIELD_NUMBER: _ClassVar[int]
    sequence: int
    step: FlowStep
    status: FlowTimelineStatus
    expected_duration_ms: int
    def __init__(self, sequence: _Optional[int] = ..., step: _Optional[_Union[FlowStep, str]] = ..., status: _Optional[_Union[FlowTimelineStatus, str]] = ..., expected_duration_ms: _Optional[int] = ...) -> None: ...

class FlowDetailView(_message.Message):
    __slots__ = ("summary", "observed_steps", "from_live_state")
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    OBSERVED_STEPS_FIELD_NUMBER: _ClassVar[int]
    FROM_LIVE_STATE_FIELD_NUMBER: _ClassVar[int]
    summary: FlowSummaryView
    observed_steps: _containers.RepeatedCompositeFieldContainer[FlowStepView]
    from_live_state: bool
    def __init__(self, summary: _Optional[_Union[FlowSummaryView, _Mapping]] = ..., observed_steps: _Optional[_Iterable[_Union[FlowStepView, _Mapping]]] = ..., from_live_state: _Optional[bool] = ...) -> None: ...
