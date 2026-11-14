from polyester.gen.orders.v1 import orders_pb2 as _orders_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ClientFrame(_message.Message):
    __slots__ = ("seq", "correlation_id", "ping", "create_order", "cancel_order", "modify_order", "cancel_all_orders", "batch_create_orders", "batch_replace_orders", "batch_cancel_orders")
    SEQ_FIELD_NUMBER: _ClassVar[int]
    CORRELATION_ID_FIELD_NUMBER: _ClassVar[int]
    PING_FIELD_NUMBER: _ClassVar[int]
    CREATE_ORDER_FIELD_NUMBER: _ClassVar[int]
    CANCEL_ORDER_FIELD_NUMBER: _ClassVar[int]
    MODIFY_ORDER_FIELD_NUMBER: _ClassVar[int]
    CANCEL_ALL_ORDERS_FIELD_NUMBER: _ClassVar[int]
    BATCH_CREATE_ORDERS_FIELD_NUMBER: _ClassVar[int]
    BATCH_REPLACE_ORDERS_FIELD_NUMBER: _ClassVar[int]
    BATCH_CANCEL_ORDERS_FIELD_NUMBER: _ClassVar[int]
    seq: int
    correlation_id: str
    ping: PingRequest
    create_order: _orders_pb2.CreateOrderRequest
    cancel_order: _orders_pb2.CancelOrderRequest
    modify_order: _orders_pb2.ModifyOrderRequest
    cancel_all_orders: _orders_pb2.CancelAllOrdersRequest
    batch_create_orders: _orders_pb2.BatchCreateOrdersRequest
    batch_replace_orders: _orders_pb2.BatchReplaceOrdersRequest
    batch_cancel_orders: _orders_pb2.BatchCancelOrdersRequest
    def __init__(self, seq: _Optional[int] = ..., correlation_id: _Optional[str] = ..., ping: _Optional[_Union[PingRequest, _Mapping]] = ..., create_order: _Optional[_Union[_orders_pb2.CreateOrderRequest, _Mapping]] = ..., cancel_order: _Optional[_Union[_orders_pb2.CancelOrderRequest, _Mapping]] = ..., modify_order: _Optional[_Union[_orders_pb2.ModifyOrderRequest, _Mapping]] = ..., cancel_all_orders: _Optional[_Union[_orders_pb2.CancelAllOrdersRequest, _Mapping]] = ..., batch_create_orders: _Optional[_Union[_orders_pb2.BatchCreateOrdersRequest, _Mapping]] = ..., batch_replace_orders: _Optional[_Union[_orders_pb2.BatchReplaceOrdersRequest, _Mapping]] = ..., batch_cancel_orders: _Optional[_Union[_orders_pb2.BatchCancelOrdersRequest, _Mapping]] = ...) -> None: ...

class PingRequest(_message.Message):
    __slots__ = ("payload",)
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    payload: bytes
    def __init__(self, payload: _Optional[bytes] = ...) -> None: ...

class ServerFrame(_message.Message):
    __slots__ = ("seq", "correlation_id", "pong", "ack", "reject", "overload", "terminal")
    SEQ_FIELD_NUMBER: _ClassVar[int]
    CORRELATION_ID_FIELD_NUMBER: _ClassVar[int]
    PONG_FIELD_NUMBER: _ClassVar[int]
    ACK_FIELD_NUMBER: _ClassVar[int]
    REJECT_FIELD_NUMBER: _ClassVar[int]
    OVERLOAD_FIELD_NUMBER: _ClassVar[int]
    TERMINAL_FIELD_NUMBER: _ClassVar[int]
    seq: int
    correlation_id: str
    pong: PongResponse
    ack: AckResponse
    reject: CommandReject
    overload: OverloadResponse
    terminal: TerminalSessionEvent
    def __init__(self, seq: _Optional[int] = ..., correlation_id: _Optional[str] = ..., pong: _Optional[_Union[PongResponse, _Mapping]] = ..., ack: _Optional[_Union[AckResponse, _Mapping]] = ..., reject: _Optional[_Union[CommandReject, _Mapping]] = ..., overload: _Optional[_Union[OverloadResponse, _Mapping]] = ..., terminal: _Optional[_Union[TerminalSessionEvent, _Mapping]] = ...) -> None: ...

