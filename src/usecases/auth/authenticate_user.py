from typing import Protocol

from src.domain.auth.constants import pwd_context
from src.domain.auth.exceptions import IncorrectCredentialsException
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

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    async def __call__(self, *, data: AuthenticateUserSchema) -> UserModel:
        try:
            user = await self.user_crud.get_by(email=data.email)
            if not self._verify_password(data.password, user.hashed_password):
                raise IncorrectCredentialsException()

            return user
        except ResourceNotFoundException:
            raise IncorrectCredentialsException()
