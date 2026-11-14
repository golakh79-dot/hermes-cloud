from __future__ import annotations

import asyncio
import contextlib
import os
import threading
from typing import Any, Literal, cast

from polyester.auth import (
    ACCOUNT_ID_ENV,
    API_KEY_ID_ENV,
    API_PRIVATE_KEY_ENV,
    load_api_key_credentials,
)
from polyester.catalogs import CatalogManager
from polyester.environment import (
    ENV_NAME_ENV,
    ENV_NAME_ENV_ALIAS,
    POLYESTER_DEVNET_ENVIRONMENT,
    PolyesterEnvironment,
    environment_from_name,
    parse_polyester_environment,
)
from polyester.errors import PolyesterError, PolyesterTransportError, PolyesterValidationError
from polyester.realtime.client import AsyncRealtimeClient
from polyester.services import (
    AsyncAddressBookService,
    AsyncApiKeysService,
    AsyncAuthService,
    AsyncBalancesService,
    AsyncChainAnalyticsService,
    AsyncDepositService,
    AsyncFeeService,
    AsyncGuardSignerService,
    AsyncHeatmapService,
    AsyncInternalTransfersService,
    AsyncLifecycleService,
    AsyncMarketDataService,
    AsyncMarketOverviewService,
    AsyncOrderbookService,
    AsyncOrdersService,
    AsyncPoliciesService,
    AsyncRateLimitService,
    AsyncSocialVerificationService,
    AsyncSubAccountsService,
    AsyncTradesService,
    AsyncTransfersService,
    AsyncTriggersService,
    AsyncVIPService,
    AsyncWithdrawService,
    AsyncZipperService,
)
from polyester.sync_subscribe import (
    SyncSubscription,
)
from polyester.sync_subscribe import (
    subscribe_sync as _subscribe_sync_impl,
)
from polyester.transport import TransportConfig, TransportFactory

DEFAULT_API_URL = POLYESTER_DEVNET_ENVIRONMENT.api_url
DEFAULT_WS_URL = POLYESTER_DEVNET_ENVIRONMENT.websocket_url
API_URL_ENV = "POLYESTER_API_URL"
WS_URL_ENV = "POLYESTER_WS_URL"


def _apply_from_env(overrides: dict[str, Any]) -> dict[str, Any]:
    """Fill missing constructor kwargs from ``POLYESTER_*`` process env."""
    if "environment" not in overrides:
        env_name = os.getenv(ENV_NAME_ENV) or os.getenv(ENV_NAME_ENV_ALIAS)
        if env_name:
            overrides["environment"] = environment_from_name(env_name)
    if "api_key_id" not in overrides:
        api_key_id = os.getenv(API_KEY_ID_ENV)
        if api_key_id:
            overrides["api_key_id"] = api_key_id.strip()
    if "api_private_key" not in overrides:
        api_private_key = os.getenv(API_PRIVATE_KEY_ENV)
        if api_private_key:
            overrides["api_private_key"] = api_private_key.strip()
    if "default_account_id" not in overrides:
        account_id = os.getenv(ACCOUNT_ID_ENV)
        if account_id:
            overrides["default_account_id"] = account_id.strip()
    if "api_url" not in overrides:
        api_url = os.getenv(API_URL_ENV)
        if api_url:
            overrides["api_url"] = api_url.strip()
    if "ws_url" not in overrides:
        ws_url = os.getenv(WS_URL_ENV)
        if ws_url:
            overrides["ws_url"] = ws_url.strip()
    return overrides


