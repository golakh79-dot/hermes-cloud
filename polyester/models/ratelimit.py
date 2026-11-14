from __future__ import annotations

import msgspec


class RateLimitDetail(msgspec.Struct, kw_only=True, omit_defaults=True):
    """Client-safe quota rejection detail from polyester.ratelimit.v1."""

    reason: str = ""
    limit: int | None = None
    remaining: int | None = None
    retry_after_ms: int | None = None
    policy_version: int | None = None
    operation_id: str = ""
    policy_class: str = ""
    scope: str = ""
    refill_model: str = ""
