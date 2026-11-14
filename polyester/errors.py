from __future__ import annotations

# Stable auth.v1.AuthErrorDetail codes used for MFA control flow.
# Prefer these over ConnectError message text.
AUTH_MFA_NOT_ENROLLED = "AUTH_MFA_NOT_ENROLLED"
AUTH_STEP_UP_REQUIRED = "AUTH_STEP_UP_REQUIRED"
AUTH_MFA_ELEVATION_REQUIRED = "AUTH_MFA_ELEVATION_REQUIRED"
AUTH_MFA_LAST_FACTOR_REQUIRED = "AUTH_MFA_LAST_FACTOR_REQUIRED"
AUTH_INTERNAL_ERROR = "AUTH_INTERNAL_ERROR"
# The account request changed nothing; retry the same request.
AUTH_TEMPORARILY_UNAVAILABLE = "AUTH_TEMPORARILY_UNAVAILABLE"

# Gateway code for an API-key request whose signed timestamp is outside the
# allowed skew window.
TIMESTAMP_SKEW = "TIMESTAMP_SKEW"

# Suffix of orders.v1.ErrorDetail codes for a mutation that was sent but not
# confirmed in time (e.g. ERROR_CODE_ORDER_CREATE_OUTCOME_UNKNOWN). The server
# may still have applied it: read back before retrying. Matching the suffix
# covers codes added to the enum later.
_OUTCOME_UNKNOWN_SUFFIX = "_OUTCOME_UNKNOWN"


class PolyesterError(Exception):
    """Base class for all SDK-raised errors."""


