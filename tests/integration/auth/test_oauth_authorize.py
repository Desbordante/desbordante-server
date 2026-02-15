import pytest
from fastapi import status
from httpx import AsyncClient

from src.schemas.auth_schemas import OAuthProvider
from tests.integration.auth.constants import OAUTH_AUTHORIZE_ENDPOINT

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize("provider", [provider for provider in OAuthProvider])
async def test_oauth_authorize(client: AsyncClient, provider: OAuthProvider):
    """Test successful oauth authorize"""
    response = await client.get(
        OAUTH_AUTHORIZE_ENDPOINT.format(provider=provider.value),
    )

    assert response.status_code == status.HTTP_302_FOUND
