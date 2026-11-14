import datetime

from polyester.gen.buf.validate import validate_pb2 as _validate_pb2
from polyester.gen.gnostic.openapi.v3 import annotations_pb2 as _annotations_pb2
from polyester.gen.google.api import annotations_pb2 as _annotations_pb2_1
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from polyester.gen.polyester.api import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RewardFulfillmentMethod(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    METHOD_UNSPECIFIED: _ClassVar[RewardFulfillmentMethod]
    EXTERNAL_TESTNET: _ClassVar[RewardFulfillmentMethod]
    INTERNAL_TRADING: _ClassVar[RewardFulfillmentMethod]

class RewardFulfillmentState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STATE_UNSPECIFIED: _ClassVar[RewardFulfillmentState]
    AWAITING_DESTINATION: _ClassVar[RewardFulfillmentState]
    READY_FOR_PAYOUT: _ClassVar[RewardFulfillmentState]
    PAID: _ClassVar[RewardFulfillmentState]
    FAILED: _ClassVar[RewardFulfillmentState]
    CANCELED: _ClassVar[RewardFulfillmentState]
METHOD_UNSPECIFIED: RewardFulfillmentMethod
EXTERNAL_TESTNET: RewardFulfillmentMethod
INTERNAL_TRADING: RewardFulfillmentMethod
STATE_UNSPECIFIED: RewardFulfillmentState
AWAITING_DESTINATION: RewardFulfillmentState
READY_FOR_PAYOUT: RewardFulfillmentState
PAID: RewardFulfillmentState
FAILED: RewardFulfillmentState
CANCELED: RewardFulfillmentState

class RewardAward(_message.Message):
    __slots__ = ("award_id", "campaign_id", "campaign_name", "asset_id", "amount_base_units", "fulfillment_method", "fulfillment_state", "published_at", "network", "fulfillment_revision", "destination_address", "transaction_id")
    AWARD_ID_FIELD_NUMBER: _ClassVar[int]
    CAMPAIGN_ID_FIELD_NUMBER: _ClassVar[int]
    CAMPAIGN_NAME_FIELD_NUMBER: _ClassVar[int]
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_BASE_UNITS_FIELD_NUMBER: _ClassVar[int]
    FULFILLMENT_METHOD_FIELD_NUMBER: _ClassVar[int]
    FULFILLMENT_STATE_FIELD_NUMBER: _ClassVar[int]
    PUBLISHED_AT_FIELD_NUMBER: _ClassVar[int]
    NETWORK_FIELD_NUMBER: _ClassVar[int]
    FULFILLMENT_REVISION_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    TRANSACTION_ID_FIELD_NUMBER: _ClassVar[int]
    award_id: str
    campaign_id: str
    campaign_name: str
    asset_id: int
    amount_base_units: str
    fulfillment_method: RewardFulfillmentMethod
    fulfillment_state: RewardFulfillmentState
    published_at: _timestamp_pb2.Timestamp
    network: str
    fulfillment_revision: int
    destination_address: str
    transaction_id: str
    def __init__(self, award_id: _Optional[str] = ..., campaign_id: _Optional[str] = ..., campaign_name: _Optional[str] = ..., asset_id: _Optional[int] = ..., amount_base_units: _Optional[str] = ..., fulfillment_method: _Optional[_Union[RewardFulfillmentMethod, str]] = ..., fulfillment_state: _Optional[_Union[RewardFulfillmentState, str]] = ..., published_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., network: _Optional[str] = ..., fulfillment_revision: _Optional[int] = ..., destination_address: _Optional[str] = ..., transaction_id: _Optional[str] = ...) -> None: ...

class SetMyRewardDestinationRequest(_message.Message):
    __slots__ = ("award_id", "destination_address", "expected_revision", "request_id")
    AWARD_ID_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_REVISION_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    award_id: str
    destination_address: str
    expected_revision: int
    request_id: str
    def __init__(self, award_id: _Optional[str] = ..., destination_address: _Optional[str] = ..., expected_revision: _Optional[int] = ..., request_id: _Optional[str] = ...) -> None: ...

class SetMyRewardDestinationResponse(_message.Message):
    __slots__ = ("award",)
    AWARD_FIELD_NUMBER: _ClassVar[int]
    award: RewardAward
    def __init__(self, award: _Optional[_Union[RewardAward, _Mapping]] = ...) -> None: ...

class ListMyRewardAwardsRequest(_message.Message):
    __slots__ = ("limit", "page_token")
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    limit: int
    page_token: str
    def __init__(self, limit: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class ListMyRewardAwardsResponse(_message.Message):
    __slots__ = ("awards", "next_page_token", "awards_may_change")
    AWARDS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    AWARDS_MAY_CHANGE_FIELD_NUMBER: _ClassVar[int]
    awards: _containers.RepeatedCompositeFieldContainer[RewardAward]
    next_page_token: str
    awards_may_change: bool
    def __init__(self, awards: _Optional[_Iterable[_Union[RewardAward, _Mapping]]] = ..., next_page_token: _Optional[str] = ..., awards_may_change: _Optional[bool] = ...) -> None: ...
