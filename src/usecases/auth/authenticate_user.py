from typing import Protocol

from src.domain.auth.exceptions import IncorrectCredentialsException
from src.domain.security.utils import verify_password
from src.exceptions import ResourceNotFoundException
from src.models.user_models import UserModel
from src.schemas.auth_schemas import AuthenticateUserSchema


class UserCrud(Protocol):
    async def get_by(self, *, email: str) -> UserModel: ...


class AuthenticateUserUseCase:
    def __init__(
        self,
        *,
        user_crud: UserCrud,
    ):
        self.user_crud = user_crud

    async def __call__(self, *, data: AuthenticateUserSchema) -> UserModel:
        try:
            user = await self.user_crud.get_by(email=data.email)
        except ResourceNotFoundException:
            raise IncorrectCredentialsException()

        if not verify_password(data.password, user.hashed_password):
            raise IncorrectCredentialsException()

        return user
