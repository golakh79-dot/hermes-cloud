import datetime

from polyester.gen.buf.validate import validate_pb2 as _validate_pb2
from polyester.gen.gnostic.openapi.v3 import annotations_pb2 as _annotations_pb2
from polyester.gen.google.api import annotations_pb2 as _annotations_pb2_1
from polyester.gen.google.api import field_behavior_pb2 as _field_behavior_pb2
from google.protobuf import field_mask_pb2 as _field_mask_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from polyester.gen.polyester.api import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PolicyAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNSPECIFIED: _ClassVar[PolicyAction]
    TRADE_SPOT: _ClassVar[PolicyAction]
    INTERNAL_TRANSFER: _ClassVar[PolicyAction]
    EXTERNAL_WITHDRAW: _ClassVar[PolicyAction]
    READ_BALANCES: _ClassVar[PolicyAction]
    READ_SPOT: _ClassVar[PolicyAction]
    READ_INTERNAL_TRANSFERS: _ClassVar[PolicyAction]
    READ_ADDRESS_BOOK: _ClassVar[PolicyAction]
    MANAGE_ADDRESS_BOOK: _ClassVar[PolicyAction]
    READ_AUTO_WITHDRAW: _ClassVar[PolicyAction]
    MANAGE_AUTO_WITHDRAW: _ClassVar[PolicyAction]
    SWAP: _ClassVar[PolicyAction]
UNSPECIFIED: PolicyAction
TRADE_SPOT: PolicyAction
INTERNAL_TRANSFER: PolicyAction
EXTERNAL_WITHDRAW: PolicyAction
READ_BALANCES: PolicyAction
READ_SPOT: PolicyAction
READ_INTERNAL_TRANSFERS: PolicyAction
READ_ADDRESS_BOOK: PolicyAction
MANAGE_ADDRESS_BOOK: PolicyAction
READ_AUTO_WITHDRAW: PolicyAction
MANAGE_AUTO_WITHDRAW: PolicyAction
SWAP: PolicyAction

class MarketScope(_message.Message):
    __slots__ = ()
    class Value(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNSPECIFIED: _ClassVar[MarketScope.Value]
        ALL: _ClassVar[MarketScope.Value]
        ALLOWLIST: _ClassVar[MarketScope.Value]
    UNSPECIFIED: MarketScope.Value
    ALL: MarketScope.Value
    ALLOWLIST: MarketScope.Value
    def __init__(self) -> None: ...

class SpotMarketSelector(_message.Message):
    __slots__ = ("symbol_id",)
    SYMBOL_ID_FIELD_NUMBER: _ClassVar[int]
    symbol_id: int
    def __init__(self, symbol_id: _Optional[int] = ...) -> None: ...

class SpotMarketRule(_message.Message):
    __slots__ = ("symbol_id",)
    SYMBOL_ID_FIELD_NUMBER: _ClassVar[int]
    symbol_id: int
    def __init__(self, symbol_id: _Optional[int] = ...) -> None: ...

class SubaccountPolicyView(_message.Message):
    __slots__ = ("id", "name", "description", "spot_markets", "spot_market_scope", "actions", "is_template", "source_template_id", "max_order_notional", "max_open_orders", "trading_halted", "locked", "review_at", "expires_at", "created_at", "updated_at", "revision")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SPOT_MARKETS_FIELD_NUMBER: _ClassVar[int]
    SPOT_MARKET_SCOPE_FIELD_NUMBER: _ClassVar[int]
    ACTIONS_FIELD_NUMBER: _ClassVar[int]
    IS_TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    MAX_ORDER_NOTIONAL_FIELD_NUMBER: _ClassVar[int]
    MAX_OPEN_ORDERS_FIELD_NUMBER: _ClassVar[int]
    TRADING_HALTED_FIELD_NUMBER: _ClassVar[int]
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    REVIEW_AT_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    REVISION_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    description: str
    spot_markets: _containers.RepeatedCompositeFieldContainer[SpotMarketRule]
    spot_market_scope: MarketScope.Value
    actions: _containers.RepeatedScalarFieldContainer[PolicyAction]
    is_template: bool
    source_template_id: int
    max_order_notional: int
    max_open_orders: int
    trading_halted: bool
    locked: bool
    review_at: _timestamp_pb2.Timestamp
    expires_at: _timestamp_pb2.Timestamp
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    revision: int
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., spot_markets: _Optional[_Iterable[_Union[SpotMarketRule, _Mapping]]] = ..., spot_market_scope: _Optional[_Union[MarketScope.Value, str]] = ..., actions: _Optional[_Iterable[_Union[PolicyAction, str]]] = ..., is_template: _Optional[bool] = ..., source_template_id: _Optional[int] = ..., max_order_notional: _Optional[int] = ..., max_open_orders: _Optional[int] = ..., trading_halted: _Optional[bool] = ..., locked: _Optional[bool] = ..., review_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., expires_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., revision: _Optional[int] = ...) -> None: ...