class PongResponse(_message.Message):
    __slots__ = ("payload",)
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    payload: bytes
    def __init__(self, payload: _Optional[bytes] = ...) -> None: ...

class AckResponse(_message.Message):
    __slots__ = ("create_order", "cancel_order", "modify_order", "cancel_all_orders", "batch_create_orders", "batch_replace_orders", "batch_cancel_orders")
    CREATE_ORDER_FIELD_NUMBER: _ClassVar[int]
    CANCEL_ORDER_FIELD_NUMBER: _ClassVar[int]
    MODIFY_ORDER_FIELD_NUMBER: _ClassVar[int]
    CANCEL_ALL_ORDERS_FIELD_NUMBER: _ClassVar[int]
    BATCH_CREATE_ORDERS_FIELD_NUMBER: _ClassVar[int]
    BATCH_REPLACE_ORDERS_FIELD_NUMBER: _ClassVar[int]
    BATCH_CANCEL_ORDERS_FIELD_NUMBER: _ClassVar[int]
    create_order: _orders_pb2.CreateOrderResponse
    cancel_order: _orders_pb2.CancelOrderResponse
    modify_order: _orders_pb2.ModifyOrderResponse
    cancel_all_orders: _orders_pb2.CancelAllOrdersResponse
    batch_create_orders: _orders_pb2.BatchCreateOrdersResponse
    batch_replace_orders: _orders_pb2.BatchReplaceOrdersResponse
    batch_cancel_orders: _orders_pb2.BatchCancelOrdersResponse
    def __init__(self, create_order: _Optional[_Union[_orders_pb2.CreateOrderResponse, _Mapping]] = ..., cancel_order: _Optional[_Union[_orders_pb2.CancelOrderResponse, _Mapping]] = ..., modify_order: _Optional[_Union[_orders_pb2.ModifyOrderResponse, _Mapping]] = ..., cancel_all_orders: _Optional[_Union[_orders_pb2.CancelAllOrdersResponse, _Mapping]] = ..., batch_create_orders: _Optional[_Union[_orders_pb2.BatchCreateOrdersResponse, _Mapping]] = ..., batch_replace_orders: _Optional[_Union[_orders_pb2.BatchReplaceOrdersResponse, _Mapping]] = ..., batch_cancel_orders: _Optional[_Union[_orders_pb2.BatchCancelOrdersResponse, _Mapping]] = ...) -> None: ...

class CommandReject(_message.Message):
    __slots__ = ("code", "detail", "error")
    CODE_FIELD_NUMBER: _ClassVar[int]
    DETAIL_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    code: str
    detail: str
    error: _orders_pb2.ErrorDetail
    def __init__(self, code: _Optional[str] = ..., detail: _Optional[str] = ..., error: _Optional[_Union[_orders_pb2.ErrorDetail, _Mapping]] = ...) -> None: ...

class OverloadResponse(_message.Message):
    __slots__ = ("code", "detail")
    CODE_FIELD_NUMBER: _ClassVar[int]
    DETAIL_FIELD_NUMBER: _ClassVar[int]
    code: str
    detail: str
    def __init__(self, code: _Optional[str] = ..., detail: _Optional[str] = ...) -> None: ...

class TerminalSessionEvent(_message.Message):
    __slots__ = ("code", "detail")
    CODE_FIELD_NUMBER: _ClassVar[int]
    DETAIL_FIELD_NUMBER: _ClassVar[int]
    code: str
    detail: str
    def __init__(self, code: _Optional[str] = ..., detail: _Optional[str] = ...) -> None: ...
