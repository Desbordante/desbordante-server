from typing import Protocol

from src.domain.security.utils import decode_token
from src.exceptions import ForbiddenException
from src.models.user_models import UserModel
from src.schemas.account_schemas import ConfirmationTokenPayloadSchema


class UserCrud(Protocol):
    async def get_by(self, *, email: str) -> UserModel: ...
    async def update(self, *, entity: UserModel, is_verified: bool) -> UserModel: ...


class ConfirmEmailUseCase:
    def __init__(
        self,
        *,
        user_crud: UserCrud,
    ):
        self.user_crud = user_crud

    async def __call__(self, *, token: str) -> UserModel:
        token_data = decode_token(schema=ConfirmationTokenPayloadSchema, token=token)

        user = await self.user_crud.get_by(email=token_data.email)

        if user.is_verified:
            raise ForbiddenException("User is already verified")

        user = await self.user_crud.update(entity=user, is_verified=True)

        return user
