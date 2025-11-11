from typing import Protocol

from src.models.user_models import UserModel
from src.schemas.auth_schemas import OAuthCredsSchema, OAuthProvider


class UserCrud(Protocol):
    async def get_by(
        self, *, oauth_provider: OAuthProvider, oauth_id: str
    ) -> UserModel: ...


class GetUserByOAuthUseCase:
    """Use case for getting user by OAuth credentials."""

    def __init__(self, user_crud: UserCrud):
        self.user_crud = user_crud

    async def __call__(self, *, creds: OAuthCredsSchema) -> UserModel:
        return await self.user_crud.get_by(
            oauth_provider=creds.provider, oauth_id=creds.oauth_id
        )
