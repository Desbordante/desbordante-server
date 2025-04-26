from typing import TypedDict, Unpack

from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.base_crud import BaseCrud
from src.models.user_models import UserModel


class UserFindProps(TypedDict, total=False):
    email: str
    id: int


class UserCrud(BaseCrud[UserModel, int]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=UserModel, session=session)

    async def get_by(self, **kwargs: Unpack[UserFindProps]) -> UserModel:
        return await super().get_by(**kwargs)
