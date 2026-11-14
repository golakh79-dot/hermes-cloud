from __future__ import annotations

from typing import Any, Literal

from polyester.codecs.scalars import format_id
from polyester.errors import PolyesterValidationError

AccountScope = Literal["main", "active"] | str | dict[str, str]


def resolve_sub_account_id(value: str | None, default: str | None) -> str | None:
    if value == "":
        return None
    return value if value is not None else default


def scoped_sub_account_id(
    *,
    account: AccountScope | None = None,
    sub_account_id: str | None = None,
    default: str | None = None,
) -> str | None:
    """Resolve sub-account scope from TS-style ``account`` or legacy ``sub_account_id``."""
    return resolve_sub_account_from_scope(
        account=account,
        sub_account_id=sub_account_id,
        default=default,
    )


def resolve_sub_account_from_scope(
    *,
    account: AccountScope | None = None,
    sub_account_id: str | None = None,
    default: str | None = None,
) -> str | None:
    if sub_account_id is not None and account is not None:
        raise PolyesterValidationError("Pass account or sub_account_id, not both")
    if sub_account_id is not None:
        return resolve_sub_account_id(sub_account_id, default)
    if account is None or account == "active" or account == "main":
        return resolve_sub_account_id(None, default)
    if isinstance(account, dict):
        scoped = account.get("subaccountId") or account.get("sub_account_id")
        if not scoped:
            raise PolyesterValidationError("account dict requires subaccountId or sub_account_id")
        return str(scoped)
    if isinstance(account, str):
        return resolve_sub_account_id(account, default)
    raise PolyesterValidationError("account must be 'main', 'active', a subaccount id, or a dict")


def resolve_account_id(value: str | int | None, default: str | int | None) -> str:
    if value is not None and value != "":
        return str(value)
    if default is not None and default != "":
        return str(default)
    raise PolyesterValidationError(
        "account_id is required; set POLYESTER_ACCOUNT_ID or pass account_id explicitly"
    )


def lifecycle_account_fields(msg: Any) -> dict[str, str]:
    fields: dict[str, str] = {}
    owner_account_id = int(getattr(msg, "owner_account_id", 0) or 0)
    smart_account_address = str(getattr(msg, "smart_account_address", "") or "")
    if owner_account_id:
        fields["owner_account_id"] = format_id(owner_account_id)
    if smart_account_address:
        fields["smart_account_address"] = smart_account_address
    return fields


class ScopedSubAccountMixin:
    """Shared ``account`` / ``sub_account_id`` resolution for trading services."""

    _default_sub_account_id: str | None

    def _resolve_sub_account_id(
        self,
        sub_account_id: str | int | None = None,
        *,
        account: AccountScope | None = None,
    ) -> str | None:
        scoped = sub_account_id if sub_account_id is None else str(sub_account_id)
        return scoped_sub_account_id(
            account=account,
            sub_account_id=scoped,
            default=self._default_sub_account_id,
        )
