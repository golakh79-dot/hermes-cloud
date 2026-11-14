from __future__ import annotations

import msgspec


class GuardSignerStatus(msgspec.Struct, kw_only=True, omit_defaults=True):
    signer_address: str = ""
    onchain_signer_address: str = ""
    initialized: bool = False
    nonce: str = ""
    nonce_space: str = "0"


class GuardApproval(msgspec.Struct, kw_only=True, omit_defaults=True):
    nonce_space: str = "0"
    deadline_unix: str = "0"
    signature: str = ""


class CreateGuardSignerWalletResult(msgspec.Struct, kw_only=True, omit_defaults=True):
    signer_address: str = ""


class RotateGuardSignerWalletResult(msgspec.Struct, kw_only=True, omit_defaults=True):
    new_signer_address: str = ""
    approval: GuardApproval | None = None


class ExportGuardSignerWalletResult(msgspec.Struct, kw_only=True, omit_defaults=True):
    private_key: str = ""

    def __repr__(self) -> str:
        return "ExportGuardSignerWalletResult(private_key='[REDACTED]')"


class BatchSignProtectedActionsResult(msgspec.Struct, kw_only=True, omit_defaults=True):
    approvals: list[GuardApproval]
