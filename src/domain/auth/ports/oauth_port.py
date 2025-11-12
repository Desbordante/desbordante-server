from typing import Protocol

from fastapi import Request
from fastapi.responses import RedirectResponse

from src.schemas.auth_schemas import OAuthProvider, OAuthUserInfoSchema


class OAuthPort(Protocol):
    """Port for OAuth operations with session management."""

    async def get_authorization_redirect(
        self,
        *,
        provider: OAuthProvider,
        request: Request,
        redirect_uri: str,
    ) -> RedirectResponse:
        """Get OAuth authorization redirect URL."""
        ...

    async def get_user_info(
        self,
        *,
        provider: OAuthProvider,
        request: Request,
    ) -> OAuthUserInfoSchema:
        """Get user info from OAuth callback."""
        ...
