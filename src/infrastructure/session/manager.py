import secrets
from datetime import datetime, timedelta, timezone

from redis.asyncio import Redis

from src.infrastructure.session.config import settings
from src.schemas.session_schemas import SessionSchema


class SessionManager:
    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    def _now(self) -> datetime:
        return datetime.now(timezone.utc)

    def _session_key(self, session_id: str) -> str:
        return f"{settings.SESSION_KEY_PREFIX}:{session_id}"

    def _user_index_key(self, user_id: int) -> str:
        return f"{settings.SESSION_INDEX_KEY_PREFIX}:{user_id}"

    def _compute_expire_at(self, session: SessionSchema) -> datetime:
        now = self._now()
        deadline = session.created_at + timedelta(
            seconds=settings.SESSION_ABSOLUTE_LIFETIME
        )
        return min(
            now + timedelta(seconds=settings.SESSION_ROLLING_LIFETIME),
            deadline,
        )

    async def create(self, *, user_id: int, is_admin: bool) -> str:
        session_id = secrets.token_urlsafe(settings.SESSION_TOKEN_BYTES)

        session_data = SessionSchema(
            user_id=user_id,
            is_admin=is_admin,
            created_at=self._now(),
        )

        index_key = self._user_index_key(user_id)
        pipe = self.redis.pipeline()
        pipe.set(
            self._session_key(session_id),
            session_data.model_dump_json(),
            ex=settings.SESSION_ROLLING_LIFETIME,
        )
        pipe.sadd(index_key, session_id)
        pipe.expire(index_key, settings.SESSION_ROLLING_LIFETIME, gt=True)
        await pipe.execute()

        return session_id

    async def get(self, *, session_id: str) -> SessionSchema | None:
        key = self._session_key(session_id)
        session_data = await self.redis.get(key)

        if not session_data:
            return None

        session = SessionSchema.model_validate_json(session_data)
        expire_at = self._compute_expire_at(session)

        pipe = self.redis.pipeline()
        pipe.expireat(key, expire_at)
        pipe.expireat(self._user_index_key(session.user_id), expire_at, gt=True)
        await pipe.execute()

        return session

    async def destroy(self, *, session_id: str) -> None:
        session_data = await self.redis.get(self._session_key(session_id))

        pipe = self.redis.pipeline()
        pipe.delete(self._session_key(session_id))

        if session_data:
            user_id = SessionSchema.model_validate_json(session_data).user_id
            pipe.srem(self._user_index_key(user_id), session_id)

        await pipe.execute()

    async def destroy_all_user_sessions(self, *, user_id: int) -> None:
        index_key = self._user_index_key(user_id)
        session_ids = await self.redis.smembers(index_key)  # type: ignore

        if not session_ids:
            return

        session_keys = [self._session_key(sid) for sid in session_ids]

        pipe = self.redis.pipeline()
        pipe.delete(*session_keys)
        pipe.delete(index_key)
        await pipe.execute()
