from fastapi import Request
from redis.asyncio import Redis
from starsessions import load_session, regenerate_session_id
from starsessions.stores.redis import RedisStore

from src.domain.session.config import settings
from src.infrastructure.redis.client import client
from src.schemas.session_schemas import UserSessionSchema


class SessionManager:
    """Session manager for user session operations."""

    USER_ID_KEY = "user_id"
    IS_ADMIN_KEY = "is_admin"

    def __init__(self, redis_client: Redis):
        self.redis_store = RedisStore(
            connection=redis_client,
            prefix=settings.PREFIX,
        )
        self.redis_client = redis_client

    def get_store(self) -> RedisStore:
        """Get underlying RedisStore for middleware."""
        return self.redis_store

    async def _ensure_session_loaded(self, request: Request) -> None:
        """Ensure session is loaded from request."""
        if not hasattr(request.state, "_session_loaded"):
            await load_session(request)
            request.state._session_loaded = True

    async def create(self, request: Request, session: UserSessionSchema) -> None:
        """Create new session for user with regenerated ID."""
        await self._ensure_session_loaded(request)
        regenerate_session_id(request)
        request.session[self.USER_ID_KEY] = session.id
        request.session[self.IS_ADMIN_KEY] = session.is_admin

    async def get(self, request: Request) -> UserSessionSchema | None:
        """Get current user session."""
        await self._ensure_session_loaded(request)

        user_id = request.session.get(self.USER_ID_KEY)
        is_admin = bool(request.session.get(self.IS_ADMIN_KEY))

        if user_id is None:
            return None

        return UserSessionSchema(id=user_id, is_admin=is_admin)

    async def destroy(self, request: Request) -> None:
        """Destroy current session."""
        await self._ensure_session_loaded(request)
        request.session.clear()

    async def clear_all_user_sessions(self, *, user_id: int) -> int:
        """
        Clear all sessions for a specific user (admin operation).
        Returns the number of sessions deleted.
        """
        deleted_count = 0
        cursor = 0

        while True:
            cursor, keys = await self.redis_client.scan(
                cursor=cursor, match=f"{settings.PREFIX}*", count=100
            )

            for key in keys:
                session_data = await self.redis_client.hgetall(key)  # type: ignore

                if session_data and session_data.get(self.USER_ID_KEY.encode()):
                    stored_user_id = int(session_data[self.USER_ID_KEY.encode()])
                    if stored_user_id == user_id:
                        await self.redis_client.delete(key)
                        deleted_count += 1

            if cursor == 0:
                break

        return deleted_count


session_manager = SessionManager(redis_client=client)
