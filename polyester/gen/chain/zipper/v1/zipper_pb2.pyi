from polyester.gen.gnostic.openapi.v3 import annotations_pb2 as _annotations_pb2
from polyester.gen.google.api import annotations_pb2 as _annotations_pb2_1
from polyester.gen.polyester.api import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ChainConfig(_message.Message):
    __slots__ = ("chain_id", "code", "name", "native_chain_id", "native_currency_symbol", "explorer_url", "icon", "required_confirmations", "confirmation_time_seconds", "is_case_sensitive", "min_address_length", "max_address_length")
    CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NATIVE_CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    NATIVE_CURRENCY_SYMBOL_FIELD_NUMBER: _ClassVar[int]
    EXPLORER_URL_FIELD_NUMBER: _ClassVar[int]
    ICON_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_CONFIRMATIONS_FIELD_NUMBER: _ClassVar[int]
    CONFIRMATION_TIME_SECONDS_FIELD_NUMBER: _ClassVar[int]
    IS_CASE_SENSITIVE_FIELD_NUMBER: _ClassVar[int]
    MIN_ADDRESS_LENGTH_FIELD_NUMBER: _ClassVar[int]
    MAX_ADDRESS_LENGTH_FIELD_NUMBER: _ClassVar[int]
    chain_id: int
    code: str
    name: str
    native_chain_id: str
    native_currency_symbol: str
    explorer_url: str
    icon: str
    required_confirmations: int
    confirmation_time_seconds: int
    is_case_sensitive: bool
    min_address_length: int
    max_address_length: int
    def __init__(self, chain_id: _Optional[int] = ..., code: _Optional[str] = ..., name: _Optional[str] = ..., native_chain_id: _Optional[str] = ..., native_currency_symbol: _Optional[str] = ..., explorer_url: _Optional[str] = ..., icon: _Optional[str] = ..., required_confirmations: _Optional[int] = ..., confirmation_time_seconds: _Optional[int] = ..., is_case_sensitive: _Optional[bool] = ..., min_address_length: _Optional[int] = ..., max_address_length: _Optional[int] = ...) -> None: ...

class AssetChainVariant(_message.Message):
    __slots__ = ("zipped_asset_id", "chain_id", "is_native_asset", "network_fee", "ztoken_address", "source_address", "source_decimals", "ztoken_decimals", "deposit_min_amount", "withdraw_min_amount", "supply_q")
    ZIPPED_ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    IS_NATIVE_ASSET_FIELD_NUMBER: _ClassVar[int]
    NETWORK_FEE_FIELD_NUMBER: _ClassVar[int]
    ZTOKEN_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    SOURCE_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    SOURCE_DECIMALS_FIELD_NUMBER: _ClassVar[int]
    ZTOKEN_DECIMALS_FIELD_NUMBER: _ClassVar[int]
    DEPOSIT_MIN_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    WITHDRAW_MIN_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    SUPPLY_Q_FIELD_NUMBER: _ClassVar[int]
    zipped_asset_id: int
    chain_id: int
    is_native_asset: bool
    network_fee: str
    ztoken_address: str
    source_address: str
    source_decimals: int
    ztoken_decimals: int
    deposit_min_amount: str
    withdraw_min_amount: str
    supply_q: int
    def __init__(self, zipped_asset_id: _Optional[int] = ..., chain_id: _Optional[int] = ..., is_native_asset: _Optional[bool] = ..., network_fee: _Optional[str] = ..., ztoken_address: _Optional[str] = ..., source_address: _Optional[str] = ..., source_decimals: _Optional[int] = ..., ztoken_decimals: _Optional[int] = ..., deposit_min_amount: _Optional[str] = ..., withdraw_min_amount: _Optional[str] = ..., supply_q: _Optional[int] = ...) -> None: ...

class ZippedAssetSupplyUpdate(_message.Message):
    __slots__ = ("zipped_asset_id", "supply_q")
    ZIPPED_ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    SUPPLY_Q_FIELD_NUMBER: _ClassVar[int]
    zipped_asset_id: int
    supply_q: int
    def __init__(self, zipped_asset_id: _Optional[int] = ..., supply_q: _Optional[int] = ...) -> None: ...

class ZippedAssetSupplyBatch(_message.Message):
    __slots__ = ("updates",)
    UPDATES_FIELD_NUMBER: _ClassVar[int]
    updates: _containers.RepeatedCompositeFieldContainer[ZippedAssetSupplyUpdate]
    def __init__(self, updates: _Optional[_Iterable[_Union[ZippedAssetSupplyUpdate, _Mapping]]] = ...) -> None: ...

class AssetConfig(_message.Message):
    __slots__ = ("asset", "ledger_id", "name", "icon", "quantity_scale", "quantity_display_decimals", "variants", "u_asset_id")
    ASSET_FIELD_NUMBER: _ClassVar[int]
    LEDGER_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ICON_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_SCALE_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_DISPLAY_DECIMALS_FIELD_NUMBER: _ClassVar[int]
    VARIANTS_FIELD_NUMBER: _ClassVar[int]
    U_ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    asset: str
    ledger_id: int
    name: str
    icon: str
    quantity_scale: int
    quantity_display_decimals: int
    variants: _containers.RepeatedCompositeFieldContainer[AssetChainVariant]
    u_asset_id: str
    def __init__(self, asset: _Optional[str] = ..., ledger_id: _Optional[int] = ..., name: _Optional[str] = ..., icon: _Optional[str] = ..., quantity_scale: _Optional[int] = ..., quantity_display_decimals: _Optional[int] = ..., variants: _Optional[_Iterable[_Union[AssetChainVariant, _Mapping]]] = ..., u_asset_id: _Optional[str] = ...) -> None: ...

class ChainContractConfig(_message.Message):
    __slots__ = ("name", "address", "type", "description", "version")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    name: str
    address: str
    type: str
    description: str
    version: int
    def __init__(self, name: _Optional[str] = ..., address: _Optional[str] = ..., type: _Optional[str] = ..., description: _Optional[str] = ..., version: _Optional[int] = ...) -> None: ...

class GetDepositWithdrawConfigRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetDepositWithdrawConfigResponse(_message.Message):
    __slots__ = ("chains", "assets", "ts_sec", "contracts")
    CHAINS_FIELD_NUMBER: _ClassVar[int]
    ASSETS_FIELD_NUMBER: _ClassVar[int]
    TS_SEC_FIELD_NUMBER: _ClassVar[int]
    CONTRACTS_FIELD_NUMBER: _ClassVar[int]
    chains: _containers.RepeatedCompositeFieldContainer[ChainConfig]
    assets: _containers.RepeatedCompositeFieldContainer[AssetConfig]
    ts_sec: int
    contracts: _containers.RepeatedCompositeFieldContainer[ChainContractConfig]
    def __init__(self, chains: _Optional[_Iterable[_Union[ChainConfig, _Mapping]]] = ..., assets: _Optional[_Iterable[_Union[AssetConfig, _Mapping]]] = ..., ts_sec: _Optional[int] = ..., contracts: _Optional[_Iterable[_Union[ChainContractConfig, _Mapping]]] = ...) -> None: ...