class ListSubaccountPoliciesRequest(_message.Message):
    __slots__ = ("subaccount_id",)
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    def __init__(self, subaccount_id: _Optional[int] = ...) -> None: ...

class ListSubaccountPoliciesResponse(_message.Message):
    __slots__ = ("policies",)
    POLICIES_FIELD_NUMBER: _ClassVar[int]
    policies: _containers.RepeatedCompositeFieldContainer[SubaccountPolicyView]
    def __init__(self, policies: _Optional[_Iterable[_Union[SubaccountPolicyView, _Mapping]]] = ...) -> None: ...

class GetSubaccountPolicyRequest(_message.Message):
    __slots__ = ("policy_id", "subaccount_id")
    POLICY_ID_FIELD_NUMBER: _ClassVar[int]
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    policy_id: int
    subaccount_id: int
    def __init__(self, policy_id: _Optional[int] = ..., subaccount_id: _Optional[int] = ...) -> None: ...

class GetSubaccountPolicyResponse(_message.Message):
    __slots__ = ("policy",)
    POLICY_FIELD_NUMBER: _ClassVar[int]
    policy: SubaccountPolicyView
    def __init__(self, policy: _Optional[_Union[SubaccountPolicyView, _Mapping]] = ...) -> None: ...

class SubaccountPolicySpec(_message.Message):
    __slots__ = ("name", "description", "spot_markets", "spot_market_scope", "actions", "max_order_notional", "max_open_orders", "trading_halted", "locked", "review_at", "expires_at")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SPOT_MARKETS_FIELD_NUMBER: _ClassVar[int]
    SPOT_MARKET_SCOPE_FIELD_NUMBER: _ClassVar[int]
    ACTIONS_FIELD_NUMBER: _ClassVar[int]
    MAX_ORDER_NOTIONAL_FIELD_NUMBER: _ClassVar[int]
    MAX_OPEN_ORDERS_FIELD_NUMBER: _ClassVar[int]
    TRADING_HALTED_FIELD_NUMBER: _ClassVar[int]
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    REVIEW_AT_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    spot_markets: _containers.RepeatedCompositeFieldContainer[SpotMarketSelector]
    spot_market_scope: MarketScope.Value
    actions: _containers.RepeatedScalarFieldContainer[PolicyAction]
    max_order_notional: int
    max_open_orders: int
    trading_halted: bool
    locked: bool
    review_at: _timestamp_pb2.Timestamp
    expires_at: _timestamp_pb2.Timestamp
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., spot_markets: _Optional[_Iterable[_Union[SpotMarketSelector, _Mapping]]] = ..., spot_market_scope: _Optional[_Union[MarketScope.Value, str]] = ..., actions: _Optional[_Iterable[_Union[PolicyAction, str]]] = ..., max_order_notional: _Optional[int] = ..., max_open_orders: _Optional[int] = ..., trading_halted: _Optional[bool] = ..., locked: _Optional[bool] = ..., review_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., expires_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class CreateSubaccountPolicyRequest(_message.Message):
    __slots__ = ("policy", "subaccount_id")
    POLICY_FIELD_NUMBER: _ClassVar[int]
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    policy: SubaccountPolicySpec
    subaccount_id: int
    def __init__(self, policy: _Optional[_Union[SubaccountPolicySpec, _Mapping]] = ..., subaccount_id: _Optional[int] = ...) -> None: ...

