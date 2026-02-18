from unittest.mock import AsyncMock

import pytest
from fastapi.responses import RedirectResponse

from src.api.auth.dependencies import get_oauth_adapter, get_session_manager
from src.main import app
from src.schemas.auth_schemas import OAuthProvider, OAuthUserInfoSchema
from tests.integration.auth.constants import MOCK_AUTHORIZE_URL_TEMPLATE

MOCK_OAUTH_ID = "test_oauth_id_123"


@pytest.fixture
def mock_oauth_adapter():
    adapter = AsyncMock()

    async def fake_get_authorization_redirect(
        *, provider: OAuthProvider, request, redirect_uri: str
    ) -> RedirectResponse:
        url = MOCK_AUTHORIZE_URL_TEMPLATE.format(provider=provider.value)
        return RedirectResponse(url=url, status_code=302)

    async def fake_get_user_info(
        *, provider: OAuthProvider, request
    ) -> OAuthUserInfoSchema:
        return OAuthUserInfoSchema(id=MOCK_OAUTH_ID)

    adapter.get_authorization_redirect = AsyncMock(
        side_effect=fake_get_authorization_redirect
    )
    adapter.get_user_info = AsyncMock(side_effect=fake_get_user_info)

    app.dependency_overrides[get_oauth_adapter] = lambda: adapter
    yield adapter
    app.dependency_overrides.pop(get_oauth_adapter, None)


@pytest.fixture
def mock_session_manager():
    manager = AsyncMock()
    app.dependency_overrides[get_session_manager] = lambda: manager
    yield manager
    app.dependency_overrides.pop(get_session_manager, None)
