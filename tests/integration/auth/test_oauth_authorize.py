from unittest.mock import MagicMock

import pytest
from httpx import AsyncClient

from src.schemas.auth_schemas import OAuthProvider

from tests.integration.auth.constants import (
    FAKE_OAUTH_REDIRECT_URL,
    FAKE_REDIRECT_URI,
    OAUTH_AUTHORIZE_PATH,
)

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize("provider", list(OAuthProvider))
async def test_oauth_authorize_success(
    client: AsyncClient,
    oauth_service_mock: MagicMock,
    url_for_mock: MagicMock,
    provider: OAuthProvider,
) -> None:
    """Returns 302, calls url_for and OAuthService.get_authorization_redirect with correct params."""
    response = await client.get(
        OAUTH_AUTHORIZE_PATH.format(provider=provider.value),
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["location"] == FAKE_OAUTH_REDIRECT_URL
    url_for_mock.assert_called_once_with("oauth_callback", provider=provider.value)
    oauth_service_mock.get_authorization_redirect.assert_called_once_with(
        provider=provider,
        redirect_uri=FAKE_REDIRECT_URI,
    )
    oauth_service_mock.get_userinfo.assert_not_called()


async def test_oauth_authorize_invalid_provider_returns_422(
    client: AsyncClient,
) -> None:
    """GET /v1/auth/{provider}/authorize/ returns 422 when provider is invalid."""
    response = await client.get(
        OAUTH_AUTHORIZE_PATH.format(provider="invalid"),
        follow_redirects=False,
    )

    assert response.status_code == 422
