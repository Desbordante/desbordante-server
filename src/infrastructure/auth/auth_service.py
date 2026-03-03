from authlib.integrations.starlette_client import OAuth
from fastapi import Request
from fastapi.responses import RedirectResponse

from src.infrastructure.auth.providers.base import AuthProviderClient
from src.infrastructure.auth.providers.github import GitHubAuthProvider
from src.infrastructure.auth.providers.google import GoogleAuthProvider
from src.schemas.auth_schemas import AuthProvider, AuthUserInfoSchema


class AuthService:
    """Auth service. Holds list of providers and delegates to the right one."""

    _providers: dict[AuthProvider, AuthProviderClient]
    _request: Request

    def __init__(self, request: Request) -> None:
        self._request = request

        oauth = OAuth()

        self._providers = {
            AuthProvider.GITHUB: GitHubAuthProvider(oauth),
            AuthProvider.GOOGLE: GoogleAuthProvider(oauth),
        }

    async def get_authorization_redirect(
        self, provider: AuthProvider, redirect_uri: str
    ) -> RedirectResponse:
        return await self._providers[provider].get_authorization_redirect(
            self._request, redirect_uri
        )

    async def get_userinfo(self, provider: AuthProvider) -> AuthUserInfoSchema:
        return await self._providers[provider].get_userinfo(self._request)
