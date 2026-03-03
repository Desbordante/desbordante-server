from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.infrastructure.auth.auth_service import AuthService
from src.infrastructure.auth.providers.github import GitHubAuthProvider
from src.infrastructure.auth.providers.google import GoogleAuthProvider
from src.schemas.auth_schemas import AuthProvider

pytestmark = pytest.mark.asyncio


@patch("src.infrastructure.auth.auth_service.OAuth")
async def test_auth_service_creates_github_and_google_providers(
    mock_oauth_class: MagicMock,
    request_mock: MagicMock,
) -> None:
    mock_oauth = MagicMock()
    mock_oauth_class.return_value = mock_oauth

    service = AuthService(request=request_mock)

    assert AuthProvider.GITHUB in service._providers
    assert AuthProvider.GOOGLE in service._providers
    assert isinstance(service._providers[AuthProvider.GITHUB], GitHubAuthProvider)
    assert isinstance(service._providers[AuthProvider.GOOGLE], GoogleAuthProvider)


@patch("src.infrastructure.auth.providers.github.settings")
async def test_github_provider_get_userinfo(
    mock_settings: MagicMock,
    request_mock: MagicMock,
) -> None:
    from src.schemas.auth_schemas import AuthUserInfoSchema

    mock_settings.GITHUB_CLIENT_ID = "test"
    mock_settings.GITHUB_CLIENT_SECRET = "test"

    mock_oauth = MagicMock()
    mock_client = MagicMock()
    mock_oauth.register.return_value = mock_client

    userinfo = {"id": 46863908}
    mock_client.authorize_access_token = AsyncMock(return_value={})
    mock_client.userinfo = AsyncMock(return_value=userinfo)
    mock_client.get = AsyncMock(
        return_value=MagicMock(
            raise_for_status=MagicMock(),
            json=MagicMock(
                return_value=[
                    {"email": "vaifaer@gmail.com", "primary": True, "verified": True},
                ]
            ),
        )
    )

    provider = GitHubAuthProvider(mock_oauth)
    result = await provider.get_userinfo(request_mock)

    assert isinstance(result, AuthUserInfoSchema)
    assert result.account_id == "46863908"
    assert result.email == "vaifaer@gmail.com"
    assert result.is_verified is True


@patch("src.infrastructure.auth.providers.google.settings")
async def test_google_provider_get_userinfo(
    mock_settings: MagicMock,
    request_mock: MagicMock,
) -> None:
    from src.schemas.auth_schemas import AuthUserInfoSchema

    mock_settings.GOOGLE_CLIENT_ID = "test"
    mock_settings.GOOGLE_CLIENT_SECRET = "test"

    mock_oauth = MagicMock()
    mock_client = MagicMock()
    mock_oauth.register.return_value = mock_client

    userinfo = {"sub": "google-123", "email": "user@gmail.com", "email_verified": True}
    mock_client.authorize_access_token = AsyncMock(return_value={"userinfo": userinfo})

    provider = GoogleAuthProvider(mock_oauth)
    result = await provider.get_userinfo(request_mock)

    assert isinstance(result, AuthUserInfoSchema)
    assert result.account_id == "google-123"
    assert result.email == "user@gmail.com"
    assert result.is_verified is True
