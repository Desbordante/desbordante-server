import re
from datetime import datetime, timedelta, timezone

import pytest
from fakeredis import FakeAsyncRedis

from src.domain.session.config import settings
from src.infrastructure.session.manager import SessionManager
from src.schemas.session_schemas import SessionSchema
from tests.integration.session.constants import (
    ABSOLUTE_REMAINING_SEC,
    NONEXISTENT_SESSION_ID,
    NONEXISTENT_USER_ID,
    OTHER_USER_ID,
    SHORT_LIFETIME,
    TEST_SESSION_ABSOLUTE_TTL,
    TEST_SESSION_OLD,
    TEST_USER_ID,
)

pytestmark = pytest.mark.asyncio


def _session_key(session_id: str) -> str:
    return f"{settings.SESSION_KEY_PREFIX}:{session_id}"


def _index_key(user_id: int) -> str:
    return f"{settings.SESSION_INDEX_KEY_PREFIX}:{user_id}"


async def create_session_for_user(
    session_manager: SessionManager,
    user_id: int,
    *,
    is_admin: bool = False,
) -> tuple[str, str, str]:
    """Create a session and return (session_id, session_key, index_key)."""
    session_id = await session_manager.create(user_id=user_id, is_admin=is_admin)
    return session_id, _session_key(session_id), _index_key(user_id)


async def assert_session_in_redis(
    redis: FakeAsyncRedis,
    session_id: str,
    user_id: int,
    is_admin: bool,
) -> None:
    """Assert session key exists and contains correct user_id and is_admin."""
    key = _session_key(session_id)
    raw = await redis.get(key)
    assert raw is not None
    session = SessionSchema.model_validate_json(raw)
    assert session.user_id == user_id
    assert session.is_admin is is_admin
    assert session.created_at is not None


async def assert_session_key_absent(redis: FakeAsyncRedis, session_id: str) -> None:
    """Assert session key does not exist."""
    assert await redis.get(_session_key(session_id)) is None


async def assert_index_empty(redis: FakeAsyncRedis, user_id: int) -> None:
    """Assert user index key does not exist."""
    assert await redis.exists(_index_key(user_id)) == 0


async def assert_index_has_session(
    redis: FakeAsyncRedis, user_id: int, session_id: str
) -> None:
    """Assert session_id is in user index."""
    members = await redis.smembers(_index_key(user_id))  # type: ignore
    assert session_id in members


async def assert_index_lacks_session(
    redis: FakeAsyncRedis, user_id: int, session_id: str
) -> None:
    """Assert session_id is not in user index."""
    members = await redis.smembers(_index_key(user_id))  # type: ignore
    assert session_id not in members


async def test_create_returns_string_and_stores_data_in_redis(
    session_manager: SessionManager, redis: FakeAsyncRedis
):
    """create() returns session_id and stores session data and user index in Redis."""
    user_id = 42
    is_admin = True

    session_id = await session_manager.create(user_id=user_id, is_admin=is_admin)

    assert isinstance(session_id, str)
    assert len(session_id) > 0
    assert re.fullmatch(r"[A-Za-z0-9_-]+", session_id), "session_id must be URL-safe"

    session_key = _session_key(session_id)
    raw = await redis.get(session_key)
    assert raw is not None
    ttl = await redis.ttl(session_key)
    assert ttl > 0
    assert ttl <= settings.SESSION_ROLLING_LIFETIME

    await assert_session_in_redis(redis, session_id, user_id, is_admin)
    await assert_index_has_session(redis, user_id, session_id)
    assert await redis.ttl(_index_key(user_id)) > 0


async def test_get_returns_none_when_key_missing(session_manager: SessionManager):
    """get() returns None when session key does not exist."""
    result = await session_manager.get(session_id=NONEXISTENT_SESSION_ID)
    assert result is None


async def test_get_returns_session_when_key_exists(
    session_manager: SessionManager, redis: FakeAsyncRedis
):
    """get() returns SessionSchema when session exists in Redis."""
    session_id, _, _ = await create_session_for_user(session_manager, TEST_USER_ID)

    session = await session_manager.get(session_id=session_id)

    assert session is not None
    assert session.user_id == TEST_USER_ID
    assert session.is_admin is False
    assert session.created_at is not None


