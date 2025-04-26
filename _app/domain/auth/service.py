from passlib.context import CryptContext

from _app.domain.user.models import User
from _app.domain.user.schemas import UserPublic
from _app.exceptions import ResourceNotFoundException
from _app.exceptions.exceptions import ResourceAlreadyExistsException
from _app.repository import BaseRepository

from .exceptions import IncorrectCredentialsException
from .schemas import UserLogin, UserRegister


class AuthService:
    _pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(self, repository: BaseRepository[User]):
        self._repository = repository

    @classmethod
    def _verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return cls._pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def _get_password_hash(cls, password: str) -> str:
        return cls._pwd_context.hash(password)

    def authenticate_user(self, data: UserLogin) -> UserPublic:
        try:
            user = self._repository.get_by(field="email", value=data.email)
            if not self._verify_password(data.password, user.hashed_password):
                raise IncorrectCredentialsException()
            return UserPublic.model_validate(user)
        except ResourceNotFoundException as e:
            raise IncorrectCredentialsException() from e

    def register_user(self, data: UserRegister) -> UserPublic:
        hashed_password = self._get_password_hash(data.password)

        user_model = User.model_validate(
            data,
            update={"hashed_password": hashed_password},
        )

        try:
            new_user = self._repository.create(user_model)
            return UserPublic.model_validate(new_user)

        except ResourceAlreadyExistsException as e:
            raise ResourceAlreadyExistsException(
                f"User with email {data.email} already exists"
            ) from e

    def get_by_id(self, id: int) -> User:
        user = self._repository.get_by_id(id)
        return user
