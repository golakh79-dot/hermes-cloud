from __future__ import annotations

from datetime import datetime
from typing import Any

import msgspec


class MeResult(msgspec.Struct, kw_only=True, omit_defaults=True):
    account_id: str = ""
    api_key_id: str = ""
    username: str = ""
    root_smart_account_address: str = ""
    session: dict[str, Any] | None = None


class UserProfile(msgspec.Struct, kw_only=True, omit_defaults=True):
    username: str = ""
    bio: str = ""
    website: str = ""
    twitter: str = ""
    twitter_verified: bool = False
    discord: str = ""
    discord_verified: bool = False
    avatar_url: str = ""
    created_at: datetime | None = None
    next_username_change_at: datetime | None = None
    vip_tier: int = 0
    username_unlocked: bool = False


class UsernameHistoryEntry(msgspec.Struct, kw_only=True, omit_defaults=True):
    username: str = ""
    set_at: datetime | None = None


class UsernameHistoryList(msgspec.Struct, kw_only=True, omit_defaults=True):
    history: list[UsernameHistoryEntry] = msgspec.field(default_factory=list)


class AccountIdentity(msgspec.Struct, kw_only=True, omit_defaults=True):
    account_id: str = ""
    username: str = ""
    avatar_url: str = ""
    root_smart_account_address: str = ""


class Ed25519Keypair(msgspec.Struct, kw_only=True):
    public_key_hex: str
    public_key: bytes
    secret_key_hex: str
    secret_key: bytes

    def __repr__(self) -> str:
        return (
            f"Ed25519Keypair(public_key_hex={self.public_key_hex!r}, "
            "secret_key_hex='[REDACTED]', secret_key='[REDACTED]')"
        )
