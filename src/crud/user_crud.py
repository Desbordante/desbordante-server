from typing import TypedDict, Unpack

from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.base_crud import BaseCrud
from src.models.user_models import UserModel


class UserFindProps(TypedDict, total=False):
    id: int


class UserUpdateProps(TypedDict, total=False):
    is_banned: bool


class UserCrud(BaseCrud[UserModel]):
    model = UserModel

    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    async def get_by(self, **kwargs: Unpack[UserFindProps]) -> UserModel:  # type: ignore
        return await super().get_by(**kwargs)

    async def update(  # type: ignore
        self, *, entity: UserModel, **kwargs: Unpack[UserUpdateProps]
    ) -> UserModel:
        return await super().update(entity=entity, **kwargs)
