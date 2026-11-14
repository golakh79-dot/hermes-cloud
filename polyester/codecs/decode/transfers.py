from __future__ import annotations

from polyester.codecs.decode.balances import u128_from_proto
from polyester.codecs.proto_helpers import format_uint64_id
from polyester.gen.ledger.read.v1 import ledger_read_pb2
from polyester.models import LedgerTransfer, TransferSide, TransfersList

_TRANSFER_SIDE_KIND_LABELS = {
    ledger_read_pb2.FUNDING_ACCOUNT: "funding_account",
    ledger_read_pb2.TRADING_ACCOUNT: "trading_account",
    ledger_read_pb2.EXTERNAL_ADDRESS: "external_address",
    ledger_read_pb2.PRIVATE_COUNTERPARTY: "private_counterparty",
    ledger_read_pb2.FEE_ACCOUNT: "fee_account",
    ledger_read_pb2.SYSTEM_ACCOUNT: "system_account",
}


def transfer_side_from_proto(msg: ledger_read_pb2.TransferSide | None) -> TransferSide | None:
    if msg is None or not msg.ByteSize():
        return None
    kind = _TRANSFER_SIDE_KIND_LABELS.get(msg.kind, "")
    account_id = format_uint64_id(msg.account_id) if msg.HasField("account_id") else ""
    chain_id = int(msg.chain_id) if msg.HasField("chain_id") else None
    if not kind and not account_id and not msg.address and chain_id is None:
        return None
    return TransferSide(
        kind=kind,
        account_id=account_id,
        address=msg.address,
        chain_id=chain_id,
    )


def ledger_transfer_from_proto(msg: ledger_read_pb2.TransferRow) -> LedgerTransfer:
    return LedgerTransfer(
        asset_id=int(msg.asset_id),
        amount=u128_from_proto(msg.amount_e18),
        transfer_type=int(msg.transfer_code),
        account_code=int(msg.account_code),
        timestamp=int(msg.ts_us),
        pending=False,
        tx_id=msg.flow_id,
        is_debit=bool(msg.is_debit),
        source=transfer_side_from_proto(msg.source if msg.HasField("source") else None),
        destination=transfer_side_from_proto(
            msg.destination if msg.HasField("destination") else None
        ),
        transfer_id=msg.transfer_id,
    )


def transfers_list_from_proto(msg: ledger_read_pb2.ListTransfersResponse) -> TransfersList:
    transfers = [ledger_transfer_from_proto(item) for item in msg.transfers]
    next_cursor: int | None = None
    if msg.next_page_token:
        try:
            parsed = int(msg.next_page_token)
            if parsed != 0:
                next_cursor = parsed
        except ValueError:
            next_cursor = None
    return TransfersList(transfers=transfers, next_cursor=next_cursor)
