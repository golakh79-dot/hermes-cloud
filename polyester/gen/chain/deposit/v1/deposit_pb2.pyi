from polyester.gen.buf.validate import validate_pb2 as _validate_pb2
from polyester.gen.gnostic.openapi.v3 import annotations_pb2 as _annotations_pb2
from polyester.gen.google.api import annotations_pb2 as _annotations_pb2_1
from polyester.gen.polyester.api import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DepositAddress(_message.Message):
    __slots__ = ("chain_id", "deposit_address")
    CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    DEPOSIT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    chain_id: int
    deposit_address: str
    def __init__(self, chain_id: _Optional[int] = ..., deposit_address: _Optional[str] = ...) -> None: ...

class CreateDepositAddressRequest(_message.Message):
    __slots__ = ("subaccount_id", "chain_id")
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    chain_id: int
    def __init__(self, subaccount_id: _Optional[int] = ..., chain_id: _Optional[int] = ...) -> None: ...

class CreateDepositAddressResponse(_message.Message):
    __slots__ = ("deposit_address",)
    DEPOSIT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    deposit_address: DepositAddress
    def __init__(self, deposit_address: _Optional[_Union[DepositAddress, _Mapping]] = ...) -> None: ...

class ListDepositAddressesRequest(_message.Message):
    __slots__ = ("subaccount_id", "chain_id")
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    subaccount_id: int
    chain_id: int
    def __init__(self, subaccount_id: _Optional[int] = ..., chain_id: _Optional[int] = ...) -> None: ...

class ListDepositAddressesResponse(_message.Message):
    __slots__ = ("deposit_addresses",)
    DEPOSIT_ADDRESSES_FIELD_NUMBER: _ClassVar[int]
    deposit_addresses: _containers.RepeatedCompositeFieldContainer[DepositAddress]
    def __init__(self, deposit_addresses: _Optional[_Iterable[_Union[DepositAddress, _Mapping]]] = ...) -> None: ...
