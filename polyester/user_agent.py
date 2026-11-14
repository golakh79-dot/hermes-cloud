"""Stable HTTP User-Agent for all Polyester SDK outbound requests.

Edge WAF rules have historically banned default library User-Agents
(``python-requests/*``, ``python-httpx/*``) with Cloudflare error 1010
before authentication runs. SDKs must send an explicit Polyester identity
instead of relying on the HTTP client's default.
"""

from __future__ import annotations

from polyester._version import __version__

USER_AGENT = f"polyester-sdk-python/{__version__}"
USER_AGENT_HEADER = "User-Agent"

# Cloudflare "browser signature banned" HTML / challenge pages.
_CLOUDFLARE_1010_MARKERS = (
    "error code: 1010",
    "error code 1010",
)


def is_cloudflare_browser_ban(body: str | None) -> bool:
    """True when a response body looks like Cloudflare error 1010."""
    if not body:
        return False
    lowered = body.lower()
    if any(marker in lowered for marker in _CLOUDFLARE_1010_MARKERS):
        return True
    # Generic CF interstitial often paired with 1010 when UA is banned.
    return "attention required" in lowered and "cloudflare" in lowered


def cloudflare_1010_message() -> str:
    return (
        "Request blocked by edge WAF (Cloudflare error 1010: browser signature banned). "
        "This is not an API authentication failure. "
        f"Retry with User-Agent {USER_AGENT!r} (set automatically by this SDK)."
    )
