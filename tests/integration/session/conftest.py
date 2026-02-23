from typing import AsyncGenerator

import pytest
import pytest_asyncio
from fakeredis import FakeAsyncRedis

from src.domain.session import config as session_config
from src.infrastructure.session.manager import SessionManager

from tests.integration.session.constants import (
    TEST_SESSION_ABSOLUTE_LIFETIME,
    TEST_SESSION_ROLLING_LIFETIME,
)


@pytest.fixture(scope="function", autouse=True)
def fixed_session_lifetimes(monkeypatch: pytest.MonkeyPatch) -> None:
    """Pin SESSION_ROLLING_LIFETIME and SESSION_ABSOLUTE_LIFETIME for tests."""
    monkeypatch.setattr(
        session_config.settings,
        "SESSION_ROLLING_LIFETIME",
        TEST_SESSION_ROLLING_LIFETIME,
    )
    monkeypatch.setattr(
        session_config.settings,
        "SESSION_ABSOLUTE_LIFETIME",
        TEST_SESSION_ABSOLUTE_LIFETIME,
    )


@pytest_asyncio.fixture(scope="function")
async def redis() -> AsyncGenerator[FakeAsyncRedis, None]:
    client = FakeAsyncRedis(decode_responses=True)
    yield client
    await client.aclose()


@pytest_asyncio.fixture(scope="function")
async def session_manager(redis: FakeAsyncRedis) -> SessionManager:
    return SessionManager(redis)
