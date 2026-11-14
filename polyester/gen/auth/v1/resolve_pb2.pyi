from polyester.gen.buf.validate import validate_pb2 as _validate_pb2
from polyester.gen.gnostic.openapi.v3 import annotations_pb2 as _annotations_pb2
from polyester.gen.google.api import annotations_pb2 as _annotations_pb2_1
from polyester.gen.google.api import field_behavior_pb2 as _field_behavior_pb2
from polyester.gen.polyester.api import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ResolveHint(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RESOLVE_HINT_UNSPECIFIED: _ClassVar[ResolveHint]
    USERNAME: _ClassVar[ResolveHint]
    ID: _ClassVar[ResolveHint]
    SMART_ACCOUNT: _ClassVar[ResolveHint]
RESOLVE_HINT_UNSPECIFIED: ResolveHint
USERNAME: ResolveHint
ID: ResolveHint
SMART_ACCOUNT: ResolveHint

class ResolvedAccount(_message.Message):
    __slots__ = ("smart_account_address", "kind", "root_username", "subaccount_label", "account_id")
    class Kind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        KIND_UNSPECIFIED: _ClassVar[ResolvedAccount.Kind]
        ROOT: _ClassVar[ResolvedAccount.Kind]
        SUB: _ClassVar[ResolvedAccount.Kind]
    KIND_UNSPECIFIED: ResolvedAccount.Kind
    ROOT: ResolvedAccount.Kind
    SUB: ResolvedAccount.Kind
    SMART_ACCOUNT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    ROOT_USERNAME_FIELD_NUMBER: _ClassVar[int]
    SUBACCOUNT_LABEL_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    smart_account_address: str
    kind: ResolvedAccount.Kind
    root_username: str
    subaccount_label: str
    account_id: int
    def __init__(self, smart_account_address: _Optional[str] = ..., kind: _Optional[_Union[ResolvedAccount.Kind, str]] = ..., root_username: _Optional[str] = ..., subaccount_label: _Optional[str] = ..., account_id: _Optional[int] = ...) -> None: ...

class ResolveAccountRequest(_message.Message):
    __slots__ = ("query", "hint", "include_subaccounts")
    QUERY_FIELD_NUMBER: _ClassVar[int]
    HINT_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_SUBACCOUNTS_FIELD_NUMBER: _ClassVar[int]
    query: str
    hint: ResolveHint
    include_subaccounts: bool
    def __init__(self, query: _Optional[str] = ..., hint: _Optional[_Union[ResolveHint, str]] = ..., include_subaccounts: _Optional[bool] = ...) -> None: ...

class ResolveAccountResponse(_message.Message):
    __slots__ = ("matches",)
    MATCHES_FIELD_NUMBER: _ClassVar[int]
    matches: _containers.RepeatedCompositeFieldContainer[ResolvedAccount]
    def __init__(self, matches: _Optional[_Iterable[_Union[ResolvedAccount, _Mapping]]] = ...) -> None: ...
