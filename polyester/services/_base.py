from __future__ import annotations

from polyester.transport import TransportFactory


class BaseService:
    def __init__(self, transport: TransportFactory) -> None:
        self._transport = transport
