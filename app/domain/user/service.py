from app.domain.user.models import User
from app.domain.user.schemas import UserPublic
from app.repository import BaseRepository


class UserService:
    def __init__(self, repository: BaseRepository[User]):
        self._repository = repository

    def get_by_id(self, id: int) -> UserPublic:
        user = self._repository.get_by_id(id)
        return UserPublic.model_validate(user)
