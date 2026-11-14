from __future__ import annotations

from polyester._wire import protobuf_to_public_dict
from polyester.models import ApiData


def api_data_from_proto(msg) -> ApiData:
    return ApiData(raw=protobuf_to_public_dict(msg))
