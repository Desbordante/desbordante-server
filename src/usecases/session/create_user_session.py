from typing import Protocol


from src.exceptions import ForbiddenException


class SessionManager(Protocol):
    async def create(self, *, user_id: int, is_admin: bool) -> str: ...


class User(Protocol):
    id: int
    is_admin: bool
    is_banned: bool


class CreateUserSessionUseCase:
    """Use case for creating user session after authentication."""

    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager

    async def __call__(self, *, user: User) -> None:
        """Create session for authenticated user."""

        if user.is_banned:
            raise ForbiddenException("User is banned")

        await self.session_manager.create(user_id=user.id, is_admin=user.is_admin)
