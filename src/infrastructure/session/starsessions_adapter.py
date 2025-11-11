from fastapi import Request
from starsessions import load_session, regenerate_session_id

from src.schemas.session_schemas import UserSessionSchema


class StarsessionsAdapter:
    """Adapter for starsessions library."""

    USER_ID_KEY = "user_id"
    IS_ADMIN_KEY = "is_admin"

    def __init__(self, request: Request):
        self.request = request
        self._session_loaded = False

    async def load(self) -> None:
        """Load session from request."""
        await load_session(self.request)
        self._session_loaded = True

    async def _ensure_session_loaded(self) -> None:
        """Ensure session is loaded only once."""
        if not self._session_loaded:
            await self.load()

    async def create(self, session: UserSessionSchema) -> None:
        """Create new session for user with regenerated ID."""
        await self._ensure_session_loaded()

        regenerate_session_id(self.request)

        self.request.session[self.USER_ID_KEY] = session.id
        self.request.session[self.IS_ADMIN_KEY] = session.is_admin

    async def get(self) -> UserSessionSchema | None:
        """Get current user session."""
        await self._ensure_session_loaded()

        user_id = self.request.session.get(self.USER_ID_KEY)
        is_admin = bool(self.request.session.get(self.IS_ADMIN_KEY))

        if user_id is None:
            return None

        return UserSessionSchema(id=user_id, is_admin=is_admin)

    async def destroy(self) -> None:
        """Destroy current session."""
        await self._ensure_session_loaded()
        self.request.session.clear()
