from typing import Protocol

from src.domain.security.utils import decode_token, get_password_hash
from src.models.user_models import UserModel
from src.schemas.auth_schemas import ResetPasswordSchema
from src.schemas.email_schemas import ResetPasswordTokenPayloadSchema


class UserCrud(Protocol):
    async def get_by(self, *, email: str) -> UserModel: ...
    async def update(
        self, *, entity: UserModel, hashed_password: str, is_verified: bool
    ) -> UserModel: ...


class ResetPasswordUseCase:
    def __init__(
        self,
        *,
        user_crud: UserCrud,
    ):
        self.user_crud = user_crud

    async def __call__(self, *, token: str, data: ResetPasswordSchema) -> UserModel:
        token_data = decode_token(schema=ResetPasswordTokenPayloadSchema, token=token)

        user = await self.user_crud.get_by(email=token_data.email)

        hashed_password = get_password_hash(data.new_password)

        user = await self.user_crud.update(
            entity=user, hashed_password=hashed_password, is_verified=True
        )

        return user
