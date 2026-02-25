from abc import ABC, abstractmethod

from authlib.integrations.starlette_client import StarletteOAuth2App
from fastapi import Request
from fastapi.responses import RedirectResponse

from src.schemas.auth_schemas import AuthUserInfoSchema


class AuthProviderClient(ABC):
    """Abstract auth provider. Config and userinfo logic are in implementations."""

    _client: StarletteOAuth2App

    async def get_authorization_redirect(
        self, request: Request, redirect_uri: str
    ) -> RedirectResponse:
        return await self._client.authorize_redirect(request, redirect_uri)

    @abstractmethod
    async def get_userinfo(self, request: Request) -> AuthUserInfoSchema: ...
