"""First-class Polyester network environments.

Presets match ``polyester-sdk-typescript`` ``src/environment.ts`` (API / WS / RPC /
account-abstraction / trading gateway) plus the language-SDK zipper extras
(funding account, guard registry, zipper endpoint) from the live catalog.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from urllib.parse import urlparse

from eth_utils import is_address, to_checksum_address

from polyester.errors import PolyesterValidationError

ENV_NAME_ENV = "POLYESTER_ENV"
ENV_NAME_ENV_ALIAS = "POLYESTER_ENVIRONMENT"

_LOCAL_HOSTS = frozenset({"localhost", "127.0.0.1", "::1", "[::1]"})


@dataclass(frozen=True, slots=True)
class EntryPointConfig:
    address: str
    version: str = "0.7"


@dataclass(frozen=True, slots=True)
class SafeDeploymentConfig:
    version: str
    safe_module_setup_address: str
    safe_4337_module_address: str
    safe_proxy_factory_address: str
    safe_singleton_address: str
    multi_send_address: str
    multi_send_call_only_address: str | None = None


@dataclass(frozen=True, slots=True)
class AccountAbstractionEnvironment:
    bundler_url: str
    paymaster_url: str
    entry_point: EntryPointConfig
    safe: SafeDeploymentConfig


@dataclass(frozen=True, slots=True)
class ContractsEnvironment:
    trading_gateway_address: str
    funding_account_address: str
    guard_registry_address: str
    zipper_endpoint_address: str


@dataclass(frozen=True, slots=True)
class PolyesterEnvironment:
    """Complete SDK environment: API, realtime, RPC, AA, and contract pins."""

    name: str
    api_url: str
    websocket_url: str
    rpc_url: str
    chain_id: int
    account_abstraction: AccountAbstractionEnvironment
    contracts: ContractsEnvironment
    chain_name: str = ""
    explorer_url: str = ""

    def with_urls(
        self,
        *,
        api_url: str | None = None,
        websocket_url: str | None = None,
        rpc_url: str | None = None,
        bundler_url: str | None = None,
        paymaster_url: str | None = None,
        allow_insecure: bool = False,
    ) -> PolyesterEnvironment:
        """Copy this environment with endpoint overrides (market-maker / VPC case)."""
        aa = self.account_abstraction
        if bundler_url is not None or paymaster_url is not None:
            aa = replace(
                aa,
                bundler_url=bundler_url if bundler_url is not None else aa.bundler_url,
                paymaster_url=paymaster_url if paymaster_url is not None else aa.paymaster_url,
            )
        return create_polyester_environment(
            name=self.name,
            api_url=api_url if api_url is not None else self.api_url,
            websocket_url=websocket_url if websocket_url is not None else self.websocket_url,
            rpc_url=rpc_url if rpc_url is not None else self.rpc_url,
            chain_id=self.chain_id,
            account_abstraction=aa,
            contracts=self.contracts,
            chain_name=self.chain_name,
            explorer_url=self.explorer_url,
            allow_insecure=allow_insecure,
        )


# Backward-compatible alias used by chain helpers.
PolyesterChainEnvironment = PolyesterEnvironment


def _is_local_host(hostname: str) -> bool:
    host = hostname.strip().lower().rstrip(".")
    return host in _LOCAL_HOSTS or host.startswith("127.")


def _normalize_url(
    value: str,
    label: str,
    allowed_schemes: tuple[str, ...],
    *,
    allow_search: bool = True,
    allow_insecure: bool = False,
) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PolyesterValidationError(f"{label} must be a non-empty string")
    if value != value.strip():
        raise PolyesterValidationError(f"{label} must not contain surrounding whitespace")
    try:
        parsed = urlparse(value)
    except ValueError as exc:
        raise PolyesterValidationError(f"{label} must be a valid URL") from exc
    if parsed.scheme not in allowed_schemes or not parsed.netloc:
        raise PolyesterValidationError(
            f"{label} must use {' or '.join(s + '://' for s in allowed_schemes)}"
        )
    insecure = parsed.scheme in {"http", "ws"} and not _is_local_host(parsed.hostname or "")
    if insecure and not allow_insecure:
        raise PolyesterValidationError(f"{label} must use a secure protocol for remote hosts")
    if not allow_search and parsed.query:
        raise PolyesterValidationError(f"{label} must not include query parameters")
    if parsed.fragment:
        raise PolyesterValidationError(f"{label} must not include a fragment")
    return value.rstrip("/")


def _normalize_address(value: str, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PolyesterValidationError(f"{label} must be a non-empty address")
    if not is_address(value):
        raise PolyesterValidationError(f"{label} must be a valid address")
    return to_checksum_address(value)


def _normalize_entry_point(entry_point: EntryPointConfig) -> EntryPointConfig:
    if entry_point.version != "0.7":
        raise PolyesterValidationError("account_abstraction.entry_point.version must be 0.7")
    return EntryPointConfig(
        address=_normalize_address(
            entry_point.address, "account_abstraction.entry_point.address"
        ),
        version=entry_point.version,
    )


def _normalize_safe(safe: SafeDeploymentConfig) -> SafeDeploymentConfig:
    if safe.version not in {"1.4.1", "1.5.0"}:
        raise PolyesterValidationError(
            'account_abstraction.safe.version must be either "1.4.1" or "1.5.0"'
        )
    return SafeDeploymentConfig(
        version=safe.version,
        safe_module_setup_address=_normalize_address(
            safe.safe_module_setup_address,
            "account_abstraction.safe.safe_module_setup_address",
        ),
        safe_4337_module_address=_normalize_address(
            safe.safe_4337_module_address,
            "account_abstraction.safe.safe_4337_module_address",
        ),
        safe_proxy_factory_address=_normalize_address(
            safe.safe_proxy_factory_address,
            "account_abstraction.safe.safe_proxy_factory_address",
        ),
        safe_singleton_address=_normalize_address(
            safe.safe_singleton_address,
            "account_abstraction.safe.safe_singleton_address",
        ),
        multi_send_address=_normalize_address(
            safe.multi_send_address,
            "account_abstraction.safe.multi_send_address",
        ),
        multi_send_call_only_address=(
            _normalize_address(
                safe.multi_send_call_only_address,
                "account_abstraction.safe.multi_send_call_only_address",
            )
            if safe.multi_send_call_only_address
            else None
        ),
    )


def create_polyester_environment(
    *,
    name: str,
    api_url: str,
    websocket_url: str,
    rpc_url: str,
    chain_id: int,
    account_abstraction: AccountAbstractionEnvironment,
    contracts: ContractsEnvironment,
    chain_name: str = "",
    explorer_url: str = "",
    allow_insecure: bool = False,
) -> PolyesterEnvironment:
    """Validate and freeze a complete environment (presets and custom / VPC URLs)."""
    if not isinstance(name, str) or not name.strip():
        raise PolyesterValidationError("name must be a non-empty string")
    if not isinstance(chain_id, int) or isinstance(chain_id, bool) or chain_id <= 0:
        raise PolyesterValidationError("chain_id must be a positive integer")
    api_url = _normalize_url(
        api_url, "api_url", ("https", "http"), allow_search=False, allow_insecure=allow_insecure
    )
    websocket_url = _normalize_url(
        websocket_url, "websocket_url", ("wss", "ws"), allow_insecure=allow_insecure
    )
    rpc_url = _normalize_url(rpc_url, "rpc_url", ("https", "http"), allow_insecure=allow_insecure)
    aa = AccountAbstractionEnvironment(
        bundler_url=_normalize_url(
            account_abstraction.bundler_url,
            "bundler_url",
            ("https", "http"),
            allow_insecure=allow_insecure,
        ),
        paymaster_url=_normalize_url(
            account_abstraction.paymaster_url,
            "paymaster_url",
            ("https", "http"),
            allow_insecure=allow_insecure,
        ),
        entry_point=_normalize_entry_point(account_abstraction.entry_point),
        safe=_normalize_safe(account_abstraction.safe),
    )
    contracts = ContractsEnvironment(
        trading_gateway_address=_normalize_address(
            contracts.trading_gateway_address, "contracts.trading_gateway_address"
        ),
        funding_account_address=_normalize_address(
            contracts.funding_account_address, "contracts.funding_account_address"
        ),
        guard_registry_address=_normalize_address(
            contracts.guard_registry_address, "contracts.guard_registry_address"
        ),
        zipper_endpoint_address=_normalize_address(
            contracts.zipper_endpoint_address, "contracts.zipper_endpoint_address"
        ),
    )
    return PolyesterEnvironment(
        name=name.strip(),
        api_url=api_url,
        websocket_url=websocket_url,
        rpc_url=rpc_url,
        chain_id=chain_id,
        account_abstraction=aa,
        contracts=contracts,
        chain_name=chain_name.strip(),
        explorer_url=explorer_url.strip(),
    )


def parse_polyester_environment(
    environment: PolyesterEnvironment,
    *,
    allow_insecure: bool = False,
) -> PolyesterEnvironment:
    """Re-validate an environment supplied to a client constructor."""
    if not isinstance(environment, PolyesterEnvironment):
        raise PolyesterValidationError("environment must be a PolyesterEnvironment")
    return create_polyester_environment(
        name=environment.name,
        api_url=environment.api_url,
        websocket_url=environment.websocket_url,
        rpc_url=environment.rpc_url,
        chain_id=environment.chain_id,
        account_abstraction=environment.account_abstraction,
        contracts=environment.contracts,
        chain_name=environment.chain_name,
        explorer_url=environment.explorer_url,
        allow_insecure=allow_insecure,
    )


def environment_from_name(name: str) -> PolyesterEnvironment:
    """Resolve ``devnet`` / ``testnet`` (and ``polyester-*`` aliases) to a preset."""
    key = name.strip().lower()
    if key in {"devnet", "polyester-devnet"}:
        return POLYESTER_DEVNET_ENVIRONMENT
    if key in {"testnet", "polyester-testnet"}:
        return POLYESTER_TESTNET_ENVIRONMENT
    raise PolyesterValidationError(
        f"unknown environment {name!r}; expected 'devnet' or 'testnet'"
    )


POLYESTER_DEVNET_ENVIRONMENT = create_polyester_environment(
    name="polyester-devnet",
    api_url="https://api.devnet.polyester.com",
    websocket_url="wss://api.devnet.polyester.com",
    rpc_url="https://rpc.polyester.tech",
    chain_id=888168,
    chain_name="Polyester Chain Devnet",
    explorer_url="https://devnet.polyesterscan.com",
    account_abstraction=AccountAbstractionEnvironment(
        bundler_url="https://bundler.polyester.tech",
        paymaster_url="https://paymaster.polyester.tech",
        entry_point=EntryPointConfig(
            address="0x59a4B77766509c4507D79eFF8089474eC3daC174",
            version="0.7",
        ),
        safe=SafeDeploymentConfig(
            version="1.4.1",
            safe_module_setup_address="0x80791683D9C079A37Debc67EaDdbFcBC6f0FF2bB",
            safe_4337_module_address="0x0713FF3d4c1b4f177833a372b1e3cb977540EA11",
            safe_proxy_factory_address="0xF8F0F649Dd3bFa9095206691E9fb2356c26216dE",
            safe_singleton_address="0x92abEa238FEA8908c397cE65366ea9278f0AeC7A",
            multi_send_address="0x70C8a8CcB45a8E2589B0f019374fc923dA34E4c7",
            multi_send_call_only_address="0x375C86a08DA98d1944D7B3c736307A72186CcAf1",
        ),
    ),
    contracts=ContractsEnvironment(
        trading_gateway_address="0xD3fecf5D39131e23b6B0f872cA0a21c8A5a30932",
        funding_account_address="0xBfF4F6224BC10f233dDB1E61E770d9832aabC7c4",
        guard_registry_address="0xd71F60FD6f784Cc0aD8c25441568C48705D95f64",
        zipper_endpoint_address="0xae6B981BE9B73421eB1ba5372d1A4A937d63ffFB",
    ),
)

POLYESTER_TESTNET_ENVIRONMENT = create_polyester_environment(
    name="polyester-testnet",
    api_url="https://api.testnet.polyester.com",
    websocket_url="wss://api.testnet.polyester.com",
    rpc_url="https://rpc.polyester.live",
    chain_id=888169,
    chain_name="Polyester Chain Testnet",
    explorer_url="https://testnet.polyesterscan.com",
    account_abstraction=AccountAbstractionEnvironment(
        bundler_url="https://bundler.polyester.live",
        paymaster_url="https://paymaster.polyester.live",
        entry_point=EntryPointConfig(
            address="0x35c524a72ffb4D348d616cDD340D176c8f3C8B2C",
            version="0.7",
        ),
        safe=SafeDeploymentConfig(
            version="1.4.1",
            safe_module_setup_address="0xdA9510c95Ab50EAd5A3DD28FA6BACce497dCF1fB",
            safe_4337_module_address="0xE278E4BCb71b095f7dAaa1bcEc1950696Fc40C74",
            safe_proxy_factory_address="0x2b8250158D58dD6D5e89313fa940586C9054A547",
            safe_singleton_address="0x6f00AB12B6A8aFf400F14f4Cd738549f0F53390d",
            multi_send_address="0xA38fEFA19ff5d8E3d988b2a0e6C8A2ae099fd97D",
            multi_send_call_only_address="0xE99b6c6d550B322347EeE11f4e8643377D8475A8",
        ),
    ),
    contracts=ContractsEnvironment(
        trading_gateway_address="0x20ef1BCeE69D73Ce1649E688dAA9A7AcF441f0EE",
        funding_account_address="0x57D15F393772041b4107943CAFa8A70b620212D1",
        guard_registry_address="0xB0E23DDa102c5d37AcBA583cf84E5aC214e7521C",
        zipper_endpoint_address="0xD439270f881b56727EaaB878CE4e80eB08A25BEB",
    ),
)
