from authlib.integrations.starlette_client import StarletteOAuth2App
from fastapi import Request
from fastapi.responses import RedirectResponse

from src.infrastructure.auth.oauth_registry import create_oauth_registry
from src.infrastructure.auth.userinfo_mapper import extract_oauth_id
from src.schemas.auth_schemas import OAuthProvider, OAuthUserInfoSchema


class AuthlibOAuthService:
    """OAuth service using Authlib. Request is bound in constructor."""

    def __init__(self, request: Request) -> None:
        self._request = request
        self._oauth = create_oauth_registry()

    async def get_authorization_redirect(
        self, provider: OAuthProvider, redirect_uri: str
    ) -> RedirectResponse:
        client = self._get_client(provider)
        return await client.authorize_redirect(self._request, redirect_uri)

    async def get_userinfo(self, provider: OAuthProvider) -> OAuthUserInfoSchema:
        client = self._get_client(provider)
        token = await client.authorize_access_token(self._request)
        userinfo = token.get("userinfo")
        if userinfo is None:
            userinfo = await client.userinfo(token=token)
        raw = dict(userinfo) if userinfo else {}
        oauth_id = extract_oauth_id(raw, provider)
        return OAuthUserInfoSchema(provider=provider, oauth_id=oauth_id)

    def _get_client(self, provider: OAuthProvider) -> StarletteOAuth2App:
        client = self._oauth.create_client(provider.value)
        if client is None:
            raise ValueError(f"OAuth provider '{provider.value}' not found")
        return client
