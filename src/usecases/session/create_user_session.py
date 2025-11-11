from typing import Protocol

from fastapi import Request

from src.models.user_models import UserModel
from src.schemas.session_schemas import UserSessionSchema


class SessionManager(Protocol):
    async def create(self, request: Request, session: UserSessionSchema) -> None: ...


class CreateUserSessionUseCase:
    """Use case for creating user session after authentication."""

    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager

    async def __call__(self, *, request: Request, user: UserModel) -> None:
        """Create session for authenticated user."""
        session = UserSessionSchema(
            user_id=user.id,
            is_admin=user.is_admin,
        )
        await self.session_manager.create(request, session)
