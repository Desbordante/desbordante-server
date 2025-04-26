from typing import Protocol

from src.domain.auth.constants import pwd_context
from src.exceptions import ResourceAlreadyExistsException
from src.models.user_models import UserModel
from src.schemas.auth_schemas import RegisterUserSchema


class UserCrud(Protocol):
    async def create(self, entity: UserModel) -> UserModel: ...


class RegisterUserUseCase:
    def __init__(
        self,
        *,
        user_crud: UserCrud,
    ):
        self.user_crud = user_crud

    def _get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    async def __call__(self, *, data: RegisterUserSchema) -> UserModel:
        hashed_password = self._get_password_hash(data.password)

        user_model = UserModel(
            email=data.email,
            full_name=data.full_name,
            hashed_password=hashed_password,
            country=data.country,
            company=data.company,
            occupation=data.occupation,
        )

        try:
            return await self.user_crud.create(entity=user_model)
        except ResourceAlreadyExistsException:
            raise ResourceAlreadyExistsException(
                f"User with email {data.email} already exists"
            )
