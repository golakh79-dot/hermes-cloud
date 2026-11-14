from __future__ import annotations

from polyester.codecs.decode.vip import vip_status_from_proto, vip_tiers_list_from_proto
from polyester.gen.vip.v1.vip_connect import VIPServiceClient
from polyester.gen.vip.v1.vip_pb2 import GetVIPStatusRequest, ListVIPTiersRequest
from polyester.models.vip import VIPStatus, VIPTiersList
from polyester.services._base import BaseService
from polyester.services._generated import unary_auth_decoded, unary_public_decoded


class AsyncVIPService(BaseService):
    async def list_vip_tiers(self) -> VIPTiersList:
        return await unary_public_decoded(
            self._transport,
            VIPServiceClient,
            lambda client, request: client.list_v_i_p_tiers(request),
            ListVIPTiersRequest(),
            vip_tiers_list_from_proto,
        )

    async def get_vip_status(self) -> VIPStatus:
        return await unary_auth_decoded(
            self._transport,
            VIPServiceClient,
            lambda client, request: client.get_v_i_p_status(request),
            GetVIPStatusRequest(),
            vip_status_from_proto,
        )
