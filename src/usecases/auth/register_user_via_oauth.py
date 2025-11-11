from typing import Protocol

from src.exceptions import ResourceAlreadyExistsException
from src.models.user_models import UserModel
from src.schemas.auth_schemas import OAuthCredsSchema


class UserCrud(Protocol):
    async def create(self, entity: UserModel) -> UserModel: ...


class RegisterUserViaOAuthUseCase:
    """Use case for registering user via OAuth."""

    def __init__(self, user_crud: UserCrud):
        self.user_crud = user_crud

    async def __call__(self, *, creds: OAuthCredsSchema) -> UserModel:
        user_model = UserModel(
            oauth_provider=creds.provider,
            oauth_id=creds.oauth_id,
        )

        try:
            return await self.user_crud.create(entity=user_model)
        except ResourceAlreadyExistsException:
            raise ResourceAlreadyExistsException(
                f"User with OAuth provider '{creds.provider.value}' and ID '{creds.oauth_id}' already exists"
            )
