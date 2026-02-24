from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import Request
from fastapi.responses import RedirectResponse

from tests.unit.infrastructure.auth.constants import (
    FAKE_OAUTH_REDIRECT_URL,
)


@pytest.fixture
def request_mock() -> MagicMock:
    return MagicMock(spec=Request)


@pytest.fixture
def oauth_client_mock() -> MagicMock:
    client = MagicMock()
    client.authorize_redirect = AsyncMock(
        return_value=RedirectResponse(url=FAKE_OAUTH_REDIRECT_URL, status_code=302)
    )
    client.authorize_access_token = AsyncMock(
        return_value={"userinfo": {"id": "123", "login": "test"}}
    )
    client.userinfo = AsyncMock(return_value={"id": "123"})
    return client


@pytest.fixture
def oauth_registry_mock(oauth_client_mock: MagicMock) -> MagicMock:
    registry = MagicMock()
    registry.create_client = MagicMock(return_value=oauth_client_mock)
    return registry
