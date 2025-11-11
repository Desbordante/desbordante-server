from typing import Protocol

from fastapi import Request

from src.schemas.session_schemas import UserSessionSchema


class SessionManager(Protocol):
    """Manager for session operations."""

    async def create(self, request: Request, session: UserSessionSchema) -> None:
        """Create new session for user with regenerated ID."""
        ...

    async def get(self, request: Request) -> UserSessionSchema | None:
        """Get current user session."""
        ...

    async def destroy(self, request: Request) -> None:
        """Destroy current session."""
        ...

    async def clear_all_user_sessions(self, *, user_id: int) -> int:
        """
        Clear all sessions for a specific user (admin operation).
        Returns the number of sessions deleted.
        """
        ...