class AsyncPolyester:
    def __init__(
        self,
        *,
        environment: PolyesterEnvironment | None = None,
        api_key_id: str | None = None,
        api_private_key: str | bytes | None = None,
        api_url: str | None = None,
        ws_url: str | None = None,
        default_sub_account_id: str | None = None,
        default_account_id: str | int | None = None,
        timeout: float = 10.0,
        wire_format: Literal["binary", "json"] = "binary",
        hydrate_catalogs: bool = True,
    ) -> None:
        resolved = parse_polyester_environment(environment or POLYESTER_DEVNET_ENVIRONMENT)
        self.environment = resolved
        self.api_url = api_url if api_url is not None else resolved.api_url
        self.ws_url = ws_url if ws_url is not None else resolved.websocket_url
        self.default_sub_account_id = default_sub_account_id
        self.default_account_id = default_account_id
        self.catalogs = CatalogManager()
        credentials = load_api_key_credentials(
            api_key_id=api_key_id,
            api_private_key=api_private_key,
            from_env=False,
        )
        self._transport = TransportFactory(
            TransportConfig(
                api_url=self.api_url,
                timeout=timeout,
                wire_format=wire_format,
            ),
            credentials=credentials,
        )
        self.realtime = AsyncRealtimeClient(
            self.ws_url,
            api_url=self.api_url,
            credentials=credentials,
            http=self._transport.public_http,
        )
        self.auth = AsyncAuthService(self._transport, realtime=self.realtime)
        self.chain_analytics = AsyncChainAnalyticsService(self._transport)
        self.market_data = AsyncMarketDataService(
            self._transport,
            self.catalogs,
            realtime=self.realtime,
        )
        self.candles = self.market_data
        self.market_overview = AsyncMarketOverviewService(
            self._transport,
            catalogs=self.catalogs,
            realtime=self.realtime,
            wait_for_catalogs=self.wait_for_catalogs,
        )
        self.zipper = AsyncZipperService(
            self._transport,
            catalogs=self.catalogs,
            realtime=self.realtime,
        )
        self.heatmap = AsyncHeatmapService(
            self._transport,
            self.catalogs,
            realtime=self.realtime,
        )
        self.lifecycle = AsyncLifecycleService(self._transport, realtime=self.realtime)
        self.balances = AsyncBalancesService(
            self._transport,
            self.catalogs,
            default_sub_account_id,
            default_account_id,
            realtime=self.realtime,
        )
        self.orderbook = AsyncOrderbookService(
            self._transport,
            catalogs=self.catalogs,
            realtime=self.realtime,
        )
        self.orders = AsyncOrdersService(
            self._transport,
            self.catalogs,
            default_sub_account_id,
            default_account_id=default_account_id,
            realtime=self.realtime,
            wait_for_catalogs=self.wait_for_catalogs,
        )
        self.trades = AsyncTradesService(
            self._transport,
            self.catalogs,
            default_sub_account_id,
            default_account_id=default_account_id,
            realtime=self.realtime,
        )
        self.triggers = AsyncTriggersService(
            self._transport,
            self.catalogs,
            default_sub_account_id,
            default_account_id=default_account_id,
            realtime=self.realtime,
            wait_for_catalogs=self.wait_for_catalogs,
        )
        self.transfers = AsyncTransfersService(
            self._transport,
            default_sub_account_id,
            default_account_id=default_account_id,
            realtime=self.realtime,
        )
        self.internal_transfers = AsyncInternalTransfersService(
            self._transport, self.catalogs, default_sub_account_id
        )
        self.deposit = AsyncDepositService(self._transport, default_sub_account_id)
        self.fees = AsyncFeeService(
            self._transport, default_sub_account_id, catalogs=self.catalogs
        )
        self.api_keys = AsyncApiKeysService(
            self._transport,
            default_sub_account_id,
            default_account_id=default_account_id,
            realtime=self.realtime,
        )
        self.policies = AsyncPoliciesService(
            self._transport,
            default_account_id=default_account_id,
            realtime=self.realtime,
        )
        self.sub_accounts = AsyncSubAccountsService(
            self._transport,
            default_sub_account_id,
            default_account_id=default_account_id,
            realtime=self.realtime,
        )
        self.address_book = AsyncAddressBookService(
            self._transport,
            default_sub_account_id,
            default_account_id=default_account_id,
            realtime=self.realtime,
        )
        self.social_verification = AsyncSocialVerificationService(self._transport)
        self.guard_signer = AsyncGuardSignerService(self._transport, default_sub_account_id)
        self.rate_limits = AsyncRateLimitService(self._transport, default_sub_account_id)
        self.vip = AsyncVIPService(self._transport)
        self.withdraw = AsyncWithdrawService(self._transport, default_sub_account_id)
        self.trading_withdraws = self.withdraw
        self._catalog_last_error: BaseException | None = None
        self._catalog_task: asyncio.Task[None] | None
        if hydrate_catalogs:
            self._catalog_task = asyncio.create_task(self._hydrate_catalogs())
        else:
            self._catalog_task = None

    @classmethod
    def from_env(cls, **overrides) -> AsyncPolyester:
        """Create a client using ``POLYESTER_*`` variables from the process environment."""
        return cls(**_apply_from_env(overrides))

    @property
    def catalogs_last_error(self) -> BaseException | None:
        """Last catalog hydration failure, if any (also raised by ``wait_for_catalogs``)."""
        return self._catalog_last_error

    async def _hydrate_catalogs(self) -> None:
        """Hydrate spot + zipper catalogs. Records failure on ``catalogs_last_error``."""
        try:
            spot_config = await self.market_data.get_spot_config()
            raw = spot_config.raw if hasattr(spot_config, "raw") else spot_config
            if not isinstance(raw, dict):
                raise PolyesterValidationError("spot catalog response is not an object")
            self.catalogs.hydrate_spot_config(raw)
            zipper_config = await self.zipper.get_deposit_withdraw_config()
            self.catalogs.hydrate_zipper_config(zipper_config)
            self._catalog_last_error = None
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            if not self.catalogs.is_unusable:
                self.catalogs.mark_unusable(f"catalog hydration failed: {exc}")
            if isinstance(exc, PolyesterError):
                self._catalog_last_error = exc
            else:
                wrapped = PolyesterTransportError(f"catalog hydration failed: {exc}")
                wrapped.__cause__ = exc
                self._catalog_last_error = wrapped

    async def wait_for_catalogs(self) -> None:
        """Await construction-time catalog hydration.

        Raises when hydration failed (HTTP errors, empty/malformed catalogs, bad
        scales/ids). Previously returned successfully after a failed best-effort
        attempt — that behavior is removed (POLY-3746).
        """
        if self._catalog_task is None:
            return
        try:
            await self._catalog_task
        except asyncio.CancelledError:
            if self._catalog_last_error is not None:
                raise self._catalog_last_error from None
            raise
        if self._catalog_last_error is not None:
            raise self._catalog_last_error

    async def __aenter__(self) -> AsyncPolyester:
        return self

    async def __aexit__(self, *exc_info: object) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        if self._catalog_task is not None and not self._catalog_task.done():
            self._catalog_task.cancel()
            with contextlib.suppress(asyncio.CancelledError, Exception):
                await self._catalog_task
        await self.realtime.aclose()
        await self._transport.aclose()


