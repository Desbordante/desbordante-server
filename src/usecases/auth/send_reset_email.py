from typing import Protocol

from src.domain.auth.tasks import send_reset_email
from src.exceptions import ResourceNotFoundException
from src.models.user_models import UserModel


class UserCrud(Protocol):
    async def get_by(self, *, email: str) -> UserModel: ...


class SendResetEmailUseCase:
    def __init__(self, *, user_crud: UserCrud):
        self.user_crud = user_crud

    async def __call__(self, to_email: str) -> None:
        try:
            await self.user_crud.get_by(email=to_email)
        except ResourceNotFoundException:
            raise ResourceNotFoundException(f"User with email {to_email} not found")

        send_reset_email.delay(to_email=to_email)
