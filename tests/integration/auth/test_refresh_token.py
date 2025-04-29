import asyncio
from datetime import timedelta
from typing import Any, Dict

import pytest
from fastapi import status
from httpx import AsyncClient

from src.domain.security.utils import create_token, decode_token
from src.schemas.auth_schemas import RefreshTokenPayloadSchema

pytestmark = pytest.mark.asyncio


async def test_refresh_token_success(
    client: AsyncClient, logged_in_user: Dict[str, Any]
):
    """Test successful token refresh"""
    await asyncio.sleep(1)

    # Use only refresh_token
    response = await client.post(
        "/auth/refresh", cookies={"refresh_token": logged_in_user["refresh_token"]}
    )

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert "user" in response.json()
    assert response.json()["user"]["email"] == logged_in_user["user"]["email"]

    # Check that new tokens are different from old ones
    assert response.json()["access_token"] != logged_in_user["access_token"]

    # Check that cookies are set
    assert "access_token" in response.cookies
    assert "refresh_token" in response.cookies


async def test_refresh_token_missing(client: AsyncClient):
    """Test token refresh without providing refresh_token"""
    response = await client.post(
        "/auth/refresh",
        cookies={},  # No refresh_token
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "detail" in response.json()


async def test_refresh_token_invalid(client: AsyncClient):
    """Test token refresh with invalid refresh_token"""
    response = await client.post(
        "/auth/refresh", cookies={"refresh_token": "invalid_token"}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "detail" in response.json()


async def test_refresh_token_expired(
    client: AsyncClient, logged_in_user: Dict[str, Any]
):
    """Test token refresh with expired refresh_token"""

    decoded_token_data = decode_token(
        schema=RefreshTokenPayloadSchema, token=logged_in_user["refresh_token"]
    )

    expired_token_pair = create_token(
        schema=RefreshTokenPayloadSchema,
        payload=decoded_token_data.model_dump(),
        expires_delta=timedelta(days=-1),
    )

    response = await client.post(
        "/auth/refresh",
        cookies={"refresh_token": expired_token_pair.token},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "detail" in response.json()
