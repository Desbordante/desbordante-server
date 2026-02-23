from typing import Protocol


from src.exceptions import UnauthorizedException
from src.schemas.session_schemas import SessionSchema


class SessionManager(Protocol):
    async def get(self, *, session_id: str) -> SessionSchema | None: ...


class GetUserSessionUseCase:
    """Use case for getting user session data."""

    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager

    async def __call__(self, *, session_id: str | None) -> SessionSchema:
        """Get user session or raise 401."""

        if session_id is None:
            raise UnauthorizedException("Session not found or expired")

        session = await self.session_manager.get(session_id=session_id)

        if session is None:
            raise UnauthorizedException("Session not found or expired")

        return session
