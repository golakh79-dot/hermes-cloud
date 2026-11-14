from polyester.gen.buf.validate import validate_pb2 as _validate_pb2
from polyester.gen.orders.v1 import orders_pb2 as _orders_pb2
from polyester.gen.orders.v1 import orders_read_pb2 as _orders_read_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Channel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CHANNEL_UNSPECIFIED: _ClassVar[Channel]
    ORDERS: _ClassVar[Channel]

class UnavailableReason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNAVAILABLE_REASON_UNSPECIFIED: _ClassVar[UnavailableReason]
    VIEW_BEHIND: _ClassVar[UnavailableReason]
    NOT_READY: _ClassVar[UnavailableReason]
    FAILOVER: _ClassVar[UnavailableReason]
    BOUNDARY_UNAVAILABLE: _ClassVar[UnavailableReason]
    ORDER_UNAVAILABLE: _ClassVar[UnavailableReason]
CHANNEL_UNSPECIFIED: Channel
ORDERS: Channel
UNAVAILABLE_REASON_UNSPECIFIED: UnavailableReason
VIEW_BEHIND: UnavailableReason
NOT_READY: UnavailableReason
FAILOVER: UnavailableReason
BOUNDARY_UNAVAILABLE: UnavailableReason
ORDER_UNAVAILABLE: UnavailableReason

class ClientMessage(_message.Message):
    __slots__ = ("auth", "subscribe", "subscribe_refresh", "unsubscribe", "sync", "ping")
    AUTH_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIBE_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIBE_REFRESH_FIELD_NUMBER: _ClassVar[int]
    UNSUBSCRIBE_FIELD_NUMBER: _ClassVar[int]
    SYNC_FIELD_NUMBER: _ClassVar[int]
    PING_FIELD_NUMBER: _ClassVar[int]
    auth: Auth
    subscribe: Subscribe
    subscribe_refresh: SubscribeRefresh
    unsubscribe: Unsubscribe
    sync: Sync
    ping: Ping
    def __init__(self, auth: _Optional[_Union[Auth, _Mapping]] = ..., subscribe: _Optional[_Union[Subscribe, _Mapping]] = ..., subscribe_refresh: _Optional[_Union[SubscribeRefresh, _Mapping]] = ..., unsubscribe: _Optional[_Union[Unsubscribe, _Mapping]] = ..., sync: _Optional[_Union[Sync, _Mapping]] = ..., ping: _Optional[_Union[Ping, _Mapping]] = ...) -> None: ...

class Auth(_message.Message):
    __slots__ = ("token",)
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: str
    def __init__(self, token: _Optional[str] = ...) -> None: ...

class Subscribe(_message.Message):
    __slots__ = ("id", "channel", "account", "token", "cursor")
    ID_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    id: str
    channel: Channel
    account: int
    token: str
    cursor: str
    def __init__(self, id: _Optional[str] = ..., channel: _Optional[_Union[Channel, str]] = ..., account: _Optional[int] = ..., token: _Optional[str] = ..., cursor: _Optional[str] = ...) -> None: ...

class SubscribeRefresh(_message.Message):
    __slots__ = ("id", "sub", "token")
    ID_FIELD_NUMBER: _ClassVar[int]
    SUB_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    id: str
    sub: str
    token: str
    def __init__(self, id: _Optional[str] = ..., sub: _Optional[str] = ..., token: _Optional[str] = ...) -> None: ...

class Unsubscribe(_message.Message):
    __slots__ = ("id", "sub")
    ID_FIELD_NUMBER: _ClassVar[int]
    SUB_FIELD_NUMBER: _ClassVar[int]
    id: str
    sub: str
    def __init__(self, id: _Optional[str] = ..., sub: _Optional[str] = ...) -> None: ...

class Sync(_message.Message):
    __slots__ = ("id", "sub")
    ID_FIELD_NUMBER: _ClassVar[int]
    SUB_FIELD_NUMBER: _ClassVar[int]
    id: str
    sub: str
    def __init__(self, id: _Optional[str] = ..., sub: _Optional[str] = ...) -> None: ...

