from typing import Protocol

from src.exceptions import UnauthorizedException
from src.schemas.session_schemas import UserSessionSchema


class SessionAdapter(Protocol):
    async def get(self) -> UserSessionSchema | None: ...


class GetUserSessionUseCase:
    """Use case for getting user session data."""

    def __init__(self, session_adapter: SessionAdapter):
        self.session_adapter = session_adapter

    async def __call__(self) -> UserSessionSchema:
        """Get user session or raise 401."""
        session = await self.session_adapter.get()

        if session is None:
            raise UnauthorizedException("Session not found or expired")

        return session
