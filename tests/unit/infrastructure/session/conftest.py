from unittest.mock import AsyncMock, MagicMock

import pytest

from src.domain.session import config as session_config
from src.infrastructure.session.manager import SessionManager

# Fixed session lifetimes for tests so they don't depend on config changes
TEST_SESSION_ROLLING_LIFETIME = 3600  # 1 hour


@pytest.fixture(autouse=True)
def fixed_session_rolling_lifetime(monkeypatch: pytest.MonkeyPatch) -> None:
    """Pin SESSION_ROLLING_LIFETIME for unit tests (create() ex= assertion)."""
    monkeypatch.setattr(
        session_config.settings,
        "SESSION_ROLLING_LIFETIME",
        TEST_SESSION_ROLLING_LIFETIME,
    )


@pytest.fixture
def redis_mock():
    """Mock async Redis: pipeline with set, sadd, execute."""
    pipe = MagicMock()
    pipe.set = MagicMock(return_value=pipe)
    pipe.sadd = MagicMock(return_value=pipe)
    pipe.execute = AsyncMock(return_value=None)

    redis = MagicMock()
    redis.pipeline.return_value = pipe
    return redis


@pytest.fixture
def session_manager(redis_mock):
    return SessionManager(redis_mock)
