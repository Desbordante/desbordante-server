from typing import Protocol

from authlib.integrations.starlette_client import StarletteOAuth2App
from fastapi import Request

from src.domain.auth.utils import extract_oauth_id
from src.schemas.auth_schemas import OAuthProvider, OAuthUserInfoSchema


class OAuthClientFactory(Protocol):
    """Port for OAuth client factory."""

    def create(self, provider: OAuthProvider) -> StarletteOAuth2App: ...


class GetOAuthUserInfoUseCase:
    """Use case for getting OAuth user info from callback."""

    def __init__(self, client_factory: OAuthClientFactory):
        self.client_factory = client_factory

    async def __call__(
        self, *, provider: OAuthProvider, request: Request
    ) -> OAuthUserInfoSchema:
        client = self.client_factory.create(provider)
        token = await client.authorize_access_token(request)

        # Try to get userinfo from token, otherwise make a request
        userinfo = token.get("userinfo")
        if userinfo is None:
            userinfo = await client.userinfo(token=token)

        oauth_id = extract_oauth_id(userinfo, provider)

        return OAuthUserInfoSchema(id=oauth_id)
