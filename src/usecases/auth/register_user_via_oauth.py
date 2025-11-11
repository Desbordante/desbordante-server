from typing import Protocol

from src.exceptions import ResourceAlreadyExistsException
from src.models.user_models import UserModel
from src.schemas.auth_schemas import OAuthCredentialsSchema


class UserCrud(Protocol):
    async def create(self, entity: UserModel) -> UserModel: ...


class RegisterUserViaOAuthUseCase:
    """Use case for registering user via OAuth."""

    def __init__(self, user_crud: UserCrud):
        self.user_crud = user_crud

    async def __call__(self, *, credentials: OAuthCredentialsSchema) -> UserModel:
        user_model = UserModel(
            oauth_provider=credentials.provider,
            oauth_id=credentials.oauth_id,
        )

        try:
            return await self.user_crud.create(entity=user_model)
        except ResourceAlreadyExistsException:
            raise ResourceAlreadyExistsException(
                f"User with OAuth provider '{credentials.provider.value}' and ID '{credentials.oauth_id}' already exists"
            )