class Ping(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class ServerMessage(_message.Message):
    __slots__ = ("sub", "seq", "authenticated", "token_expiring", "subscribed", "subscribe_refreshed", "unsubscribed", "subscribe_expiring", "snapshot_begin", "snapshot_page", "snapshot_end", "unit", "covered", "ready", "synced", "resync_required", "unavailable", "available", "error", "heartbeat", "pong")
    SUB_FIELD_NUMBER: _ClassVar[int]
    SEQ_FIELD_NUMBER: _ClassVar[int]
    AUTHENTICATED_FIELD_NUMBER: _ClassVar[int]
    TOKEN_EXPIRING_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIBED_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIBE_REFRESHED_FIELD_NUMBER: _ClassVar[int]
    UNSUBSCRIBED_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIBE_EXPIRING_FIELD_NUMBER: _ClassVar[int]
    SNAPSHOT_BEGIN_FIELD_NUMBER: _ClassVar[int]
    SNAPSHOT_PAGE_FIELD_NUMBER: _ClassVar[int]
    SNAPSHOT_END_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    COVERED_FIELD_NUMBER: _ClassVar[int]
    READY_FIELD_NUMBER: _ClassVar[int]
    SYNCED_FIELD_NUMBER: _ClassVar[int]
    RESYNC_REQUIRED_FIELD_NUMBER: _ClassVar[int]
    UNAVAILABLE_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    HEARTBEAT_FIELD_NUMBER: _ClassVar[int]
    PONG_FIELD_NUMBER: _ClassVar[int]
    sub: str
    seq: int
    authenticated: Authenticated
    token_expiring: TokenExpiring
    subscribed: Subscribed
    subscribe_refreshed: SubscribeRefreshed
    unsubscribed: Unsubscribed
    subscribe_expiring: SubscribeExpiring
    snapshot_begin: SnapshotBegin
    snapshot_page: SnapshotPage
    snapshot_end: SnapshotEnd
    unit: Unit
    covered: Covered
    ready: Ready
    synced: Synced
    resync_required: ResyncRequired
    unavailable: Unavailable
    available: Available
    error: RequestError
    heartbeat: Heartbeat
    pong: Pong
    def __init__(self, sub: _Optional[str] = ..., seq: _Optional[int] = ..., authenticated: _Optional[_Union[Authenticated, _Mapping]] = ..., token_expiring: _Optional[_Union[TokenExpiring, _Mapping]] = ..., subscribed: _Optional[_Union[Subscribed, _Mapping]] = ..., subscribe_refreshed: _Optional[_Union[SubscribeRefreshed, _Mapping]] = ..., unsubscribed: _Optional[_Union[Unsubscribed, _Mapping]] = ..., subscribe_expiring: _Optional[_Union[SubscribeExpiring, _Mapping]] = ..., snapshot_begin: _Optional[_Union[SnapshotBegin, _Mapping]] = ..., snapshot_page: _Optional[_Union[SnapshotPage, _Mapping]] = ..., snapshot_end: _Optional[_Union[SnapshotEnd, _Mapping]] = ..., unit: _Optional[_Union[Unit, _Mapping]] = ..., covered: _Optional[_Union[Covered, _Mapping]] = ..., ready: _Optional[_Union[Ready, _Mapping]] = ..., synced: _Optional[_Union[Synced, _Mapping]] = ..., resync_required: _Optional[_Union[ResyncRequired, _Mapping]] = ..., unavailable: _Optional[_Union[Unavailable, _Mapping]] = ..., available: _Optional[_Union[Available, _Mapping]] = ..., error: _Optional[_Union[RequestError, _Mapping]] = ..., heartbeat: _Optional[_Union[Heartbeat, _Mapping]] = ..., pong: _Optional[_Union[Pong, _Mapping]] = ...) -> None: ...

class Authenticated(_message.Message):
    __slots__ = ("expires_ts_sec",)
    EXPIRES_TS_SEC_FIELD_NUMBER: _ClassVar[int]
    expires_ts_sec: int
    def __init__(self, expires_ts_sec: _Optional[int] = ...) -> None: ...

class TokenExpiring(_message.Message):
    __slots__ = ("expires_ts_sec",)
    EXPIRES_TS_SEC_FIELD_NUMBER: _ClassVar[int]
    expires_ts_sec: int
    def __init__(self, expires_ts_sec: _Optional[int] = ...) -> None: ...

class Subscribed(_message.Message):
    __slots__ = ("id", "account", "expires_ts_sec")
    ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_TS_SEC_FIELD_NUMBER: _ClassVar[int]
    id: str
    account: int
    expires_ts_sec: int
    def __init__(self, id: _Optional[str] = ..., account: _Optional[int] = ..., expires_ts_sec: _Optional[int] = ...) -> None: ...

class SubscribeRefreshed(_message.Message):
    __slots__ = ("id", "expires_ts_sec")
    ID_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_TS_SEC_FIELD_NUMBER: _ClassVar[int]
    id: str
    expires_ts_sec: int
    def __init__(self, id: _Optional[str] = ..., expires_ts_sec: _Optional[int] = ...) -> None: ...

class Unsubscribed(_message.Message):
    __slots__ = ("id", "reason")
    class Reason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        REASON_UNSPECIFIED: _ClassVar[Unsubscribed.Reason]
        REQUESTED: _ClassVar[Unsubscribed.Reason]
        TOKEN_EXPIRED: _ClassVar[Unsubscribed.Reason]
    REASON_UNSPECIFIED: Unsubscribed.Reason
    REQUESTED: Unsubscribed.Reason
    TOKEN_EXPIRED: Unsubscribed.Reason
    ID_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    id: str
    reason: Unsubscribed.Reason
    def __init__(self, id: _Optional[str] = ..., reason: _Optional[_Union[Unsubscribed.Reason, str]] = ...) -> None: ...

class SubscribeExpiring(_message.Message):
    __slots__ = ("expires_ts_sec",)
    EXPIRES_TS_SEC_FIELD_NUMBER: _ClassVar[int]
    expires_ts_sec: int
    def __init__(self, expires_ts_sec: _Optional[int] = ...) -> None: ...

class SnapshotBegin(_message.Message):
    __slots__ = ("epoch",)
    EPOCH_FIELD_NUMBER: _ClassVar[int]
    epoch: int
    def __init__(self, epoch: _Optional[int] = ...) -> None: ...

class SnapshotPage(_message.Message):
    __slots__ = ("orders",)
    ORDERS_FIELD_NUMBER: _ClassVar[int]
    orders: _containers.RepeatedCompositeFieldContainer[_orders_read_pb2.Order]
    def __init__(self, orders: _Optional[_Iterable[_Union[_orders_read_pb2.Order, _Mapping]]] = ...) -> None: ...

class SnapshotEnd(_message.Message):
    __slots__ = ("cursor", "count", "digest")
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    DIGEST_FIELD_NUMBER: _ClassVar[int]
    cursor: str
    count: int
    digest: int
    def __init__(self, cursor: _Optional[str] = ..., count: _Optional[int] = ..., digest: _Optional[int] = ...) -> None: ...

class Unit(_message.Message):
    __slots__ = ("prev_cursor", "next_cursor", "orders", "removed_order_ids", "events")
    PREV_CURSOR_FIELD_NUMBER: _ClassVar[int]
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    ORDERS_FIELD_NUMBER: _ClassVar[int]
    REMOVED_ORDER_IDS_FIELD_NUMBER: _ClassVar[int]
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    prev_cursor: str
    next_cursor: str
    orders: _containers.RepeatedCompositeFieldContainer[_orders_read_pb2.Order]
    removed_order_ids: _containers.RepeatedScalarFieldContainer[int]
    events: _containers.RepeatedCompositeFieldContainer[UnitEvent]
    def __init__(self, prev_cursor: _Optional[str] = ..., next_cursor: _Optional[str] = ..., orders: _Optional[_Iterable[_Union[_orders_read_pb2.Order, _Mapping]]] = ..., removed_order_ids: _Optional[_Iterable[int]] = ..., events: _Optional[_Iterable[_Union[UnitEvent, _Mapping]]] = ...) -> None: ...

class Covered(_message.Message):
    __slots__ = ("cursor",)
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    cursor: str
    def __init__(self, cursor: _Optional[str] = ...) -> None: ...

class Ready(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Synced(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class ResyncRequired(_message.Message):
    __slots__ = ("reason",)
    class Reason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        REASON_UNSPECIFIED: _ClassVar[ResyncRequired.Reason]
        CURSOR_UNKNOWN: _ClassVar[ResyncRequired.Reason]
        CURSOR_EXPIRED: _ClassVar[ResyncRequired.Reason]
        HISTORY_RESET: _ClassVar[ResyncRequired.Reason]
    REASON_UNSPECIFIED: ResyncRequired.Reason
    CURSOR_UNKNOWN: ResyncRequired.Reason
    CURSOR_EXPIRED: ResyncRequired.Reason
    HISTORY_RESET: ResyncRequired.Reason
    REASON_FIELD_NUMBER: _ClassVar[int]
    reason: ResyncRequired.Reason
    def __init__(self, reason: _Optional[_Union[ResyncRequired.Reason, str]] = ...) -> None: ...

class Unavailable(_message.Message):
    __slots__ = ("reason", "order_ids")
    REASON_FIELD_NUMBER: _ClassVar[int]
    ORDER_IDS_FIELD_NUMBER: _ClassVar[int]
    reason: UnavailableReason
    order_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, reason: _Optional[_Union[UnavailableReason, str]] = ..., order_ids: _Optional[_Iterable[int]] = ...) -> None: ...

class Available(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class RequestError(_message.Message):
    __slots__ = ("id", "code", "message")
    class Code(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        CODE_UNSPECIFIED: _ClassVar[RequestError.Code]
        FORBIDDEN: _ClassVar[RequestError.Code]
        INVALID_REQUEST: _ClassVar[RequestError.Code]
        SUBSCRIPTION_UNKNOWN: _ClassVar[RequestError.Code]
        CURSOR_INVALID: _ClassVar[RequestError.Code]
        TOO_MANY_SUBSCRIPTIONS: _ClassVar[RequestError.Code]
        BEHIND: _ClassVar[RequestError.Code]
    CODE_UNSPECIFIED: RequestError.Code
    FORBIDDEN: RequestError.Code
    INVALID_REQUEST: RequestError.Code
    SUBSCRIPTION_UNKNOWN: RequestError.Code
    CURSOR_INVALID: RequestError.Code
    TOO_MANY_SUBSCRIPTIONS: RequestError.Code
    BEHIND: RequestError.Code
    ID_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    id: str
    code: RequestError.Code
    message: str
    def __init__(self, id: _Optional[str] = ..., code: _Optional[_Union[RequestError.Code, str]] = ..., message: _Optional[str] = ...) -> None: ...

class Heartbeat(_message.Message):
    __slots__ = ("server_ts_ns",)
    SERVER_TS_NS_FIELD_NUMBER: _ClassVar[int]
    server_ts_ns: int
    def __init__(self, server_ts_ns: _Optional[int] = ...) -> None: ...

class Pong(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class UnitEvent(_message.Message):
    __slots__ = ("order", "outcome")
    ORDER_FIELD_NUMBER: _ClassVar[int]
    OUTCOME_FIELD_NUMBER: _ClassVar[int]
    order: OrderEvent
    outcome: CommandOutcome
    def __init__(self, order: _Optional[_Union[OrderEvent, _Mapping]] = ..., outcome: _Optional[_Union[CommandOutcome, _Mapping]] = ...) -> None: ...

class OrderEvent(_message.Message):
    __slots__ = ("order_id", "version", "kind", "reject_reason", "cancel_reason", "replacement_order_id", "fill")
    class Kind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        KIND_UNSPECIFIED: _ClassVar[OrderEvent.Kind]
        ACCEPTED: _ClassVar[OrderEvent.Kind]
        FILLED: _ClassVar[OrderEvent.Kind]
        CANCELED: _ClassVar[OrderEvent.Kind]
        REJECTED: _ClassVar[OrderEvent.Kind]
        REPLACED: _ClassVar[OrderEvent.Kind]
        ATTACHED_RISK: _ClassVar[OrderEvent.Kind]
    KIND_UNSPECIFIED: OrderEvent.Kind
    ACCEPTED: OrderEvent.Kind
    FILLED: OrderEvent.Kind
    CANCELED: OrderEvent.Kind
    REJECTED: OrderEvent.Kind
    REPLACED: OrderEvent.Kind
    ATTACHED_RISK: OrderEvent.Kind
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    REJECT_REASON_FIELD_NUMBER: _ClassVar[int]
    CANCEL_REASON_FIELD_NUMBER: _ClassVar[int]
    REPLACEMENT_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    FILL_FIELD_NUMBER: _ClassVar[int]
    order_id: int
    version: int
    kind: OrderEvent.Kind
    reject_reason: _orders_pb2.ErrorCode
    cancel_reason: _orders_read_pb2.CancelReason
    replacement_order_id: int
    fill: Fill
    def __init__(self, order_id: _Optional[int] = ..., version: _Optional[int] = ..., kind: _Optional[_Union[OrderEvent.Kind, str]] = ..., reject_reason: _Optional[_Union[_orders_pb2.ErrorCode, str]] = ..., cancel_reason: _Optional[_Union[_orders_read_pb2.CancelReason, str]] = ..., replacement_order_id: _Optional[int] = ..., fill: _Optional[_Union[Fill, _Mapping]] = ...) -> None: ...

class Fill(_message.Message):
    __slots__ = ("match_id", "ordinal", "role", "qty_scaled", "price_ticks")
    class Role(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ROLE_UNSPECIFIED: _ClassVar[Fill.Role]
        MAKER: _ClassVar[Fill.Role]
        TAKER: _ClassVar[Fill.Role]
    ROLE_UNSPECIFIED: Fill.Role
    MAKER: Fill.Role
    TAKER: Fill.Role
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    ORDINAL_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    QTY_SCALED_FIELD_NUMBER: _ClassVar[int]
    PRICE_TICKS_FIELD_NUMBER: _ClassVar[int]
    match_id: int
    ordinal: int
    role: Fill.Role
    qty_scaled: int
    price_ticks: int
    def __init__(self, match_id: _Optional[int] = ..., ordinal: _Optional[int] = ..., role: _Optional[_Union[Fill.Role, str]] = ..., qty_scaled: _Optional[int] = ..., price_ticks: _Optional[int] = ...) -> None: ...

class CommandOutcome(_message.Message):
    __slots__ = ("kind", "order_id", "new_order_id", "client_order_id", "reason")
    class Kind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        KIND_UNSPECIFIED: _ClassVar[CommandOutcome.Kind]
        AMEND_REJECTED: _ClassVar[CommandOutcome.Kind]
        CANCEL_REJECTED: _ClassVar[CommandOutcome.Kind]
        REPLACE_REJECTED: _ClassVar[CommandOutcome.Kind]
        REJECTED: _ClassVar[CommandOutcome.Kind]
        CANCEL_ALL_DONE: _ClassVar[CommandOutcome.Kind]
    KIND_UNSPECIFIED: CommandOutcome.Kind
    AMEND_REJECTED: CommandOutcome.Kind
    CANCEL_REJECTED: CommandOutcome.Kind
    REPLACE_REJECTED: CommandOutcome.Kind
    REJECTED: CommandOutcome.Kind
    CANCEL_ALL_DONE: CommandOutcome.Kind
    KIND_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    NEW_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    kind: CommandOutcome.Kind
    order_id: int
    new_order_id: int
    client_order_id: str
    reason: _orders_pb2.ErrorCode
    def __init__(self, kind: _Optional[_Union[CommandOutcome.Kind, str]] = ..., order_id: _Optional[int] = ..., new_order_id: _Optional[int] = ..., client_order_id: _Optional[str] = ..., reason: _Optional[_Union[_orders_pb2.ErrorCode, str]] = ...) -> None: ...
