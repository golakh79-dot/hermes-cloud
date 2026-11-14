from __future__ import annotations

from polyester._wire import protobuf_to_public_dict
from polyester.codecs.proto_helpers import format_uint64_id
from polyester.codecs.scalars import timestamp_dict_to_datetime
from polyester.gen.auth.v1 import auth_pb2, profile_pb2
from polyester.models.auth import (
    MeResult,
    UsernameHistoryEntry,
    UsernameHistoryList,
    UserProfile,
)


def me_from_proto(msg: auth_pb2.MeResponse) -> MeResult:
    session = None
    if msg.HasField("session"):
        session = protobuf_to_public_dict(msg.session)
    return MeResult(
        account_id=format_uint64_id(msg.account_id) if msg.account_id else "",
        api_key_id=(msg.api_key_id or "").strip(),
        username=msg.username,
        root_smart_account_address=msg.root_smart_account_address,
        session=session,
    )


def profile_from_proto(msg: profile_pb2.UserProfile) -> UserProfile:
    return UserProfile(
        username=msg.username,
        bio=msg.bio,
        website=msg.website,
        twitter=msg.twitter,
        twitter_verified=msg.twitter_verified,
        discord=msg.discord,
        discord_verified=msg.discord_verified,
        avatar_url=msg.avatar_url,
        created_at=timestamp_dict_to_datetime(msg.created_at),
        next_username_change_at=timestamp_dict_to_datetime(msg.next_username_change_at),
        vip_tier=msg.vip_tier,
        username_unlocked=msg.username_unlocked,
    )


def username_history_from_proto(
    msg: profile_pb2.GetUsernameHistoryResponse,
) -> UsernameHistoryList:
    return UsernameHistoryList(
        history=[
            UsernameHistoryEntry(
                username=entry.username,
                set_at=timestamp_dict_to_datetime(entry.set_at),
            )
            for entry in msg.history
        ]
    )
