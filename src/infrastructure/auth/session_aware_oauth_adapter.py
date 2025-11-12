from fastapi import Request
from fastapi.responses import RedirectResponse

from src.domain.auth.factory import OAuthClientFactory
from src.domain.auth.utils import extract_oauth_id
from src.domain.session.manager import SessionManager
from src.schemas.auth_schemas import OAuthProvider, OAuthUserInfoSchema


class SessionAwareOAuthAdapter:
    """OAuth adapter that ensures session is loaded before operations."""

    def __init__(
        self,
        oauth_factory: OAuthClientFactory,
        session_manager: SessionManager,
    ):
        self.oauth_factory = oauth_factory
        self.session_manager = session_manager

    async def get_authorization_redirect(
        self,
        *,
        provider: OAuthProvider,
        request: Request,
        redirect_uri: str,
    ) -> RedirectResponse:
        """Get OAuth authorization redirect URL (session loaded automatically)."""
        await self.session_manager.get(request)
        client = self.oauth_factory.create(provider)
        return await client.authorize_redirect(request, redirect_uri)

    async def get_user_info(
        self,
        *,
        provider: OAuthProvider,
        request: Request,
    ) -> OAuthUserInfoSchema:
        """Get user info from OAuth callback (session loaded automatically)."""
        await self.session_manager.get(request)
        client = self.oauth_factory.create(provider)
        token = await client.authorize_access_token(request)

        userinfo = token.get("userinfo")
        if userinfo is None:
            userinfo = await client.userinfo(token=token)

        oauth_id = extract_oauth_id(userinfo, provider)
        return OAuthUserInfoSchema(id=oauth_id)
