from __future__ import annotations

import msgspec


class AddressBookViewInvalidation(msgspec.Struct, kw_only=True, omit_defaults=True):
    scope: str = ""
    invalidated_at: str = ""
    view_revision: int = 0


class OrderBookDeltaUpdate(msgspec.Struct, kw_only=True, omit_defaults=True):
    symbol_id: int = 0
    book_seq_start: str = ""
    book_seq_end: str = ""
    reset: bool = False
    bids: list[tuple[str, str]] = msgspec.field(default_factory=list)
    asks: list[tuple[str, str]] = msgspec.field(default_factory=list)
