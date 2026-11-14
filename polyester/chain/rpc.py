"""Minimal JSON-RPC helpers for chain RPC / bundler / paymaster."""

from __future__ import annotations

import asyncio
import contextlib
import itertools
import json
import threading
import time
from collections.abc import Iterator
from typing import Any

import httpx

from polyester.user_agent import USER_AGENT, USER_AGENT_HEADER

# Reject oversized JSON-RPC bodies before decode (DoS / memory).
MAX_JSONRPC_RESPONSE_BYTES = 1 * 1024 * 1024
_HTTP_HEADERS = {USER_AGENT_HEADER: USER_AGENT}


class JsonRpcError(RuntimeError):
    def __init__(self, message: str, *, code: int | None = None, data: Any = None) -> None:
        super().__init__(message)
        self.code = code
        self.data = data


class JsonRpcClient:
    def __init__(self, url: str, *, timeout: float = 60.0) -> None:
        self._url = url
        self._timeout = timeout
        # itertools.count next() is atomic under the CPython GIL (thread-safe enough
        # for concurrent request()/arequest() callers sharing one client).
        self._ids = itertools.count(1)

    def request(self, method: str, params: list[Any] | None = None) -> Any:
        req_id = next(self._ids)
        payload = {
            "jsonrpc": "2.0",
            "id": req_id,
            "method": method,
            "params": params or [],
        }
        deadline = time.monotonic() + self._timeout
        # httpx Timeout is per-phase, not a total wall clock. Enforce an absolute
        # deadline via a closer that aborts the client at ``deadline`` plus
        # between-chunk checks (covers stall and slow-drip without worker threads).
        with (
            httpx.Client(
                timeout=httpx.Timeout(self._timeout),
                headers=_HTTP_HEADERS,
            ) as client,
            _deadline_client_close(client, deadline),
        ):
            try:
                with client.stream("POST", self._url, json=payload) as response:
                    response.raise_for_status()
                    raw = _read_limited_sync(
                        response,
                        MAX_JSONRPC_RESPONSE_BYTES,
                        deadline=deadline,
                    )
            except httpx.TimeoutException as exc:
                raise JsonRpcError("json-rpc timed out") from exc
            except (httpx.HTTPError, OSError) as exc:
                if time.monotonic() >= deadline:
                    raise JsonRpcError("json-rpc timed out") from exc
                raise
        return _decode_jsonrpc_envelope(raw, expected_id=req_id)

    async def arequest(self, method: str, params: list[Any] | None = None) -> Any:
        req_id = next(self._ids)
        payload = {
            "jsonrpc": "2.0",
            "id": req_id,
            "method": method,
            "params": params or [],
        }
        try:
            async with asyncio.timeout(self._timeout):
                async with httpx.AsyncClient(
                    timeout=self._timeout,
                    headers=_HTTP_HEADERS,
                ) as client, client.stream("POST", self._url, json=payload) as response:
                    response.raise_for_status()
                    raw = await _read_limited(response, MAX_JSONRPC_RESPONSE_BYTES)
        except TimeoutError as exc:
            raise JsonRpcError("json-rpc timed out") from exc
        except httpx.TimeoutException as exc:
            raise JsonRpcError("json-rpc timed out") from exc
        return _decode_jsonrpc_envelope(raw, expected_id=req_id)


@contextlib.contextmanager
def _deadline_client_close(client: httpx.Client, deadline: float) -> Iterator[None]:
    """Close ``client`` at ``deadline`` so a blocked sync read cannot outlive it.

    The timer is cancelled on exit, so successful calls leave no worker threads.
    Closing the client unblocks in-flight stream reads without a dedicated worker
    pool or leaked connections.
    """
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise JsonRpcError("json-rpc timed out")
    timer = threading.Timer(remaining, client.close)
    timer.daemon = True
    timer.start()
    try:
        yield
    finally:
        timer.cancel()


def _content_length_exceeds(response: httpx.Response, max_bytes: int) -> bool:
    raw = response.headers.get("content-length")
    if raw is None:
        return False
    try:
        return int(raw) > max_bytes
    except ValueError:
        return False


def _read_limited_sync(
    response: httpx.Response,
    max_bytes: int,
    *,
    deadline: float,
) -> bytes:
    if _content_length_exceeds(response, max_bytes):
        raise JsonRpcError(f"json-rpc response exceeds {max_bytes} bytes")
    chunks: list[bytes] = []
    total = 0
    for chunk in response.iter_bytes():
        if time.monotonic() >= deadline:
            response.close()
            raise JsonRpcError("json-rpc timed out")
        total += len(chunk)
        if total > max_bytes:
            raise JsonRpcError(f"json-rpc response exceeds {max_bytes} bytes")
        chunks.append(chunk)
    if time.monotonic() >= deadline:
        raise JsonRpcError("json-rpc timed out")
    return b"".join(chunks)


async def _read_limited(response: httpx.Response, max_bytes: int) -> bytes:
    if _content_length_exceeds(response, max_bytes):
        raise JsonRpcError(f"json-rpc response exceeds {max_bytes} bytes")
    chunks: list[bytes] = []
    total = 0
    async for chunk in response.aiter_bytes():
        total += len(chunk)
        if total > max_bytes:
            raise JsonRpcError(f"json-rpc response exceeds {max_bytes} bytes")
        chunks.append(chunk)
    return b"".join(chunks)


def _decode_jsonrpc_envelope(raw: bytes, *, expected_id: int) -> Any:
    try:
        body = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise JsonRpcError("json-rpc response is not valid JSON") from exc
    if not isinstance(body, dict):
        raise JsonRpcError("json-rpc response must be a JSON object")
    if body.get("jsonrpc") != "2.0":
        raise JsonRpcError('json-rpc response must have jsonrpc="2.0"')
    if "id" not in body or body["id"] != expected_id:
        raise JsonRpcError(
            f"json-rpc response id mismatch: expected {expected_id}, got {body.get('id')!r}"
        )
    has_result = "result" in body
    has_error = "error" in body and body["error"] is not None
    if has_result == has_error:
        raise JsonRpcError("json-rpc response must contain exactly one of result|error")
    if has_error:
        err = body["error"]
        if not isinstance(err, dict):
            raise JsonRpcError("json-rpc error must be an object")
        raise JsonRpcError(
            str(err.get("message", err)),
            code=err.get("code") if isinstance(err.get("code"), int) else None,
            data=err.get("data"),
        )
    # ``result: null`` is a valid JSON-RPC success (has_result True).
    return body["result"]
