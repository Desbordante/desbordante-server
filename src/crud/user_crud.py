from typing import TypedDict, Unpack

from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.base_crud import BaseCrud
from src.models.user_models import UserModel
from src.schemas.auth_schemas import OAuthProvider


class UserFindProps(TypedDict, total=False):
    id: int
    oauth_provider: OAuthProvider
    oauth_id: str


class UserUpdateProps(TypedDict, total=False):
    is_active: bool


class UserCrud(BaseCrud[UserModel, int]):
    model = UserModel

    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    async def get_by(self, **kwargs: Unpack[UserFindProps]) -> UserModel:  # type: ignore
        return await super().get_by(**kwargs)

    async def update(  # type: ignore
        self, *, entity: UserModel, **kwargs: Unpack[UserUpdateProps]
    ) -> UserModel:
        return await super().update(entity=entity, **kwargs)

    async def update_is_active(self, *, user_id: int, is_active: bool) -> UserModel:
        user = await self.get_by(id=user_id)
        return await self.update(entity=user, is_active=is_active)
