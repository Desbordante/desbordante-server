import pytest

from src.infrastructure.session import config as session_config
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
