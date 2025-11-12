from typing import Protocol

from src.models.user_models import UserModel
from src.schemas.auth_schemas import OAuthProvider


class GetUserByOAuthUseCasePort(Protocol):
    async def __call__(
        self, *, provider: OAuthProvider, oauth_id: str
    ) -> UserModel | None: ...


class RegisterUserViaOAuthUseCasePort(Protocol):
    async def __call__(
        self, *, provider: OAuthProvider, oauth_id: str
    ) -> UserModel: ...


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

    async def __call__(self, *, provider: OAuthProvider, oauth_id: str) -> UserModel:
        user = await self.get_user_by_oauth(provider=provider, oauth_id=oauth_id)

        if user is None:
            user = await self.register_user_via_oauth(
                provider=provider, oauth_id=oauth_id
            )

        return user
