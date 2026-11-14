ORDERBOOK_SUPPORTED_DEPTHS = (1, 5, 10, 20, 50, 100, 200, 500, 1000)

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


def depth_to_connect_enum(depth: int) -> str:
    if depth in DEPTH_TO_PROTO:
        return DEPTH_TO_PROTO[depth]
    closest = min(ORDERBOOK_SUPPORTED_DEPTHS, key=lambda value: abs(value - depth))
    return DEPTH_TO_PROTO[closest]