class Polyester:
    def __init__(self, **config) -> None:
        self._loop = asyncio.new_event_loop()
        self._loop_thread = threading.Thread(
            target=self._loop.run_forever,
            name="polyester-sync-loop",
            daemon=True,
        )
        self._loop_thread.start()
        hydrate = config.get("hydrate_catalogs", True)
        self._active_sync_subscriptions: list[SyncSubscription] = []

        async def _bootstrap() -> AsyncPolyester:
            client = AsyncPolyester(**config)
            if hydrate:
                await client.wait_for_catalogs()
            return client

        self._client = asyncio.run_coroutine_threadsafe(_bootstrap(), self._loop).result(timeout=60)
        self.catalogs = self._client.catalogs
        self.catalog = self.catalogs
        self.realtime = _SyncService(self._loop, self._client.realtime)
        self.auth = cast(Any, _SyncService(self._loop, self._client.auth))
        self.auth.profile = _SyncSubscribeService(
            self._loop,
            self._client.auth.profile,
            self._active_sync_subscriptions,
            subscribe_methods={"subscribe_sync": "subscribe_identity"},
        )
        self.chain_analytics = _SyncService(self._loop, self._client.chain_analytics)
        self.market_data = _SyncSubscribeService(
            self._loop,
            self._client.market_data,
            self._active_sync_subscriptions,
            subscribe_methods={
                "subscribe_trades_sync": "subscribe_trades",
                "subscribe_candles_sync": "subscribe_candles",
            },
        )
        self.candles = self.market_data
        self.market_overview = _SyncSubscribeService(
            self._loop,
            self._client.market_overview,
            self._active_sync_subscriptions,
            subscribe_methods={"subscribe_sync": "create_subscription"},
        )
        self.zipper = _SyncSubscribeService(
            self._loop,
            self._client.zipper,
            self._active_sync_subscriptions,
            subscribe_methods={"subscribe_sync": "subscribe_zipped_asset_supply"},
        )
        self.heatmap = _SyncSubscribeService(
            self._loop,
            self._client.heatmap,
            self._active_sync_subscriptions,
            subscribe_methods={"subscribe_sync": "subscribe_live"},
        )
        self.lifecycle = _SyncSubscribeService(
            self._loop,
            self._client.lifecycle,
            self._active_sync_subscriptions,
            subscribe_methods={
                "subscribe_open_flows_sync": "subscribe_open_flows",
                "subscribe_flow_detail_sync": "subscribe_flow_detail",
            },
        )
        self.balances = _SyncSubscribeService(
            self._loop, self._client.balances, self._active_sync_subscriptions
        )
        self.orderbook = _SyncSubscribeService(
            self._loop,
            self._client.orderbook,
            self._active_sync_subscriptions,
            subscribe_methods={"subscribe_sync": "create_subscription"},
        )
        self.orders = _SyncSubscribeService(
            self._loop, self._client.orders, self._active_sync_subscriptions
        )
        self.trades = _SyncSubscribeService(
            self._loop, self._client.trades, self._active_sync_subscriptions
        )
        self.triggers = _SyncSubscribeService(
            self._loop,
            self._client.triggers,
            self._active_sync_subscriptions,
            subscribe_methods={
                "subscribe_sync": "subscribe",
                "subscribe_events_sync": "subscribe_events",
            },
        )
        self.transfers = _SyncSubscribeService(
            self._loop, self._client.transfers, self._active_sync_subscriptions
        )
        self.internal_transfers = _SyncService(self._loop, self._client.internal_transfers)
        self.deposit = _SyncService(self._loop, self._client.deposit)
        self.fees = _SyncService(self._loop, self._client.fees)
        self.api_keys = _SyncSubscribeService(
            self._loop, self._client.api_keys, self._active_sync_subscriptions
        )
        self.policies = _SyncSubscribeService(
            self._loop,
            self._client.policies,
            self._active_sync_subscriptions,
            subscribe_methods={
                "subscribe_sync": "subscribe_subaccount_policies",
                "subscribe_api_policies_sync": "subscribe_api_policies",
            },
        )
        self.sub_accounts = _SyncSubscribeService(
            self._loop,
            self._client.sub_accounts,
            self._active_sync_subscriptions,
            subscribe_methods={
                "subscribe_sync": "subscribe",
                "subscribe_api_keys_sync": "subscribe_api_keys",
            },
        )
        self.address_book = _SyncSubscribeService(
            self._loop,
            self._client.address_book,
            self._active_sync_subscriptions,
            subscribe_methods={"subscribe_sync": "subscribe_view_invalidations"},
        )
        self.social_verification = _SyncService(self._loop, self._client.social_verification)
        self.guard_signer = _SyncService(self._loop, self._client.guard_signer)
        self.rate_limits = _SyncService(self._loop, self._client.rate_limits)
        self.vip = _SyncService(self._loop, self._client.vip)
        self.withdraw = _SyncService(self._loop, self._client.withdraw)
        self.trading_withdraws = self.withdraw

    @classmethod
    def from_env(cls, **overrides) -> Polyester:
        """Create a client using ``POLYESTER_*`` variables from the process environment."""
        return cls(**_apply_from_env(overrides))

    def close(self) -> None:
        for subscription in list(self._active_sync_subscriptions):
            subscription.close()
        self._active_sync_subscriptions.clear()

        async def _shutdown() -> None:
            await self._client.aclose()

        future = asyncio.run_coroutine_threadsafe(_shutdown(), self._loop)
        with contextlib.suppress(Exception):
            future.result(timeout=10)
        self._loop.call_soon_threadsafe(self._loop.stop)
        self._loop_thread.join(timeout=5)

    def __enter__(self) -> Polyester:
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()


