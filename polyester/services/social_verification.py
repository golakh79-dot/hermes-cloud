from __future__ import annotations

from polyester.codecs.decode.common import api_data_from_proto
from polyester.codecs.enums import resolve_proto_enum
from polyester.gen.auth.v1 import social_verification_pb2 as sv_pb2
from polyester.gen.auth.v1.social_verification_connect import SocialVerificationServiceClient
from polyester.models import ApiData
from polyester.services._base import BaseService
from polyester.services._generated import unary_auth_decoded

_PROVIDER_ALIASES = {
    "twitter": sv_pb2.TWITTER,
    "discord": sv_pb2.DISCORD,
}

_METHOD_ALIASES = {
    "profile": sv_pb2.METHOD_PROFILE,
    "channel": sv_pb2.METHOD_CHANNEL,
    "dm": sv_pb2.METHOD_DM,
}


class AsyncSocialVerificationService(BaseService):
    async def start(
        self,
        *,
        provider: str,
        method: str | None = None,
        handle: str | None = None,
    ) -> ApiData:
        request = sv_pb2.StartSocialVerificationRequest(
            provider=resolve_proto_enum(
                sv_pb2, provider, aliases=_PROVIDER_ALIASES, field_name="provider"
            ),
        )
        if method:
            request.method = resolve_proto_enum(
                sv_pb2, method, aliases=_METHOD_ALIASES, field_name="method"
            )
        if handle:
            request.handle = handle
        return await unary_auth_decoded(
            self._transport,
            SocialVerificationServiceClient,
            lambda client, req: client.start_social_verification(req),
            request,
            api_data_from_proto,
        )

    async def mark_ready(self, *, provider: str) -> ApiData:
        request = sv_pb2.SocialVerificationReadyRequest(
            provider=resolve_proto_enum(
                sv_pb2, provider, aliases=_PROVIDER_ALIASES, field_name="provider"
            ),
        )
        return await unary_auth_decoded(
            self._transport,
            SocialVerificationServiceClient,
            lambda client, req: client.social_verification_ready(req),
            request,
            api_data_from_proto,
        )

    async def get(self, *, provider: str) -> ApiData:
        request = sv_pb2.GetSocialVerificationRequest(
            provider=resolve_proto_enum(
                sv_pb2, provider, aliases=_PROVIDER_ALIASES, field_name="provider"
            ),
        )
        return await unary_auth_decoded(
            self._transport,
            SocialVerificationServiceClient,
            lambda client, req: client.get_social_verification(req),
            request,
            api_data_from_proto,
        )
