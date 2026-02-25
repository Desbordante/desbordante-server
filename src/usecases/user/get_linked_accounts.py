from typing import Protocol

from src.models.auth_models import AuthAccountModel


class AuthAccountCrud(Protocol):
    async def get_all_by_owner(self, owner_id: int) -> list[AuthAccountModel]: ...


class User(Protocol):
    id: int


class GetLinkedAccountsUseCase:
    def __init__(
        self,
        *,
        auth_account_crud: AuthAccountCrud,
        user: User,
    ):
        self.auth_account_crud = auth_account_crud
        self.user = user

    async def __call__(self) -> list[AuthAccountModel]:
        accounts = await self.auth_account_crud.get_all_by_owner(owner_id=self.user.id)

        return accounts
