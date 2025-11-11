from typing import Protocol


class SessionAdapter(Protocol):
    async def destroy(self) -> None: ...


class DestroySessionUseCase:
    """Use case for destroying user session (logout)."""

    def __init__(self, session_adapter: SessionAdapter):
        self.session_adapter = session_adapter

    async def __call__(self) -> None:
        """Destroy current session."""
        await self.session_adapter.destroy()
