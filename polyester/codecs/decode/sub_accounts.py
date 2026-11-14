from __future__ import annotations

from polyester.codecs.decode.api_keys import api_key_from_proto
from polyester.codecs.decode.policies import subaccount_policy_from_proto
from polyester.codecs.proto_helpers import format_uint64_id, has_field, proto_enum_name
from polyester.codecs.scalars import timestamp_dict_to_datetime
from polyester.gen.auth.v1 import subaccounts_pb2
from polyester.models.sub_accounts import (
    GetSubaccountResult,
    SubAccount,
    SubAccountActivityEvent,
    SubAccountActivityList,
    SubAccountInvite,
    SubAccountInvitesList,
    SubAccountMember,
    SubAccountMembersList,
    SubAccountsList,
)


def _subaccount_role_from_proto(value: int) -> str:
    name = proto_enum_name(subaccounts_pb2.SubaccountRole, value)
    if name in {"", "subaccount_role_unspecified"}:
        return "viewer"
    return name


def _invite_status_from_proto(value: int) -> str:
    name = proto_enum_name(subaccounts_pb2.SubaccountInviteStatus, value)
    if name.startswith("subaccount_invite_status_"):
        return name.removeprefix("subaccount_invite_status_")
    return name or "pending"


def _subaccount_status_from_proto(value: int) -> str:
    return proto_enum_name(subaccounts_pb2.SubaccountStatus, value)


def subaccount_from_proto(msg: subaccounts_pb2.Subaccount) -> SubAccount:
    return SubAccount(
        id=format_uint64_id(msg.id),
        role=_subaccount_role_from_proto(msg.role),
        label=msg.label,
        icon=msg.icon,
        color=msg.color,
        status=_subaccount_status_from_proto(msg.status),
        smart_account_address=msg.smart_account_address,
        owner_username=msg.owner_username,
        owner_avatar_url=msg.owner_avatar_url,
        owner_root_smart_account_address=msg.owner_root_smart_account_address,
        subaccount_policy_id=format_uint64_id(msg.subaccount_policy_id),
        require_member_mfa=bool(msg.require_member_mfa),
        smart_account_salt_nonce=int(msg.smart_account_salt_nonce),
        updated_at=timestamp_dict_to_datetime(msg.updated_at),
        revision=int(msg.revision),
    )


def subaccounts_list_from_proto(msg: subaccounts_pb2.ListSubaccountsResponse) -> SubAccountsList:
    return SubAccountsList(
        subaccounts=[subaccount_from_proto(item) for item in msg.subaccounts],
        total_created=int(msg.total_created),
    )


def subaccount_member_from_proto(msg: subaccounts_pb2.SubaccountMemberView) -> SubAccountMember:
    return SubAccountMember(
        account_id=format_uint64_id(msg.account_id),
        role=_subaccount_role_from_proto(msg.role),
        username=msg.username,
        smart_account_address=msg.smart_account_address,
        avatar_url=msg.avatar_url,
        mfa_enrolled=bool(msg.mfa_enrolled),
    )


def subaccount_members_list_from_proto(
    msg: subaccounts_pb2.ListSubaccountMembersResponse,
) -> SubAccountMembersList:
    return SubAccountMembersList(
        members=[subaccount_member_from_proto(item) for item in msg.members]
    )


def subaccount_invite_from_proto(msg: subaccounts_pb2.SubaccountInvite) -> SubAccountInvite:
    return SubAccountInvite(
        id=format_uint64_id(msg.id),
        subaccount_id=format_uint64_id(msg.subaccount_id),
        grantee_account_id=format_uint64_id(msg.grantee_account_id),
        inviter_account_id=format_uint64_id(msg.inviter_account_id),
        role=_subaccount_role_from_proto(msg.role),
        status=_invite_status_from_proto(msg.status),
        created_at=timestamp_dict_to_datetime(msg.created_at),
        responded_at=timestamp_dict_to_datetime(msg.responded_at),
        grantee_username=msg.grantee_username,
        inviter_username=msg.inviter_username,
        subaccount_label=msg.subaccount_label,
        inviter_root_smart_account_address=msg.inviter_root_smart_account_address,
        grantee_root_smart_account_address=msg.grantee_root_smart_account_address,
        require_member_mfa=bool(msg.require_member_mfa),
    )


def subaccount_invites_list_from_proto(
    msg: subaccounts_pb2.ListSubaccountInvitesResponse,
) -> SubAccountInvitesList:
    return SubAccountInvitesList(
        invites=[subaccount_invite_from_proto(item) for item in msg.invites]
    )


def subaccount_activity_event_from_proto(
    msg: subaccounts_pb2.ActivityEvent,
) -> SubAccountActivityEvent:
    return SubAccountActivityEvent(
        created_at=timestamp_dict_to_datetime(msg.created_at),
        entity_kind=proto_enum_name(
            subaccounts_pb2.ActivityEntityKind, msg.entity_kind
        ).removeprefix("activity_entity_"),
        event_action=proto_enum_name(
            subaccounts_pb2.ActivityEventAction, msg.event_action
        ).removeprefix("activity_action_"),
        source=proto_enum_name(subaccounts_pb2.ActivityEventSource, msg.source).removeprefix(
            "activity_source_"
        ),
        ip=msg.ip,
        user_agent=msg.user_agent,
        actor_account_id=format_uint64_id(msg.actor_account_id),
        payload_json=msg.payload_json,
    )


def subaccount_activity_list_from_proto(
    msg: subaccounts_pb2.ListSubaccountEventsResponse,
) -> SubAccountActivityList:
    return SubAccountActivityList(
        events=[subaccount_activity_event_from_proto(item) for item in msg.events],
        next_page_token=msg.next_page_token,
    )


def get_subaccount_from_proto(msg: subaccounts_pb2.GetSubaccountResponse) -> GetSubaccountResult:
    subaccount = subaccount_from_proto(msg.subaccount) if has_field(msg, "subaccount") else None
    policy = subaccount_policy_from_proto(msg.policy) if has_field(msg, "policy") else None
    return GetSubaccountResult(
        subaccount=subaccount,
        api_keys=[api_key_from_proto(item) for item in msg.api_keys],
        members=[subaccount_member_from_proto(item) for item in msg.members],
        invites=[subaccount_invite_from_proto(item) for item in msg.invites],
        policy=policy,
    )
