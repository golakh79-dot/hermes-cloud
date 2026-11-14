"""Shared imports for on-chain Funding helpers."""

from __future__ import annotations

import eth_abi  # noqa: F401
from eth_utils import function_signature_to_4byte_selector  # noqa: F401


def require_eth_abi() -> None:
    """No-op retained for call sites; eth-abi is a required dependency."""
