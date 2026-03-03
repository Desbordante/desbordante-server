from typing import Protocol

from src.exceptions import ResourceNotFoundException
from src.models.auth_models import AuthAccountModel
from src.models.user_models import UserModel
from src.schemas.auth_schemas import AuthCredsSchema, AuthProvider


class RegisterUserViaProviderUseCasePort(Protocol):
    async def __call__(self, *, creds: AuthCredsSchema) -> UserModel: ...


class AuthAccountCrud(Protocol):
    async def get_by(
        self, *, provider: AuthProvider, account_id: str
    ) -> AuthAccountModel: ...


class GetOrCreateUserViaProviderUseCase:
    """Use case for getting or creating user via auth provider. Finds existing user or registers new one."""

    def __init__(
        self,
        *,
        register_user_via_provider: RegisterUserViaProviderUseCasePort,
        auth_account_crud: AuthAccountCrud,
    ):
        self._auth_account_crud = auth_account_crud
        self._register_user_via_provider = register_user_via_provider

    async def __call__(self, *, creds: AuthCredsSchema) -> UserModel:
        try:
            auth_account = await self._auth_account_crud.get_by(
                provider=creds.provider,
                account_id=creds.account_id,
            )
            user = auth_account.owner
        except ResourceNotFoundException:
            user = await self._register_user_via_provider(creds=creds)

        return user
