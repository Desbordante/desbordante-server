from typing import Protocol

from fastapi import Request

from src.exceptions import ForbiddenException
from src.schemas.session_schemas import UserSessionSchema


class SessionManager(Protocol):
    async def create(self, request: Request, session: UserSessionSchema) -> None: ...


class User(Protocol):
    id: int
    is_admin: bool
    is_active: bool


class CreateUserSessionUseCase:
    """Use case for creating user session after authentication."""

    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager

    async def __call__(self, *, request: Request, user: User) -> None:
        """Create session for authenticated user."""

        if not user.is_active:
            raise ForbiddenException("User is banned")

        session = UserSessionSchema(
            id=user.id,
            is_admin=user.is_admin,
        )

        await self.session_manager.create(request, session)
