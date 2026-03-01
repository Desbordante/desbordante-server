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
        self._user_crud = user_crud

    async def __call__(self, *, user_id: int) -> UserModel:
        user = await self._user_crud.get_by(id=user_id)

        return user
