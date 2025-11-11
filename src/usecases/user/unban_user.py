from typing import Protocol

from src.models.user_models import UserModel


class UserCrud(Protocol):
    async def update_is_active(self, *, user_id: int, is_active: bool) -> UserModel: ...


class UnbanUserUseCase:
    def __init__(
        self,
        *,
        user_crud: UserCrud,
    ):
        self.user_crud = user_crud

    async def __call__(self, *, user_id: int) -> UserModel:
        user = await self.user_crud.update_is_active(user_id=user_id, is_active=True)
        return user
