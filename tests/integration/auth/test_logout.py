import pytest
from fastapi import status
from httpx import AsyncClient

from tests.integration.auth.constants import LOGOUT_ENDPOINT
from tests.integration.auth.types import RegisteredUserResponse

pytestmark = pytest.mark.asyncio


async def test_logout(client: AsyncClient, registered_user: RegisteredUserResponse):
    """Test successful logout"""
    # Check that auth cookies are set
    assert "access_token" in client.cookies
    assert "refresh_token" in client.cookies

    response = await client.post(LOGOUT_ENDPOINT)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Check that cookies were cleared
    cookie_header = response.headers.get("set-cookie", "")
    assert "access_token=;" in cookie_header or "access_token=" in cookie_header
    assert "refresh_token=;" in cookie_header or "refresh_token=" in cookie_header
