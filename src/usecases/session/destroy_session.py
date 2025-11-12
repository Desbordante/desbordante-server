from typing import Protocol

from fastapi import Request


class SessionManager(Protocol):
    async def destroy(self, request: Request) -> None: ...


class DestroySessionUseCase:
    """Use case for destroying user session (logout)."""

    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager

    async def __call__(self, *, request: Request) -> None:
        """Destroy current session."""
        await self.session_manager.destroy(request)
