from __future__ import annotations

ORDERBOOK_SUPPORTED_DEPTHS = (1, 5, 10, 20, 50, 100, 200, 500, 1000)

INTERVAL_ALIASES: dict[str, str] = {
    "1s": "INTERVAL_1S",
    "1m": "INTERVAL_1M",
    "5m": "INTERVAL_5M",
    "1h": "INTERVAL_1H",
}

DEPTH_TO_PROTO: dict[int, str] = {
    1: "DEPTH_1",
    5: "DEPTH_5",
    10: "DEPTH_10",
    20: "DEPTH_20",
    50: "DEPTH_50",
    100: "DEPTH_100",
    200: "DEPTH_200",
    500: "DEPTH_500",
    1000: "DEPTH_1000",
}

QTY_MODE_ALIASES: dict[str, str] = {
    "close": "CLOSE",
    "peak": "PEAK",
}


def depth_to_proto_name(depth: int) -> str:
    if depth in DEPTH_TO_PROTO:
        return DEPTH_TO_PROTO[depth]
    closest = min(ORDERBOOK_SUPPORTED_DEPTHS, key=lambda value: abs(value - depth))
    return DEPTH_TO_PROTO[closest]