class CreateSubaccountPolicyResponse(_message.Message):
    __slots__ = ("policy",)
    POLICY_FIELD_NUMBER: _ClassVar[int]
    policy: SubaccountPolicyView
    def __init__(self, policy: _Optional[_Union[SubaccountPolicyView, _Mapping]] = ...) -> None: ...

class UpdateSubaccountPolicyRequest(_message.Message):
    __slots__ = ("policy_id", "policy", "update_mask", "expected_revision")
    POLICY_ID_FIELD_NUMBER: _ClassVar[int]
    POLICY_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_REVISION_FIELD_NUMBER: _ClassVar[int]
    policy_id: int
    policy: SubaccountPolicySpec
    update_mask: _field_mask_pb2.FieldMask
    expected_revision: int
    def __init__(self, policy_id: _Optional[int] = ..., policy: _Optional[_Union[SubaccountPolicySpec, _Mapping]] = ..., update_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ..., expected_revision: _Optional[int] = ...) -> None: ...

class UpdateSubaccountPolicyResponse(_message.Message):
    __slots__ = ("policy",)
    POLICY_FIELD_NUMBER: _ClassVar[int]
    policy: SubaccountPolicyView
    def __init__(self, policy: _Optional[_Union[SubaccountPolicyView, _Mapping]] = ...) -> None: ...

class DeleteSubaccountPolicyRequest(_message.Message):
    __slots__ = ("policy_id",)
    POLICY_ID_FIELD_NUMBER: _ClassVar[int]
    policy_id: int
    def __init__(self, policy_id: _Optional[int] = ...) -> None: ...

class DeleteSubaccountPolicyResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SetSubaccountPolicyRequest(_message.Message):
    __slots__ = ("subaccount_id", "policy_id")
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    POLICY_ID_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    policy_id: int
    def __init__(self, subaccount_id: _Optional[int] = ..., policy_id: _Optional[int] = ...) -> None: ...

class SetSubaccountPolicyResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ApiPolicyView(_message.Message):
    __slots__ = ("id", "name", "description", "spot_markets", "actions", "spot_market_scope", "is_template", "source_template_id", "created_at", "updated_at", "revision")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SPOT_MARKETS_FIELD_NUMBER: _ClassVar[int]
    ACTIONS_FIELD_NUMBER: _ClassVar[int]
    SPOT_MARKET_SCOPE_FIELD_NUMBER: _ClassVar[int]
    IS_TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    REVISION_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    description: str
    spot_markets: _containers.RepeatedCompositeFieldContainer[SpotMarketRule]
    actions: _containers.RepeatedScalarFieldContainer[PolicyAction]
    spot_market_scope: MarketScope.Value
    is_template: bool
    source_template_id: int
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    revision: int
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., spot_markets: _Optional[_Iterable[_Union[SpotMarketRule, _Mapping]]] = ..., actions: _Optional[_Iterable[_Union[PolicyAction, str]]] = ..., spot_market_scope: _Optional[_Union[MarketScope.Value, str]] = ..., is_template: _Optional[bool] = ..., source_template_id: _Optional[int] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., revision: _Optional[int] = ...) -> None: ...

class ListApiPoliciesRequest(_message.Message):
    __slots__ = ("key_id",)
    KEY_ID_FIELD_NUMBER: _ClassVar[int]
    key_id: str
    def __init__(self, key_id: _Optional[str] = ...) -> None: ...

class ListApiPoliciesResponse(_message.Message):
    __slots__ = ("policies",)
    POLICIES_FIELD_NUMBER: _ClassVar[int]
    policies: _containers.RepeatedCompositeFieldContainer[ApiPolicyView]
    def __init__(self, policies: _Optional[_Iterable[_Union[ApiPolicyView, _Mapping]]] = ...) -> None: ...

