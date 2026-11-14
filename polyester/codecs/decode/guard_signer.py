from __future__ import annotations

from polyester.codecs.proto_helpers import bytes_to_hex
from polyester.gen.chain.guard.v1 import guard_signer_pb2
from polyester.models.guard_signer import (
    BatchSignProtectedActionsResult,
    CreateGuardSignerWalletResult,
    ExportGuardSignerWalletResult,
    GuardApproval,
    GuardSignerStatus,
    RotateGuardSignerWalletResult,
)


def guard_approval_from_proto(msg: guard_signer_pb2.GuardApproval) -> GuardApproval:
    return GuardApproval(
        nonce_space=str(msg.nonce_space),
        deadline_unix=str(msg.deadline_unix),
        signature=bytes_to_hex(msg.signature),
    )


def guard_signer_status_from_proto(msg: guard_signer_pb2.GuardSignerStatus) -> GuardSignerStatus:
    return GuardSignerStatus(
        signer_address=msg.signer_address,
        onchain_signer_address=msg.onchain_signer_address,
        initialized=bool(msg.initialized),
        nonce=msg.nonce,
        nonce_space=str(msg.nonce_space),
    )


def create_wallet_from_proto(
    msg: guard_signer_pb2.CreateGuardSignerWalletResponse,
) -> CreateGuardSignerWalletResult:
    return CreateGuardSignerWalletResult(signer_address=msg.signer_address)


def status_from_proto(
    msg: guard_signer_pb2.GetGuardSignerStatusResponse,
) -> GuardSignerStatus | None:
    if msg.HasField("status"):
        return guard_signer_status_from_proto(msg.status)
    return None


def sign_protected_action_from_proto(
    msg: guard_signer_pb2.SignProtectedActionResponse,
) -> GuardApproval | None:
    if msg.HasField("approval"):
        return guard_approval_from_proto(msg.approval)
    return None


def batch_sign_from_proto(
    msg: guard_signer_pb2.BatchSignProtectedActionsResponse,
) -> BatchSignProtectedActionsResult:
    return BatchSignProtectedActionsResult(
        approvals=[guard_approval_from_proto(item) for item in msg.approvals]
    )


def rotate_wallet_from_proto(
    msg: guard_signer_pb2.RotateGuardSignerWalletResponse,
) -> RotateGuardSignerWalletResult:
    approval = None
    if msg.HasField("approval"):
        approval = guard_approval_from_proto(msg.approval)
    return RotateGuardSignerWalletResult(
        new_signer_address=msg.new_signer_address,
        approval=approval,
    )


def export_wallet_from_proto(
    msg: guard_signer_pb2.ExportGuardSignerWalletResponse,
) -> ExportGuardSignerWalletResult:
    return ExportGuardSignerWalletResult(private_key=msg.private_key)
