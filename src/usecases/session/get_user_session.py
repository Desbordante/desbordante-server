from typing import Protocol

from fastapi import Request

from src.exceptions import UnauthorizedException
from src.schemas.session_schemas import SessionSchema


class SessionManager(Protocol):
    async def get(self, request: Request) -> SessionSchema | None: ...


class GetUserSessionUseCase:
    """Use case for getting user session data."""

    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager

    async def __call__(self, *, request: Request) -> SessionSchema:
        """Get user session or raise 401."""
        session = await self.session_manager.get(request)

        if session is None:
            raise UnauthorizedException("Session not found or expired")

        return session
