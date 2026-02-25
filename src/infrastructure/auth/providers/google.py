"""Google OIDC provider. Uses standard OIDC userinfo endpoint."""

from typing import Any

from authlib.integrations.starlette_client import OAuth, StarletteOAuth2App
from fastapi import Request

from src.domain.auth.config import settings
from src.infrastructure.auth.providers.base import AuthProviderClient
from src.schemas.auth_schemas import AuthProvider, AuthUserInfoSchema


class GoogleAuthProvider(AuthProviderClient):
    """Google OIDC provider. Uses standard userinfo."""

    _client: StarletteOAuth2App

    def __init__(self, oauth: OAuth) -> None:
        self._client = oauth.register(
            name=AuthProvider.GOOGLE,
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            authorize_url="https://accounts.google.com/o/oauth2/v2/auth",
            access_token_url="https://oauth2.googleapis.com/token",
            userinfo_endpoint="https://www.googleapis.com/oauth2/v2/userinfo",
            server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
            client_kwargs={"scope": "openid email"},
        )  # type: ignore

    async def get_userinfo(self, request: Request) -> AuthUserInfoSchema:
        token = await self._client.authorize_access_token(request)

        userinfo: dict[str, Any] = token["userinfo"]

        return AuthUserInfoSchema(
            account_id=str(userinfo["sub"]),
            email=userinfo["email"],
            is_verified=userinfo["email_verified"],
        )
