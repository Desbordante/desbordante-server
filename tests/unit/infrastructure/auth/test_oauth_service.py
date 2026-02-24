from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.infrastructure.auth.oauth_service import AuthlibOAuthService
from src.schemas.auth_schemas import OAuthProvider

from tests.unit.infrastructure.auth.constants import (
    FAKE_OAUTH_ID,
    FAKE_OAUTH_REDIRECT_URL,
    FAKE_REDIRECT_URI,
)

pytestmark = pytest.mark.asyncio


@patch("src.infrastructure.auth.oauth_service.extract_oauth_id")
@patch("src.infrastructure.auth.oauth_service.create_oauth_registry")
async def test_get_authorization_redirect_calls_client_with_request_and_uri(
    mock_create_registry: MagicMock,
    mock_extract_oauth_id: MagicMock,
    request_mock: MagicMock,
    oauth_registry_mock: MagicMock,
    oauth_client_mock: MagicMock,
) -> None:
    mock_create_registry.return_value = oauth_registry_mock

    service = AuthlibOAuthService(request=request_mock)
    result = await service.get_authorization_redirect(
        provider=OAuthProvider.GITHUB, redirect_uri=FAKE_REDIRECT_URI
    )

    assert result.status_code == 302
    assert result.headers["location"] == FAKE_OAUTH_REDIRECT_URL
    oauth_registry_mock.create_client.assert_called_once_with(
        OAuthProvider.GITHUB.value
    )
    oauth_client_mock.authorize_redirect.assert_awaited_once_with(
        request_mock, FAKE_REDIRECT_URI
    )


@patch("src.infrastructure.auth.oauth_service.extract_oauth_id")
@patch("src.infrastructure.auth.oauth_service.create_oauth_registry")
async def test_get_userinfo_returns_schema_from_token_userinfo(
    mock_create_registry: MagicMock,
    mock_extract_oauth_id: MagicMock,
    request_mock: MagicMock,
    oauth_registry_mock: MagicMock,
    oauth_client_mock: MagicMock,
) -> None:
    mock_create_registry.return_value = oauth_registry_mock
    mock_extract_oauth_id.return_value = FAKE_OAUTH_ID
    oauth_client_mock.authorize_access_token = AsyncMock(
        return_value={"userinfo": {"id": "123"}}
    )

    service = AuthlibOAuthService(request=request_mock)
    result = await service.get_userinfo(provider=OAuthProvider.GITHUB)

    assert result.provider == OAuthProvider.GITHUB
    assert result.oauth_id == FAKE_OAUTH_ID
    oauth_client_mock.authorize_access_token.assert_awaited_once_with(request_mock)
    oauth_client_mock.userinfo.assert_not_called()
    mock_extract_oauth_id.assert_called_once_with({"id": "123"}, OAuthProvider.GITHUB)


@patch("src.infrastructure.auth.oauth_service.extract_oauth_id")
@patch("src.infrastructure.auth.oauth_service.create_oauth_registry")
async def test_get_userinfo_fetches_userinfo_when_not_in_token(
    mock_create_registry: MagicMock,
    mock_extract_oauth_id: MagicMock,
    request_mock: MagicMock,
    oauth_registry_mock: MagicMock,
    oauth_client_mock: MagicMock,
) -> None:
    mock_create_registry.return_value = oauth_registry_mock
    mock_extract_oauth_id.return_value = FAKE_OAUTH_ID
    oauth_client_mock.authorize_access_token = AsyncMock(return_value={})
    oauth_client_mock.userinfo = AsyncMock(return_value={"sub": "google-123"})

    service = AuthlibOAuthService(request=request_mock)
    result = await service.get_userinfo(provider=OAuthProvider.GOOGLE)

    assert result.provider == OAuthProvider.GOOGLE
    assert result.oauth_id == FAKE_OAUTH_ID
    oauth_client_mock.userinfo.assert_awaited_once()
    mock_extract_oauth_id.assert_called_once_with(
        {"sub": "google-123"}, OAuthProvider.GOOGLE
    )


@patch("src.infrastructure.auth.oauth_service.create_oauth_registry")
async def test_get_client_raises_for_unknown_provider(
    mock_create_registry: MagicMock,
    request_mock: MagicMock,
    oauth_registry_mock: MagicMock,
) -> None:
    mock_create_registry.return_value = oauth_registry_mock
    oauth_registry_mock.create_client.return_value = None

    service = AuthlibOAuthService(request=request_mock)

    with pytest.raises(ValueError, match="OAuth provider 'github' not found"):
        await service.get_authorization_redirect(
            provider=OAuthProvider.GITHUB, redirect_uri=FAKE_REDIRECT_URI
        )
