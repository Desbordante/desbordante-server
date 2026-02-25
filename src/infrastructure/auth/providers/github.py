from typing import Any

from authlib.integrations.starlette_client import OAuth, StarletteOAuth2App
from fastapi import Request

from src.domain.auth.config import settings
from src.infrastructure.auth.providers.base import AuthProviderClient
from src.schemas.auth_schemas import AuthProvider, AuthUserInfoSchema


class GitHubAuthProvider(AuthProviderClient):
    """GitHub auth provider. Fetches user info + primary email"""

    _client: StarletteOAuth2App

    def __init__(self, oauth: OAuth) -> None:
        self._client = oauth.register(
            name=AuthProvider.GITHUB,
            client_id=settings.GITHUB_CLIENT_ID,
            client_secret=settings.GITHUB_CLIENT_SECRET,
            authorize_url="https://github.com/login/oauth/authorize",
            access_token_url="https://github.com/login/oauth/access_token",
            userinfo_endpoint="https://api.github.com/user",
            api_base_url="https://api.github.com/",
            client_kwargs={"scope": "user:email"},
        )  # type: ignore

    async def get_userinfo(self, request: Request) -> AuthUserInfoSchema:
        token = await self._client.authorize_access_token(request)

        userinfo = await self._client.userinfo(token=token)

        resp = await self._client.get("user/emails", token=token)
        resp.raise_for_status()
        emails: list[dict] = resp.json()

        primary_entry: dict[str, Any] | None = next(
            (e for e in emails if e.get("primary")), None
        )

        if primary_entry is None:
            raise ValueError("No primary email found")

        return AuthUserInfoSchema(
            account_id=str(userinfo["id"]),
            email=primary_entry["email"],
            is_verified=primary_entry["verified"],
        )
