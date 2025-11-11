from typing import Protocol

from src.models.user_models import UserModel
from src.schemas.session_schemas import UserSessionSchema


class SessionAdapter(Protocol):
    async def create(self, session: UserSessionSchema) -> None: ...


class CreateUserSessionUseCase:
    """Use case for creating user session after authentication."""

    def __init__(self, session_adapter: SessionAdapter):
        self.session_adapter = session_adapter

    async def __call__(self, *, user: UserModel) -> None:
        """Create session for authenticated user."""
        session = UserSessionSchema(
            user_id=user.id,
            is_admin=user.is_admin,
        )
        await self.session_adapter.create(session)
