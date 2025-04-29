from typing import Protocol

from src.domain.security.utils import get_password_hash, verify_password
from src.exceptions import ForbiddenException
from src.models.user_models import UserModel
from src.schemas.account_schemas import ChangePasswordSchema


class UserCrud(Protocol):
    async def update(self, *, entity: UserModel, hashed_password: str) -> UserModel: ...


class ChangePasswordUseCase:
    def __init__(
        self,
        *,
        user_crud: UserCrud,
        user: UserModel,
    ):
        self.user_crud = user_crud
        self.user = user

    async def __call__(self, *, data: ChangePasswordSchema) -> UserModel:
        if not verify_password(data.current_password, self.user.hashed_password):
            raise ForbiddenException("Incorrect current password")

        hashed_password = get_password_hash(data.new_password)

        user = await self.user_crud.update(
            entity=self.user, hashed_password=hashed_password
        )

        return user
