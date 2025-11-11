from typing import Protocol

from authlib.integrations.starlette_client import StarletteOAuth2App
from fastapi import Request
from fastapi.responses import RedirectResponse

from src.schemas.auth_schemas import OAuthProvider


class OAuthClientFactory(Protocol):
    """Port for OAuth client factory."""

    def create(self, provider: OAuthProvider) -> StarletteOAuth2App: ...


class GetOAuthAuthorizationRedirectUseCase:
    """Use case for getting OAuth authorization redirect URL."""

    def __init__(self, client_factory: OAuthClientFactory):
        self.client_factory = client_factory

    async def __call__(
        self, *, provider: OAuthProvider, request: Request, redirect_uri: str
    ) -> RedirectResponse:
        client = self.client_factory.create(provider)
        return await client.authorize_redirect(request, redirect_uri)
