from typing import Protocol

from src.models.user_models import UserModel
from src.schemas.account_schemas import UpdateUserInfoSchema


class UserCrud(Protocol):
    async def update(self, *, entity: UserModel, hashed_password: str) -> UserModel: ...


class UpdateInfoUseCase:
    def __init__(
        self,
        *,
        user_crud: UserCrud,
        user: UserModel,
    ):
        self.user_crud = user_crud
        self.user = user

    async def __call__(self, *, data: UpdateUserInfoSchema) -> UserModel:
        user = await self.user_crud.update(
            entity=self.user,
            **data.model_dump(exclude_none=True),
        )

        return user
