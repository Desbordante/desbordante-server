from app.domain.user.repository import UserRepository
from app.domain.user.schemas import UserSchema


class UserService:
    def __init__(self, repository: UserRepository):
        self._repository = repository

    async def get_by_email(self, email: str) -> UserSchema:
        user = await self._repository.get_by_email(email)
        return UserSchema.model_validate(user)

    async def get_by_id(self, id: int) -> UserSchema:
        user = await self._repository.get_by_id(id)
        return UserSchema.model_validate(user)
