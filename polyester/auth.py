from __future__ import annotations

import asyncio
import hashlib
import os
import threading
import time
from dataclasses import dataclass, field
from urllib.parse import parse_qsl, quote, urlsplit

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from polyester.errors import PolyesterAuthError, PolyesterRateLimitError, PolyesterTransportError

API_KEY_ID_ENV = "POLYESTER_API_KEY_ID"
API_PRIVATE_KEY_ENV = "POLYESTER_API_PRIVATE_KEY"
ACCOUNT_ID_ENV = "POLYESTER_ACCOUNT_ID"
MAX_SIGNING_FUTURE_SKEW_MS = 5_000
_MAX_SIGNING_BACKPRESSURE_SECONDS = 10.0


class _SigningTimestampAllocator:
    """Allocate distinct millisecond timestamps without exceeding clock skew."""

    def __init__(self) -> None:
        self._last_timestamp_ms = 0
        self._lock = threading.Lock()
        self._async_lock = asyncio.Lock()

    def next(self) -> int:
        """Allocate immediately or fail with retryable capacity backpressure.

        Synchronous callers must never sleep an async executor thread. Async
        SDK transports use :meth:`next_async`, which waits cooperatively.
        """
        return self._try_next()

    async def next_async(self) -> int:
        """Allocate with bounded, cooperative backpressure."""

        async def allocate() -> int:
            async with self._async_lock:
                while True:
                    try:
                        return self._try_next()
                    except PolyesterRateLimitError as exc:
                        await asyncio.sleep(exc.retry_after or 0.001)

        try:
            return await asyncio.wait_for(
                allocate(),
                timeout=_MAX_SIGNING_BACKPRESSURE_SECONDS,
            )
        except TimeoutError as exc:
            raise PolyesterRateLimitError(
                "signing timestamp capacity exhausted; retry after clock advances",
                retry_after=0.001,
            ) from exc

    def _try_next(self) -> int:
        now = time.time_ns() // 1_000_000
        if now < 0:
            raise PolyesterTransportError("system clock is before UNIX_EPOCH")
        with self._lock:
            candidate = max(now, self._last_timestamp_ms + 1)
            if candidate <= now + MAX_SIGNING_FUTURE_SKEW_MS:
                self._last_timestamp_ms = candidate
                return candidate
            wait_seconds = max(0.001, (candidate - (now + MAX_SIGNING_FUTURE_SKEW_MS)) / 1_000)
        raise PolyesterRateLimitError(
            "signing timestamp capacity exhausted; retry after clock advances",
            retry_after=wait_seconds,
        )


@dataclass(frozen=True, slots=True)
class ApiKeyCredentials:
    key_id: str
    private_key: bytes = field(repr=False)
    _timestamp_allocator: _SigningTimestampAllocator = field(
        default_factory=_SigningTimestampAllocator,
        repr=False,
        compare=False,
    )

    def __repr__(self) -> str:
        return f"ApiKeyCredentials(key_id={self.key_id!r}, private_key='[REDACTED]')"

    def sign_payload(self, payload: bytes) -> bytes:
        """Sign exact protocol-defined business-payload bytes with Ed25519."""
        if not isinstance(payload, bytes):
            raise TypeError("payload must be bytes")
        key = Ed25519PrivateKey.from_private_bytes(self.private_key)
        return key.sign(payload)


def load_api_key_credentials(
    *,
    api_key_id: str | None = None,
    api_private_key: str | bytes | None = None,
    from_env: bool = True,
) -> ApiKeyCredentials | None:
    key_id = api_key_id
    private = api_private_key
    if from_env:
        key_id = key_id or os.getenv(API_KEY_ID_ENV)
        private = private if private is not None else os.getenv(API_PRIVATE_KEY_ENV)
    if not key_id and not private:
        return None
    if not key_id or private is None:
        if from_env:
            message = "Both POLYESTER_API_KEY_ID and POLYESTER_API_PRIVATE_KEY are required"
        else:
            message = "Both api_key_id and api_private_key are required"
        raise PolyesterAuthError(message)
    return ApiKeyCredentials(key_id=key_id, private_key=normalize_private_key(private))


def normalize_private_key(value: str | bytes) -> bytes:
    if isinstance(value, bytes):
        private = value
    else:
        try:
            private = bytes.fromhex(value.strip())
        except ValueError as exc:
            raise PolyesterAuthError(
                "API private key must be a valid hex string or raw bytes"
            ) from exc
    if len(private) != 32:
        raise PolyesterAuthError("Ed25519 API private key must be exactly 32 bytes")
    return private


def generate_ed25519_keypair() -> tuple[bytes, bytes]:
    """Generate a new Ed25519 keypair (public, secret), each 32 bytes."""
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    return public_key.public_bytes_raw(), private_key.private_bytes_raw()


def sha256_hex(body: bytes) -> str:
    return hashlib.sha256(body).hexdigest()


def canonical_query(url: str) -> str:
    _validated_url(url)
    pairs = []
    for key, value in parse_qsl(urlsplit(url).query, keep_blank_values=True):
        pairs.append(f"{quote(key, safe='')}={quote(value, safe='')}")
    pairs.sort()
    return "&".join(pairs)


def canonical_signing_string(
    *,
    timestamp_ms: str,
    method: str,
    url: str,
    body: bytes,
) -> str:
    pathname = _validated_url(url).path or "/"
    return "\n".join(
        [timestamp_ms, method.upper(), pathname, canonical_query(url), sha256_hex(body)]
    )


def sign_request(
    credentials: ApiKeyCredentials,
    *,
    method: str,
    url: str,
    body: bytes = b"",
    timestamp_ms: str | None = None,
) -> dict[str, str]:
    timestamp = timestamp_ms or str(credentials._timestamp_allocator.next())
    return _sign_request_at_timestamp(
        credentials,
        method=method,
        url=url,
        body=body,
        timestamp=timestamp,
    )


async def sign_request_async(
    credentials: ApiKeyCredentials,
    *,
    method: str,
    url: str,
    body: bytes = b"",
    timestamp_ms: str | None = None,
) -> dict[str, str]:
    """Sign without blocking an async runtime while timestamp capacity recovers."""
    timestamp = timestamp_ms or str(await credentials._timestamp_allocator.next_async())
    return _sign_request_at_timestamp(
        credentials,
        method=method,
        url=url,
        body=body,
        timestamp=timestamp,
    )


def _sign_request_at_timestamp(
    credentials: ApiKeyCredentials,
    *,
    method: str,
    url: str,
    body: bytes,
    timestamp: str,
) -> dict[str, str]:
    canonical = canonical_signing_string(
        timestamp_ms=timestamp,
        method=method,
        url=url,
        body=body,
    )
    key = Ed25519PrivateKey.from_private_bytes(credentials.private_key)
    signature = key.sign(canonical.encode("utf-8")).hex()
    return {
        "X-API-KEY-ID": credentials.key_id,
        "X-API-TIMESTAMP": timestamp,
        "X-API-SIGNATURE": signature,
    }


def _validated_url(url: str):
    parsed = urlsplit(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise PolyesterAuthError(f"Cannot sign malformed absolute HTTP URL: {url!r}")
    return parsed
