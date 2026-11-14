from __future__ import annotations

from polyester.errors import PolyesterResponseContractError
from polyester.gen.chain.withdraw.v1 import withdraw_pb2
from polyester.models import WithdrawDestinationValidation, WithdrawIntentResult

_VALIDATION_CODE_LABELS = {
    int(withdraw_pb2.RESULT_UNSPECIFIED): "unspecified",
    int(withdraw_pb2.VALID): "valid",
    int(withdraw_pb2.INVALID_ADDRESS): "invalid_address",
    int(withdraw_pb2.UNSUPPORTED_CHAIN): "unsupported_chain",
    int(withdraw_pb2.POLYESTER_SMART_ACCOUNT): "polyester_smart_account",
    int(withdraw_pb2.TOKEN_CONTRACT): "token_contract",
    int(withdraw_pb2.DENYLISTED_ADDRESS): "denylisted_address",
}


def withdraw_destination_validation_code_label(code: int) -> str:
    value = int(code)
    return _VALIDATION_CODE_LABELS.get(value, f"unknown_code_{value}")


def withdraw_intent_from_proto(
    msg: withdraw_pb2.CreateTradingWithdrawResponse
    | withdraw_pb2.CreateWalletTradingWithdrawResponse,
) -> WithdrawIntentResult:
    if not msg.intent_id.strip():
        raise PolyesterResponseContractError(
            type(msg).__name__, "missing intent_id"
        )
    return WithdrawIntentResult(intent_id=msg.intent_id)


def withdraw_destination_validation_from_proto(
    msg: withdraw_pb2.ValidateWithdrawDestinationResponse,
) -> WithdrawDestinationValidation:
    return WithdrawDestinationValidation(
        valid=bool(msg.valid),
        code=withdraw_destination_validation_code_label(int(msg.code)),
        message=str(msg.message or ""),
        canonical_destination_address=str(msg.canonical_destination_address or ""),
    )
