"""Centrifugo v2 binary protobuf client-protocol framing."""

from __future__ import annotations

from dataclasses import dataclass

from polyester.errors import PolyesterRealtimeError


@dataclass(frozen=True)
class ProtocolError:
    code: int
    message: str
    temporary: bool


@dataclass(frozen=True)
class Reply:
    id: int
    error: ProtocolError | None


@dataclass(frozen=True)
class Publication:
    data: bytes


@dataclass(frozen=True)
class Ping:
    pass


Incoming = Reply | Publication | Ping


def connect_command(command_id: int, token: str | None = None) -> bytes:
    request = _string_field(1, token) if token else b""
    return _command(command_id, 4, request)


def subscribe_command(command_id: int, channel: str, token: str | None = None) -> bytes:
    request = _string_field(1, channel)
    if token:
        request += _string_field(2, token)
    return _command(command_id, 5, request)


def pong_command() -> bytes:
    return b"\x00"


def _command(command_id: int, field: int, request: bytes) -> bytes:
    message = _varint_field(1, command_id) + _bytes_field(field, request)
    return _varint(len(message)) + message


def decode_replies(frame: bytes) -> list[Incoming]:
    cursor = _Cursor(frame)
    incoming: list[Incoming] = []
    while cursor.remaining:
        _decode_reply(cursor.take(cursor.varint()), incoming)
    return incoming


def _decode_reply(data: bytes, incoming: list[Incoming]) -> None:
    if not data:
        incoming.append(Ping())
        return
    cursor = _Cursor(data)
    reply_id = 0
    error: ProtocolError | None = None
    saw_push = False
    while cursor.remaining:
        field, wire = cursor.key()
        if (field, wire) == (1, 0):
            reply_id = cursor.varint()
        elif (field, wire) == (2, 2):
            error = _decode_error(cursor.length_delimited())
        elif (field, wire) == (4, 2):
            saw_push = True
            _decode_push(cursor.length_delimited(), incoming)
        else:
            cursor.skip(wire)
    if reply_id or error is not None or not saw_push:
        incoming.append(Reply(reply_id, error))


def _decode_error(data: bytes) -> ProtocolError:
    cursor = _Cursor(data)
    code = 0
    message = ""
    temporary = False
    while cursor.remaining:
        field, wire = cursor.key()
        if (field, wire) == (1, 0):
            code = cursor.varint()
        elif (field, wire) == (2, 2):
            try:
                message = cursor.length_delimited().decode()
            except UnicodeDecodeError as exc:
                raise PolyesterRealtimeError("invalid Centrifugo error UTF-8") from exc
        elif (field, wire) == (3, 0):
            temporary = bool(cursor.varint())
        else:
            cursor.skip(wire)
    return ProtocolError(code, message, temporary)


def _decode_push(data: bytes, incoming: list[Incoming]) -> None:
    cursor = _Cursor(data)
    while cursor.remaining:
        field, wire = cursor.key()
        if (field, wire) == (4, 2):
            _decode_publication(cursor.length_delimited(), incoming)
        else:
            cursor.skip(wire)


def _decode_publication(data: bytes, incoming: list[Incoming]) -> None:
    cursor = _Cursor(data)
    while cursor.remaining:
        field, wire = cursor.key()
        if (field, wire) == (4, 2):
            incoming.append(Publication(cursor.length_delimited()))
        else:
            cursor.skip(wire)


def _varint_field(field: int, value: int) -> bytes:
    return _varint((field << 3) | 0) + _varint(value)


def _string_field(field: int, value: str) -> bytes:
    return _bytes_field(field, value.encode())


def _bytes_field(field: int, value: bytes) -> bytes:
    return _varint((field << 3) | 2) + _varint(len(value)) + value


def _varint(value: int) -> bytes:
    if value < 0:
        raise PolyesterRealtimeError("negative Centrifugo protobuf varint")
    encoded = bytearray()
    while value >= 0x80:
        encoded.append((value & 0x7F) | 0x80)
        value >>= 7
    encoded.append(value)
    return bytes(encoded)


class _Cursor:
    def __init__(self, data: bytes) -> None:
        self._data = data
        self._offset = 0

    @property
    def remaining(self) -> int:
        return len(self._data) - self._offset

    def varint(self) -> int:
        value = 0
        for shift in range(0, 70, 7):
            if not self.remaining:
                raise PolyesterRealtimeError("truncated Centrifugo protobuf")
            byte = self._data[self._offset]
            self._offset += 1
            if shift == 63 and byte > 1:
                raise PolyesterRealtimeError("Centrifugo protobuf varint overflow")
            value |= (byte & 0x7F) << shift
            if not byte & 0x80:
                return value
        raise PolyesterRealtimeError("Centrifugo protobuf varint overflow")

    def key(self) -> tuple[int, int]:
        key = self.varint()
        field = key >> 3
        if not field:
            raise PolyesterRealtimeError("Centrifugo protobuf field number is zero")
        return field, key & 0x07

    def take(self, length: int) -> bytes:
        end = self._offset + length
        if end > len(self._data):
            raise PolyesterRealtimeError("truncated Centrifugo protobuf")
        value = self._data[self._offset : end]
        self._offset = end
        return value

    def length_delimited(self) -> bytes:
        return self.take(self.varint())

    def skip(self, wire: int) -> None:
        if wire == 0:
            self.varint()
        elif wire == 1:
            self.take(8)
        elif wire == 2:
            self.length_delimited()
        elif wire == 5:
            self.take(4)
        else:
            raise PolyesterRealtimeError(f"unsupported Centrifugo protobuf wire type {wire}")
