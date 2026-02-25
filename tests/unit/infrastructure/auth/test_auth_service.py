from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.responses import RedirectResponse

from src.infrastructure.auth.auth_service import AuthService
from src.schemas.auth_schemas import AuthProvider, AuthUserInfoSchema

from tests.unit.infrastructure.auth.constants import (
    FAKE_OAUTH_ID,
    FAKE_OAUTH_REDIRECT_URL,
    FAKE_REDIRECT_URI,
)

pytestmark = pytest.mark.asyncio


@patch("src.infrastructure.auth.auth_service.GoogleAuthProvider")
@patch("src.infrastructure.auth.auth_service.GitHubAuthProvider")
async def test_get_authorization_redirect_delegates_to_provider(
    mock_github_provider: MagicMock,
    mock_google_provider: MagicMock,
    request_mock: MagicMock,
) -> None:
    mock_provider = MagicMock()
    mock_provider.get_authorization_redirect = AsyncMock(
        return_value=RedirectResponse(url=FAKE_OAUTH_REDIRECT_URL, status_code=302)
    )
    mock_github_provider.return_value = mock_provider
    mock_google_provider.return_value = MagicMock()

    service = AuthService(request=request_mock)
    result = await service.get_authorization_redirect(
        provider=AuthProvider.GITHUB, redirect_uri=FAKE_REDIRECT_URI
    )

    assert result.status_code == 302
    assert result.headers["location"] == FAKE_OAUTH_REDIRECT_URL
    mock_provider.get_authorization_redirect.assert_awaited_once_with(
        request_mock, FAKE_REDIRECT_URI
    )


@patch("src.infrastructure.auth.auth_service.GoogleAuthProvider")
@patch("src.infrastructure.auth.auth_service.GitHubAuthProvider")
async def test_get_userinfo_delegates_to_provider(
    mock_github_provider: MagicMock,
    mock_google_provider: MagicMock,
    request_mock: MagicMock,
) -> None:
    expected_schema = AuthUserInfoSchema(
        account_id=FAKE_OAUTH_ID,
        email="test@example.com",
        is_verified=True,
    )
    mock_provider = MagicMock()
    mock_provider.get_userinfo = AsyncMock(return_value=expected_schema)
    mock_github_provider.return_value = mock_provider
    mock_google_provider.return_value = MagicMock()

    service = AuthService(request=request_mock)
    result = await service.get_userinfo(provider=AuthProvider.GITHUB)

    assert result == expected_schema
    mock_provider.get_userinfo.assert_awaited_once_with(request_mock)
