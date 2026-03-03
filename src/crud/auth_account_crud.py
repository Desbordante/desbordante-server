from typing import TypedDict, Unpack

from sqlalchemy import select

from src.crud.base_crud import BaseCrud
from src.models.auth_models import AuthAccountModel
from src.schemas.auth_schemas import AuthProvider


class AuthAccountFindProps(TypedDict, total=False):
    provider: AuthProvider
    account_id: str
    owner_id: int


class AuthAccountCrud(BaseCrud[AuthAccountModel]):
    model = AuthAccountModel

    async def get_by(self, **kwargs: Unpack[AuthAccountFindProps]) -> AuthAccountModel:
        return await super().get_by(**kwargs)

    async def get_all_by_owner(self, owner_id: int) -> list[AuthAccountModel]:
        result = await self._session.execute(
            select(AuthAccountModel).where(AuthAccountModel.owner_id == owner_id)
        )
        return list(result.scalars().all())
