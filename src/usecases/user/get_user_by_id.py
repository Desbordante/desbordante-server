from typing import Protocol

from src.models.user_models import UserModel


class UserCrud(Protocol):
    async def get_by(self, *, id: int) -> UserModel: ...


class GetUserByIdUseCase:
    def __init__(
        self,
        *,
        user_crud: UserCrud,
    ):
        self.user_crud = user_crud

    async def __call__(self, *, id: int) -> UserModel:
        user = await self.user_crud.get_by(id=id)
        return user
