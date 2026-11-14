from __future__ import annotations

from datetime import datetime

import msgspec

from polyester.models.policies import SubaccountPolicy
from polyester.models.trading import ApiKeySummary


class SubAccount(msgspec.Struct, kw_only=True, omit_defaults=True):
    id: str = ""
    role: str = ""
    label: str = ""
    icon: str = ""
    color: str = ""
    status: str = ""
    smart_account_address: str = ""
    owner_username: str = ""
    owner_avatar_url: str = ""
    owner_root_smart_account_address: str = ""
    subaccount_policy_id: str = ""
    require_member_mfa: bool = False
    smart_account_salt_nonce: int = 0
    updated_at: datetime | None = None
    revision: int = 0


class SubAccountsList(msgspec.Struct, kw_only=True, omit_defaults=True):
    subaccounts: list[SubAccount]
    total_created: int = 0


class CreateSubaccountResult(msgspec.Struct, kw_only=True, omit_defaults=True):
    subaccount_id: str = ""
    total_created: int = 0
    smart_account_salt_nonce: int = 0
    revision: int = 0


class SubAccountMember(msgspec.Struct, kw_only=True, omit_defaults=True):
    account_id: str = ""
    role: str = ""
    username: str = ""
    smart_account_address: str = ""
    avatar_url: str = ""
    mfa_enrolled: bool = False


class SubAccountMembersList(msgspec.Struct, kw_only=True, omit_defaults=True):
    members: list[SubAccountMember]


class SubAccountInvite(msgspec.Struct, kw_only=True, omit_defaults=True):
    id: str = ""
    subaccount_id: str = ""
    grantee_account_id: str = ""
    inviter_account_id: str = ""
    role: str = ""
    status: str = ""
    created_at: datetime | None = None
    responded_at: datetime | None = None
    grantee_username: str = ""
    inviter_username: str = ""
    subaccount_label: str = ""
    inviter_root_smart_account_address: str = ""
    grantee_root_smart_account_address: str = ""
    require_member_mfa: bool = False


class SubAccountInvitesList(msgspec.Struct, kw_only=True, omit_defaults=True):
    invites: list[SubAccountInvite]


class SubAccountActivityEvent(msgspec.Struct, kw_only=True, omit_defaults=True):
    created_at: datetime | None = None
    entity_kind: str = ""
    event_action: str = ""
    source: str = ""
    ip: str = ""
    user_agent: str = ""
    actor_account_id: str = ""
    payload_json: str = ""


class SubAccountActivityList(msgspec.Struct, kw_only=True, omit_defaults=True):
    events: list[SubAccountActivityEvent]
    next_page_token: str = ""


class GetSubaccountResult(msgspec.Struct, kw_only=True, omit_defaults=True):
    subaccount: SubAccount | None = None
    api_keys: list[ApiKeySummary] = []
    members: list[SubAccountMember] = []
    invites: list[SubAccountInvite] = []
    policy: SubaccountPolicy | None = None
