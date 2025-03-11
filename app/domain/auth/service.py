from app.domain.user.models import User
from app.domain.user.repository import UserRepository

from .schemas import RegisterUserSchema
from app.domain.user.schemas import UserSchema
from .exceptions import IncorrectCredentialsException
from passlib.context import CryptContext

from app.domain.user.exceptions import UserNotFoundException


class AuthService:
    _pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(self, repository: UserRepository):
        self._repository = repository

    @classmethod
    def _verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return cls._pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def _get_password_hash(cls, password: str) -> str:
        return cls._pwd_context.hash(password)

    async def authenticate_user(self, email: str, password: str) -> UserSchema:
        try:
            user = await self._repository.get_by_email(email)
            if not self._verify_password(password, user.hashed_password):
                raise IncorrectCredentialsException()
            return UserSchema.model_validate(user)
        except UserNotFoundException as e:
            raise IncorrectCredentialsException() from e

    async def register_user(self, data: RegisterUserSchema) -> UserSchema:
        hashed_password = self._get_password_hash(data.password)
        user_model = User(
            email=data.email,
            hashed_password=hashed_password,
            first_name=data.first_name,
            last_name=data.last_name,
        )

        new_user = await self._repository.add_user(user_model)
        return UserSchema.model_validate(new_user)
