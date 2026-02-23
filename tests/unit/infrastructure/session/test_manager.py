from datetime import datetime

import pytest

from src.domain.session.config import settings
from src.schemas.session_schemas import SessionSchema

pytestmark = pytest.mark.asyncio


async def test_create_returns_string_and_calls_redis_set_and_sadd(
    session_manager, redis_mock
):
    """create() returns a session_id string and stores session data and user index via Redis set/sadd."""
    user_id = 42
    is_admin = True

    session_id = await session_manager.create(user_id=user_id, is_admin=is_admin)

    assert isinstance(session_id, str)
    assert len(session_id) > 0

    pipe = redis_mock.pipeline.return_value
    pipe.set.assert_called_once()
    set_key, set_value = pipe.set.call_args[0]
    assert set_key == f"{settings.SESSION_KEY_PREFIX}:{session_id}"
    assert pipe.set.call_args[1]["ex"] == settings.SESSION_ROLLING_LIFETIME

    session = SessionSchema.model_validate_json(set_value)
    assert session.user_id == user_id
    assert session.is_admin is is_admin
    assert session.created_at is not None
    assert isinstance(session.created_at, datetime)

    pipe.sadd.assert_called_once_with(
        f"{settings.SESSION_INDEX_KEY_PREFIX}:{user_id}",
        session_id,
    )
    pipe.execute.assert_awaited_once()