async def test_get_extends_ttl_rolling(
    session_manager: SessionManager, redis: FakeAsyncRedis
):
    """get() extends session TTL (rolling refresh) when it was set shorter."""
    session_id, session_key, _ = await create_session_for_user(
        session_manager, TEST_USER_ID
    )
    await redis.expire(session_key, SHORT_LIFETIME)
    ttl_before = await redis.ttl(session_key)
    assert 0 < ttl_before <= SHORT_LIFETIME

    await session_manager.get(session_id=session_id)

    ttl_after = await redis.ttl(session_key)
    assert ttl_after > SHORT_LIFETIME
    assert ttl_after <= settings.SESSION_ROLLING_LIFETIME


async def test_get_extends_index_ttl(
    session_manager: SessionManager, redis: FakeAsyncRedis
):
    """get() extends index TTL when it was set shorter."""
    session_id, _, index_key = await create_session_for_user(
        session_manager, TEST_USER_ID
    )
    await redis.expire(index_key, SHORT_LIFETIME)
    ttl_before = await redis.ttl(index_key)
    assert 0 < ttl_before <= SHORT_LIFETIME

    await session_manager.get(session_id=session_id)

    ttl_after = await redis.ttl(index_key)
    assert ttl_after > SHORT_LIFETIME


async def test_get_does_not_extend_ttl_beyond_absolute(
    session_manager: SessionManager, redis: FakeAsyncRedis
):
    """get() does not set TTL above remaining time until absolute deadline."""
    session_key = _session_key(TEST_SESSION_ABSOLUTE_TTL)
    created_at = datetime.now(timezone.utc) - timedelta(
        seconds=settings.SESSION_ABSOLUTE_LIFETIME - ABSOLUTE_REMAINING_SEC
    )
    data = SessionSchema(user_id=TEST_USER_ID, is_admin=False, created_at=created_at)
    await redis.set(
        session_key,
        data.model_dump_json(),
        ex=settings.SESSION_ROLLING_LIFETIME,
    )

    await session_manager.get(session_id=TEST_SESSION_ABSOLUTE_TTL)

    ttl = await redis.ttl(session_key)
    assert 0 < ttl < settings.SESSION_ROLLING_LIFETIME
    assert ttl <= ABSOLUTE_REMAINING_SEC


async def test_destroy_removes_session_key_and_from_user_index(
    session_manager: SessionManager, redis: FakeAsyncRedis
):
    """destroy() removes session key and session_id from user index when session exists."""
    user_id = 7
    session_id, session_key, index_key = await create_session_for_user(
        session_manager, user_id, is_admin=True
    )

    await session_manager.destroy(session_id=session_id)

    await assert_session_key_absent(redis, session_id)
    await assert_index_lacks_session(redis, user_id, session_id)
    await assert_index_empty(redis, user_id)


async def test_destroy_nonexistent_session_does_not_raise(
    session_manager: SessionManager,
):
    """destroy() does not raise when session key does not exist."""
    await session_manager.destroy(session_id=NONEXISTENT_SESSION_ID)


async def test_destroy_removes_only_given_session_from_user_index(
    session_manager: SessionManager, redis: FakeAsyncRedis
):
    """destroy() removes only the given session; other sessions of the same user remain."""
    user_id = 10
    session_id_1, key_1, index_key = await create_session_for_user(
        session_manager, user_id, is_admin=False
    )
    session_id_2, key_2, _ = await create_session_for_user(
        session_manager, user_id, is_admin=True
    )

    await session_manager.destroy(session_id=session_id_1)

    await assert_session_key_absent(redis, session_id_1)
    assert await redis.get(key_2) is not None
    await assert_index_lacks_session(redis, user_id, session_id_1)
    await assert_index_has_session(redis, user_id, session_id_2)


async def test_destroy_all_user_sessions_removes_all_sessions_and_index(
    session_manager: SessionManager, redis: FakeAsyncRedis
):
    """destroy_all_user_sessions() removes all session keys and the user index."""
    user_id = 5
    session_id_1, key_1, index_key = await create_session_for_user(
        session_manager, user_id, is_admin=False
    )
    session_id_2, key_2, _ = await create_session_for_user(
        session_manager, user_id, is_admin=True
    )

    await session_manager.destroy_all_user_sessions(user_id=user_id)

    await assert_session_key_absent(redis, session_id_1)
    await assert_session_key_absent(redis, session_id_2)
    await assert_index_empty(redis, user_id)


