from polyester.codecs.scalars import (
    MAX_PROTOCOL_SCALE,
    align_price_ticks,
    datetime_to_timestamp_dict,
    format_id,
    format_price_ticks,
    format_qty_scaled,
    id_to_int,
    omit_none,
    parse_price_ticks,
    parse_qty_scaled,
    parse_required_uint64_decimal,
    timestamp_dict_to_datetime,
    validate_protocol_scale,
)

__all__ = [
    "MAX_PROTOCOL_SCALE",
    "align_price_ticks",
    "datetime_to_timestamp_dict",
    "format_id",
    "format_price_ticks",
    "format_qty_scaled",
    "id_to_int",
    "omit_none",
    "parse_price_ticks",
    "parse_qty_scaled",
    "parse_required_uint64_decimal",
    "timestamp_dict_to_datetime",
    "validate_protocol_scale",
]


def __getattr__(name: str):
    if name in {"create_order_to_wire", "normalize_create_order_request"}:
        from polyester.codecs.orders import create_order_to_wire, normalize_create_order_request

        exports = {
            "create_order_to_wire": create_order_to_wire,
            "normalize_create_order_request": normalize_create_order_request,
        }
        return exports[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
