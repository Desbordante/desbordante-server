from typing import Protocol


from src.schemas.session_schemas import UserSessionSchema


class SessionPort(Protocol):
    """Port for session management."""

    async def create(self, session: UserSessionSchema) -> None:
        """Create new session for user with regenerated ID."""
        ...

    async def get(self) -> UserSessionSchema | None:
        """Get current user session."""
        ...

    async def destroy(self) -> None:
        """Destroy current session."""
        ...
