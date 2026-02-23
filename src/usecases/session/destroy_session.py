from typing import Protocol


class SessionManager(Protocol):
    async def destroy(self, *, session_id: str) -> None: ...


class DestroySessionUseCase:
    """Use case for destroying user session (logout)."""

    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager

    async def __call__(self, *, session_id: str) -> None:
        """Destroy session by session id."""
        await self.session_manager.destroy(session_id=session_id)
