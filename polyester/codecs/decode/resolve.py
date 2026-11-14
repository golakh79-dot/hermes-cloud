from __future__ import annotations

from polyester.codecs.proto_helpers import format_uint64_id, proto_enum_name
from polyester.gen.auth.v1 import resolve_pb2
from polyester.models import ResolvedAccount, ResolvedAccountsList


def resolved_account_from_proto(msg: resolve_pb2.ResolvedAccount) -> ResolvedAccount:
    return ResolvedAccount(
        smart_account_address=msg.smart_account_address,
        kind=proto_enum_name(resolve_pb2.ResolvedAccount.Kind, msg.kind),
        root_username=msg.root_username,
        subaccount_label=msg.subaccount_label,
        account_id=format_uint64_id(msg.account_id),
    )


def resolved_accounts_from_proto(msg: resolve_pb2.ResolveAccountResponse) -> ResolvedAccountsList:
    return ResolvedAccountsList(matches=[resolved_account_from_proto(item) for item in msg.matches])
