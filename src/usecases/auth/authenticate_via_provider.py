from typing import Any, Protocol

from src.exceptions import ForbiddenException
from src.schemas.auth_schemas import (
    AuthCredsSchema,
    AuthProvider,
    AuthUserInfoSchema,
)


class AuthServicePort(Protocol):
    async def get_userinfo(self, provider: AuthProvider) -> AuthUserInfoSchema: ...


class GetOrCreateUserViaProviderPort(Protocol):
    async def __call__(self, *, creds: AuthCredsSchema) -> Any: ...


class CreateUserSessionPort(Protocol):
    async def __call__(self, *, user: Any) -> str: ...


class AuthenticateViaProviderUseCase:
    """Use case for auth provider callback: get creds, get/create user, create session."""

    def __init__(
        self,
        *,
        auth_service: AuthServicePort,
        get_or_create_user_via_provider: GetOrCreateUserViaProviderPort,
        create_session: CreateUserSessionPort,
    ) -> None:
        self._auth_service = auth_service
        self._get_or_create_user_via_provider = get_or_create_user_via_provider
        self._create_session = create_session

    async def __call__(self, *, provider: AuthProvider) -> str:
        user_info = await self._auth_service.get_userinfo(provider=provider)

        if not user_info.is_verified:
            raise ForbiddenException("User email is not verified")

        user = await self._get_or_create_user_via_provider(
            creds=AuthCredsSchema(
                provider=provider,
                account_id=user_info.account_id,
                email=user_info.email,
            )
        )

        return await self._create_session(user=user)
