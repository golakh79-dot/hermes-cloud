from __future__ import annotations

from polyester.codecs.decode.common import api_data_from_proto
from polyester.gen.marketdata.v1 import heatmap_pb2
from polyester.models import ApiData


def heatmap_from_proto(msg: heatmap_pb2.GetOrderbookHeatmapResponse) -> ApiData:
    return api_data_from_proto(msg)
