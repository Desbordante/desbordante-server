from typing import Any, Dict

import pytest
from fastapi import status
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_logout_success(client: AsyncClient, logged_in_user: Dict[str, Any]):
    """Test successful logout"""
    # Check that auth cookies are set
    assert "access_token" in client.cookies
    assert "refresh_token" in client.cookies

    response = await client.post("/auth/logout")

    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Check that cookies were cleared
    cookie_header = response.headers.get("set-cookie", "")
    assert "access_token=;" in cookie_header or "access_token=" in cookie_header
    assert "refresh_token=;" in cookie_header or "refresh_token=" in cookie_header


async def test_logout_unauthenticated(client: AsyncClient):
    """Test logout when unauthenticated"""
    # Send request without cookies
    response = await client.post("/auth/logout", cookies={})

    # Logout should succeed even if the user is not authenticated
    assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_logout_invalid_tokens(client: AsyncClient):
    """Test logout with invalid tokens"""
    # Use explicit cookies with invalid tokens
    invalid_cookies = {
        "access_token": "invalid_token",
        "refresh_token": "invalid_token",
    }

    response = await client.post("/auth/logout", cookies=invalid_cookies)

    # Logout should succeed even with invalid tokens
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Check that cookies were cleared
    cookie_header = response.headers.get("set-cookie", "")
    assert "access_token=;" in cookie_header or "access_token=" in cookie_header
    assert "refresh_token=;" in cookie_header or "refresh_token=" in cookie_header
