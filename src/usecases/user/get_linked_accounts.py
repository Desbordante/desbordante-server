from typing import Protocol

from src.domain.authorization.entities import AuthenticatedActor
from src.models.auth_models import AuthAccountModel


class AuthAccountCrud(Protocol):
    async def get_all_by_owner(self, owner_id: int) -> list[AuthAccountModel]: ...


class GetLinkedAccountsUseCase:
    def __init__(
        self,
        *,
        auth_account_crud: AuthAccountCrud,
    ):
        self._auth_account_crud = auth_account_crud

    async def __call__(self, *, actor: AuthenticatedActor) -> list[AuthAccountModel]:
        accounts = await self._auth_account_crud.get_all_by_owner(
            owner_id=actor.user_id
        )

        return accounts
