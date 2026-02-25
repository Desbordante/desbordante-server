from typing import Generator
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.responses import RedirectResponse
from starlette.requests import Request

from src.api.auth.dependencies import get_auth_service
from src.main import app

from tests.integration.auth.constants import (
    FAKE_OAUTH_REDIRECT_URL,
    FAKE_REDIRECT_URI,
)


@pytest.fixture
def url_for_mock() -> MagicMock:
    return MagicMock(return_value=FAKE_REDIRECT_URI)


@pytest.fixture
def oauth_service_mock() -> MagicMock:
    service = MagicMock()
    service.get_authorization_redirect = AsyncMock(
        return_value=RedirectResponse(url=FAKE_OAUTH_REDIRECT_URL, status_code=302)
    )
    return service


@pytest.fixture(autouse=True)
def mock_oauth(
    oauth_service_mock: MagicMock,
    url_for_mock: MagicMock,
    monkeypatch: pytest.MonkeyPatch,
) -> Generator[None, None, None]:
    """Replace OAuth service and request.url_for to avoid real requests."""

    def _override(request: Request) -> MagicMock:
        return oauth_service_mock

    monkeypatch.setattr(Request, "url_for", url_for_mock)
    app.dependency_overrides[get_auth_service] = _override
    yield
    app.dependency_overrides.pop(get_auth_service, None)