class _SyncService:
    def __init__(self, loop: asyncio.AbstractEventLoop, service: object) -> None:
        self._loop = loop
        self._service = service

    def __getattr__(self, name: str):
        attr = getattr(self._service, name)
        if isinstance(attr, _SyncService):
            return attr
        if not callable(attr) and type(attr).__name__.endswith("Service"):
            return _SyncService(self._loop, attr)
        if asyncio.iscoroutinefunction(attr):

            def async_call(*args, **kwargs):
                future = asyncio.run_coroutine_threadsafe(attr(*args, **kwargs), self._loop)
                return future.result(timeout=60)

            return async_call

        if callable(attr):

            def call(*args, **kwargs):
                result = attr(*args, **kwargs)
                if asyncio.iscoroutine(result):
                    future = asyncio.run_coroutine_threadsafe(result, self._loop)
                    return future.result(timeout=60)
                return result

            return call
        return attr


class _SyncSubscribeService(_SyncService):
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        service: object,
        active_subscriptions: list[SyncSubscription],
        *,
        subscribe_methods: dict[str, str] | None = None,
    ) -> None:
        super().__init__(loop, service)
        self._active_subscriptions = active_subscriptions
        for sync_name, async_attr in (subscribe_methods or {"subscribe_sync": "subscribe"}).items():
            setattr(self, sync_name, self._make_subscribe_sync(async_attr))

    def _make_subscribe_sync(self, async_attr: str):
        def subscribe_sync(
            *,
            on_event,
            on_error=None,
            **kwargs,
        ) -> SyncSubscription:
            subscribe_fn = getattr(self._service, async_attr)
            handle = _subscribe_sync_impl(
                self._loop,
                lambda: subscribe_fn(**kwargs),
                on_event=on_event,
                on_error=on_error,
            )
            self._active_subscriptions.append(handle)
            return handle

        return subscribe_sync
