from typing import Protocol

from authlib.integrations.starlette_client import StarletteOAuth2App
from fastapi import Request
from fastapi.responses import RedirectResponse

from src.schemas.auth_schemas import OAuthProvider


class OAuthClientFactory(Protocol):
    def create(self, provider: OAuthProvider) -> StarletteOAuth2App: ...


class GetOAuthAuthorizationRedirectUseCase:
    """Use case for getting OAuth authorization redirect URL."""

    def __init__(self, oauth_factory: OAuthClientFactory):
        self.oauth_factory = oauth_factory

    async def __call__(
        self, *, provider: OAuthProvider, request: Request, redirect_uri: str
    ) -> RedirectResponse:
        client = self.oauth_factory.create(provider)
        return await client.authorize_redirect(request, redirect_uri)