class GetApiPolicyRequest(_message.Message):
    __slots__ = ("policy_id", "key_id")
    POLICY_ID_FIELD_NUMBER: _ClassVar[int]
    KEY_ID_FIELD_NUMBER: _ClassVar[int]
    policy_id: int
    key_id: str
    def __init__(self, policy_id: _Optional[int] = ..., key_id: _Optional[str] = ...) -> None: ...

class GetApiPolicyResponse(_message.Message):
    __slots__ = ("policy",)
    POLICY_FIELD_NUMBER: _ClassVar[int]
    policy: ApiPolicyView
    def __init__(self, policy: _Optional[_Union[ApiPolicyView, _Mapping]] = ...) -> None: ...

class ApiPolicySpec(_message.Message):
    __slots__ = ("name", "description", "spot_markets", "spot_market_scope", "actions", "is_template")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SPOT_MARKETS_FIELD_NUMBER: _ClassVar[int]
    SPOT_MARKET_SCOPE_FIELD_NUMBER: _ClassVar[int]
    ACTIONS_FIELD_NUMBER: _ClassVar[int]
    IS_TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    spot_markets: _containers.RepeatedCompositeFieldContainer[SpotMarketSelector]
    spot_market_scope: MarketScope.Value
    actions: _containers.RepeatedScalarFieldContainer[PolicyAction]
    is_template: bool
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., spot_markets: _Optional[_Iterable[_Union[SpotMarketSelector, _Mapping]]] = ..., spot_market_scope: _Optional[_Union[MarketScope.Value, str]] = ..., actions: _Optional[_Iterable[_Union[PolicyAction, str]]] = ..., is_template: _Optional[bool] = ...) -> None: ...

class CreateApiPolicyRequest(_message.Message):
    __slots__ = ("policy", "assign_to_key_id")
    POLICY_FIELD_NUMBER: _ClassVar[int]
    ASSIGN_TO_KEY_ID_FIELD_NUMBER: _ClassVar[int]
    policy: ApiPolicySpec
    assign_to_key_id: str
    def __init__(self, policy: _Optional[_Union[ApiPolicySpec, _Mapping]] = ..., assign_to_key_id: _Optional[str] = ...) -> None: ...

class CreateApiPolicyResponse(_message.Message):
    __slots__ = ("policy",)
    POLICY_FIELD_NUMBER: _ClassVar[int]
    policy: ApiPolicyView
    def __init__(self, policy: _Optional[_Union[ApiPolicyView, _Mapping]] = ...) -> None: ...

class UpdateApiPolicyRequest(_message.Message):
    __slots__ = ("policy_id", "policy", "update_mask", "expected_revision")
    POLICY_ID_FIELD_NUMBER: _ClassVar[int]
    POLICY_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_REVISION_FIELD_NUMBER: _ClassVar[int]
    policy_id: int
    policy: ApiPolicySpec
    update_mask: _field_mask_pb2.FieldMask
    expected_revision: int
    def __init__(self, policy_id: _Optional[int] = ..., policy: _Optional[_Union[ApiPolicySpec, _Mapping]] = ..., update_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ..., expected_revision: _Optional[int] = ...) -> None: ...

class UpdateApiPolicyResponse(_message.Message):
    __slots__ = ("policy",)
    POLICY_FIELD_NUMBER: _ClassVar[int]
    policy: ApiPolicyView
    def __init__(self, policy: _Optional[_Union[ApiPolicyView, _Mapping]] = ...) -> None: ...

class DeleteApiPolicyRequest(_message.Message):
    __slots__ = ("policy_id",)
    POLICY_ID_FIELD_NUMBER: _ClassVar[int]
    policy_id: int
    def __init__(self, policy_id: _Optional[int] = ...) -> None: ...

class DeleteApiPolicyResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SetApiKeyPolicyRequest(_message.Message):
    __slots__ = ("key_id", "policy_id")
    KEY_ID_FIELD_NUMBER: _ClassVar[int]
    POLICY_ID_FIELD_NUMBER: _ClassVar[int]
    key_id: str
    policy_id: int
    def __init__(self, key_id: _Optional[str] = ..., policy_id: _Optional[int] = ...) -> None: ...

class SetApiKeyPolicyResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
