from typing import Any, Protocol

from authlib.integrations.starlette_client import StarletteOAuth2App
from fastapi import Request

from src.schemas.auth_schemas import OAuthProvider


class OAuthClientFactory(Protocol):
    """Port for OAuth client factory."""

    def create(self, provider: OAuthProvider) -> StarletteOAuth2App: ...


class OAuthCallbackUseCase:
    """Use case for handling OAuth callback."""

    def __init__(self, client_factory: OAuthClientFactory):
        self.client_factory = client_factory

    async def __call__(
        self, *, provider: OAuthProvider, request: Request
    ) -> dict[str, Any]:
        client = self.client_factory.create(provider)
        token = await client.authorize_access_token(request)

        # Try to get userinfo from token, otherwise make a request
        user = token.get("userinfo")
        if user is None:
            user = await client.userinfo(token=token)

        return user
