from typing import Protocol

from fastapi import Request
from fastapi.responses import RedirectResponse

from src.schemas.auth_schemas import OAuthProvider, OAuthUserInfoSchema


class OAuthPort(Protocol):
    """Port for OAuth operations."""

    async def get_authorization_redirect(
        self, *, provider: OAuthProvider, request: Request, redirect_uri: str
    ) -> RedirectResponse: ...

    async def get_user_info(
        self, *, provider: OAuthProvider, request: Request
    ) -> OAuthUserInfoSchema: ...


class GetOAuthAuthorizationRedirectUseCase:
    """Use case for getting OAuth authorization redirect URL."""

    def __init__(self, oauth_adapter: OAuthPort):
        self.oauth_adapter = oauth_adapter

    async def __call__(
        self, *, provider: OAuthProvider, request: Request, redirect_uri: str
    ) -> RedirectResponse:
        return await self.oauth_adapter.get_authorization_redirect(
            provider=provider, request=request, redirect_uri=redirect_uri
        )
