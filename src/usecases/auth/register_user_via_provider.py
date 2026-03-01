from typing import Protocol

from src.models.auth_models import AuthAccountModel
from src.models.user_models import UserModel
from src.schemas.auth_schemas import AuthCredsSchema


class UserCrud(Protocol):
    async def create(self, entity: UserModel) -> UserModel: ...


class RegisterUserViaProviderUseCase:
    """Use case for registering user via auth provider (OAuth/OIDC)."""

    def __init__(self, user_crud: UserCrud):
        self._user_crud = user_crud

    async def __call__(self, *, creds: AuthCredsSchema) -> UserModel:
        user_model = UserModel(
            email=creds.email,
            auth_accounts=[
                AuthAccountModel(
                    provider=creds.provider,
                    account_id=creds.account_id,
                )
            ],
        )

        return await self._user_crud.create(entity=user_model)
