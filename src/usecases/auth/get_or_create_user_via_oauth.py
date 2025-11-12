from typing import Protocol

from src.exceptions import ResourceNotFoundException
from src.models.user_models import UserModel
from src.schemas.auth_schemas import OAuthCredsSchema


class GetUserByOAuthUseCasePort(Protocol):
    async def __call__(self, *, creds: OAuthCredsSchema) -> UserModel: ...


class RegisterUserViaOAuthUseCasePort(Protocol):
    async def __call__(self, *, creds: OAuthCredsSchema) -> UserModel: ...


class GetOrCreateUserViaOAuthUseCase:
    """Use case for getting or creating user via OAuth. Finds existing user or registers new one."""

    def __init__(
        self,
        *,
        get_user_by_oauth: GetUserByOAuthUseCasePort,
        register_user_via_oauth: RegisterUserViaOAuthUseCasePort,
    ):
        self.get_user_by_oauth = get_user_by_oauth
        self.register_user_via_oauth = register_user_via_oauth

    async def __call__(self, *, creds: OAuthCredsSchema) -> UserModel:
        try:
            user = await self.get_user_by_oauth(creds=creds)
        except ResourceNotFoundException:
            user = await self.register_user_via_oauth(creds=creds)

        return user
