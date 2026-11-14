from __future__ import annotations

from polyester.codecs.ledger_amounts import LEDGER_SCALE
from polyester.errors import PolyesterResponseContractError
from polyester.gen.transfer.v1 import internal_transfer_pb2
from polyester.models import InternalTransferResult
from polyester.types.money import AssetAmount, QuantityDomain


def _u128_scaled(msg) -> int:
    if msg is None:
        return 0
    return (int(getattr(msg, "hi", 0) or 0) << 64) + int(getattr(msg, "lo", 0) or 0)


def internal_transfer_from_proto(
    msg: internal_transfer_pb2.CreateInternalTransferResponse,
) -> InternalTransferResult:
    if not msg.request_id.strip() or not msg.transfer_id.strip():
        raise PolyesterResponseContractError(
            "CreateInternalTransfer", "missing request_id or transfer_id"
        )
    return InternalTransferResult(
        request_id=msg.request_id,
        transfer_id=msg.transfer_id,
        asset_id=int(msg.asset_id),
        asset_code=msg.asset_code,
        quantity=AssetAmount.from_scaled(
            _u128_scaled(msg.amount_e18) if msg.HasField("amount_e18") else 0,
            scale=LEDGER_SCALE,
            domain=QuantityDomain.LEDGER_E18,
            asset_id=int(msg.asset_id),
        ),
    )