class PolyesterAuthError(PolyesterError):
    """Raised when credentials are missing or rejected."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        label: str | None = None,
        body: str | None = None,
        code: str | None = None,
        context: str | None = None,
        endpoint: str | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.label = label
        self.body = body
        self.code = code
        self.context = context or label
        self.endpoint = endpoint


class PolyesterValidationError(PolyesterError):
    """Raised when public SDK input cannot be converted to wire input."""


class PolyesterTransportError(PolyesterError):
    """Raised for network, timeout, or transport/runtime failures."""


class PolyesterResponseContractError(PolyesterError):
    """Raised when a successful mutation response violates its wire contract."""

    def __init__(self, context: str, message: str) -> None:
        super().__init__(f"{context}: {message}")
        self.context = context


class PolyesterRateLimitError(PolyesterTransportError):
    """Raised when the API returns a rate-limit response.

    ``detail`` is the structured ``polyester.ratelimit.v1.RateLimitDetail``
    payload when the server attached it. ``retry_after`` prefers
    ``detail.retry_after_ms``, then response headers when available.
    """

    def __init__(
        self,
        message: str,
        *,
        retry_after: float | None = None,
        detail: object | None = None,
    ) -> None:
        super().__init__(message)
        self.retry_after = retry_after
        self.detail = detail


class PolyesterServerError(PolyesterTransportError):
    """Raised for server-side 5xx failures."""


class PolyesterTimeoutError(PolyesterTransportError):
    """Raised when a request deadline expires before a response arrives.

    Retryable, but the outcome is unknown: a mutation may still have been
    applied, so reconcile before retrying it (see :func:`mutation_outcome_unknown`).
    """


class PolyesterTimestampSkewError(PolyesterTransportError):
    """Raised when the API-key request timestamp is outside the allowed skew window.

    Retryable: the gateway rejected the request before any service saw it,
    and a retry signs it again with a fresh timestamp. If it persists, the
    local clock is wrong. For large bursts, bound concurrency so requests do
    not wait locally past the skew window.
    """

    code = TIMESTAMP_SKEW

    def __init__(
        self,
        message: str = "API key timestamp is outside the allowed skew window.",
        *,
        status_code: int | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code


class PolyesterApiError(PolyesterError):
    """Raised for structured Connect/API errors.

    ``existing_order_id`` is set on an ``ERROR_CODE_CONFLICT_DUPLICATE_CLIENT_ORDER_ID``
    order rejection: the public ID of the order that already holds the client
    order ID, when the server knows it.
    """

    def __init__(
        self,
        message: str,
        *,
        code: str | None = None,
        metadata: dict[str, str] | None = None,
        raw: object | None = None,
        existing_order_id: str | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.metadata = metadata or {}
        self.raw = raw
        self.existing_order_id = existing_order_id


def auth_error_code(err: BaseException) -> str | None:
    """Return the structured auth.v1.AuthErrorDetail code when present."""
    if isinstance(err, PolyesterApiError) and err.code:
        return err.code
    return None


def is_mfa_enrollment_required(err: BaseException) -> bool:
    """True when the caller must enroll an MFA factor before continuing."""
    return auth_error_code(err) == AUTH_MFA_NOT_ENROLLED


def is_step_up_required(err: BaseException) -> bool:
    """True when the caller must retry with a fresh X-Auth-Step-Up proof."""
    return auth_error_code(err) == AUTH_STEP_UP_REQUIRED


def is_mfa_elevation_required(err: BaseException) -> bool:
    """True when the caller needs a recent MFA-elevated interactive session."""
    return auth_error_code(err) == AUTH_MFA_ELEVATION_REQUIRED


def is_mfa_last_factor_required(err: BaseException) -> bool:
    """True when the final active MFA factor cannot be removed."""
    return auth_error_code(err) == AUTH_MFA_LAST_FACTOR_REQUIRED


class PolyesterNotImplementedError(PolyesterApiError):
    """Raised for HTTP 501 or Connect ``unimplemented``: the server does not
    offer this RPC or feature. Not retryable."""

    def __init__(self, message: str, *, code: str | None = "unimplemented") -> None:
        super().__init__(message, code=code)


class PolyesterRouteNotFoundError(PolyesterNotImplementedError):
    """Raised when the gateway has no route for a Connect RPC (plain HTTP 404)."""

    def __init__(self, procedure: str | None = None) -> None:
        hint = (
            f"RPC not exposed on this API host{f': {procedure}' if procedure else ''}. "
            "The procedure may be unimplemented on devnet or disabled in this environment."
        )
        super().__init__(hint, code="route_not_found")
        self.procedure = procedure


def is_not_found(err: BaseException) -> bool:
    """Return whether an API error means the requested resource is absent.

    Gateway route 404s are intentionally excluded: an unavailable RPC is not a
    successful idempotent delete/cancel.
    """
    if not isinstance(err, PolyesterApiError) or isinstance(err, PolyesterRouteNotFoundError):
        return False
    code = str(err.code or "").strip().lower().replace("-", "_")
    return code == "not_found" or code.endswith("_not_found")


class PolyesterRealtimeError(PolyesterError):
    """Raised for realtime connection, subscription, or decode failures.

    ``code`` is the private WebSocket request error code (for example
    ``FORBIDDEN``); ``close_code`` is the WebSocket close code that ended the
    stream (for example ``4403``). Both are ``None`` when not applicable.
    """

    def __init__(
        self,
        message: str = "",
        *,
        code: str | None = None,
        close_code: int | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.close_code = close_code


class PolyesterRealtimeOverflowError(PolyesterRealtimeError):
    """Raised when a realtime subscription queue is full.

    Subscriptions fail instead of silently dropping updates so callers can
    recover (reconnect, resubscribe, or slow their consumer).
    """


def _is_outcome_unknown_api_error(err: BaseException) -> bool:
    return (
        isinstance(err, PolyesterApiError)
        and err.code is not None
        and err.code.endswith(_OUTCOME_UNKNOWN_SUFFIX)
    )


def is_retryable_error(err: BaseException) -> bool:
    """Return whether retrying may succeed after backoff.

    True for transport, rate-limit, timestamp-skew and server errors, and for
    ``AUTH_TEMPORARILY_UNAVAILABLE`` (the request changed nothing).

    False for an order or trigger create, cancel, modify or control whose
    outcome is unknown (``ERROR_CODE_*_OUTCOME_UNKNOWN``): the server may
    have applied it, so a blind retry could, for example, place an order
    twice. Read the order or trigger back first; see
    :func:`mutation_outcome_unknown`.

    A true result does not guarantee that a mutation was not applied: a
    timeout is retryable but may still have applied. Preserve the original
    idempotency key and reconcile first when :func:`mutation_outcome_unknown`
    returns true.
    """
    if _is_outcome_unknown_api_error(err):
        return False
    if isinstance(err, PolyesterApiError) and err.code == AUTH_TEMPORARILY_UNAVAILABLE:
        return True
    return isinstance(
        err,
        (PolyesterTransportError, PolyesterRateLimitError, PolyesterServerError),
    )


def mutation_outcome_unknown(err: BaseException) -> bool:
    """Return whether the server may have applied a failed mutation.

    True for transport and server errors (except rate limits and timestamp
    skew, which the gateway rejects before any service sees the request), for
    a malformed success response, and for an order or trigger create, cancel,
    modify or control that was sent but not confirmed in time
    (``ERROR_CODE_*_OUTCOME_UNKNOWN``). Read the order or trigger back before
    retrying.
    """
    return (
        isinstance(err, PolyesterResponseContractError)
        or _is_outcome_unknown_api_error(err)
        or (
            isinstance(err, (PolyesterTransportError, PolyesterServerError))
            and not isinstance(err, (PolyesterRateLimitError, PolyesterTimestampSkewError))
        )
    )
