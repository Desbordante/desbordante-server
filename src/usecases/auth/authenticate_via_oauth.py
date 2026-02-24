from typing import Any, Protocol

from src.schemas.auth_schemas import (
    OAuthCredsSchema,
    OAuthProvider,
    OAuthUserInfoSchema,
)


class OAuthServicePort(Protocol):
    async def get_userinfo(self, provider: OAuthProvider) -> OAuthUserInfoSchema: ...


class GetOrCreateUserViaOAuthPort(Protocol):
    async def __call__(self, *, creds: OAuthCredsSchema) -> Any: ...


class CreateUserSessionPort(Protocol):
    async def __call__(self, *, user: Any) -> str: ...


class AuthenticateViaOAuthUseCase:
    """Use case for OAuth callback: get creds, get/create user, create session."""

    def __init__(
        self,
        *,
        oauth_service: OAuthServicePort,
        get_or_create_user_via_oauth: GetOrCreateUserViaOAuthPort,
        create_session: CreateUserSessionPort,
    ) -> None:
        self._oauth_service = oauth_service
        self._get_or_create_user_via_oauth = get_or_create_user_via_oauth
        self._create_session = create_session

    async def __call__(self, *, provider: OAuthProvider) -> str:
        creds = await self._oauth_service.get_userinfo(provider=provider)

        user = await self._get_or_create_user_via_oauth(creds=creds)

        return await self._create_session(user=user)
