import pytest
from fastapi import status
from httpx import AsyncClient

from src.schemas.auth_schemas import OAuthProvider
from tests.integration.auth.constants import (
    MOCK_AUTHORIZE_URL_TEMPLATE,
    OAUTH_AUTHORIZE_ENDPOINT,
)

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize("provider", list(OAuthProvider))
async def test_oauth_authorize_redirects_to_provider(
    client: AsyncClient, mock_oauth_adapter, provider: OAuthProvider
):
    """Test that oauth authorize returns a redirect to the provider's authorization URL."""
    response = await client.get(
        OAUTH_AUTHORIZE_ENDPOINT.format(provider=provider.value),
    )

    assert response.status_code == status.HTTP_302_FOUND
    assert response.headers["location"] == MOCK_AUTHORIZE_URL_TEMPLATE.format(
        provider=provider.value
    )


@pytest.mark.parametrize("provider", list(OAuthProvider))
async def test_oauth_authorize_calls_adapter_with_correct_args(
    client: AsyncClient, mock_oauth_adapter, provider: OAuthProvider
):
    """Test that the adapter is called with the correct provider and callback redirect_uri."""
    await client.get(
        OAUTH_AUTHORIZE_ENDPOINT.format(provider=provider.value),
    )

    mock_oauth_adapter.get_authorization_redirect.assert_awaited_once()
    call_kwargs = mock_oauth_adapter.get_authorization_redirect.call_args.kwargs
    assert call_kwargs["provider"] == provider
    assert f"/{provider.value}/callback/" in call_kwargs["redirect_uri"]


async def test_oauth_authorize_rejects_invalid_provider(client: AsyncClient):
    """Test that an invalid provider returns a validation error."""
    response = await client.get(
        OAUTH_AUTHORIZE_ENDPOINT.format(provider="invalid_provider"),
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