async def test_destroy_all_user_sessions_empty_index_does_not_raise(
    session_manager: SessionManager,
):
    """destroy_all_user_sessions() does not raise when user has no sessions."""
    await session_manager.destroy_all_user_sessions(user_id=NONEXISTENT_USER_ID)


async def test_destroy_all_user_sessions_removes_index_when_session_keys_expired(
    session_manager: SessionManager, redis: FakeAsyncRedis
):
    """destroy_all_user_sessions() removes index even when session keys already expired (simulated by manual delete)."""
    user_id = 6
    session_id_1, key_1, index_key = await create_session_for_user(
        session_manager, user_id, is_admin=False
    )
    session_id_2, key_2, _ = await create_session_for_user(
        session_manager, user_id, is_admin=True
    )

    await redis.delete(key_1, key_2)

    await session_manager.destroy_all_user_sessions(user_id=user_id)

    await assert_index_empty(redis, user_id)


async def test_get_missing_session_does_not_touch_index(
    session_manager: SessionManager, redis: FakeAsyncRedis
):
    """get() when session key is gone (e.g. expired) does not modify index."""
    session_id, session_key, index_key = await create_session_for_user(
        session_manager, TEST_USER_ID
    )

    await redis.delete(session_key)

    result = await session_manager.get(session_id=session_id)

    assert result is None
    await assert_index_has_session(redis, TEST_USER_ID, session_id)


async def test_index_contains_only_own_user_sessions(
    session_manager: SessionManager, redis: FakeAsyncRedis
):
    """Each user's index contains only that user's session_ids."""
    session_1, _, _ = await create_session_for_user(
        session_manager, TEST_USER_ID, is_admin=False
    )
    session_2, _, _ = await create_session_for_user(
        session_manager, OTHER_USER_ID, is_admin=True
    )

    members_1 = await redis.smembers(_index_key(TEST_USER_ID))  # type: ignore
    members_2 = await redis.smembers(_index_key(OTHER_USER_ID))  # type: ignore

    assert members_1 == {session_1}
    assert members_2 == {session_2}


async def test_get_does_not_shorten_index_ttl_with_gt(
    session_manager: SessionManager, redis: FakeAsyncRedis
):
    """get() on session with short remaining time does not shorten index TTL (gt=True)."""
    await create_session_for_user(session_manager, TEST_USER_ID, is_admin=True)
    index_key = _index_key(TEST_USER_ID)
    ttl_before = await redis.ttl(index_key)  # type: ignore[misc]
    assert ttl_before > 100

    session_key_a = _session_key(TEST_SESSION_OLD)
    created_at_old = datetime.now(timezone.utc) - timedelta(
        seconds=settings.SESSION_ABSOLUTE_LIFETIME - 60
    )
    data_a = SessionSchema(
        user_id=TEST_USER_ID, is_admin=False, created_at=created_at_old
    )
    await redis.set(session_key_a, data_a.model_dump_json(), ex=120)
    await redis.sadd(index_key, TEST_SESSION_OLD)  # type: ignore[misc]

    await session_manager.get(session_id=TEST_SESSION_OLD)

    ttl_after = await redis.ttl(index_key)  # type: ignore[misc]
    assert ttl_after > 100


async def test_destroy_all_user_sessions_does_not_affect_other_users(
    session_manager: SessionManager, redis: FakeAsyncRedis
):
    """destroy_all_user_sessions() removes only the given user's sessions."""
    session_a, key_a, index_a = await create_session_for_user(
        session_manager, TEST_USER_ID, is_admin=False
    )
    session_b, key_b, index_b = await create_session_for_user(
        session_manager, OTHER_USER_ID, is_admin=True
    )

    await session_manager.destroy_all_user_sessions(user_id=TEST_USER_ID)

    await assert_session_key_absent(redis, session_a)
    await assert_index_empty(redis, TEST_USER_ID)
    assert await redis.get(key_b) is not None
    assert await redis.exists(index_b) == 1
