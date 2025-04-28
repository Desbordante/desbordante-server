from typing import Any, Dict

import pytest
from fastapi import status
from httpx import AsyncClient

from src.schemas.user_schemas import UserSchema

pytestmark = pytest.mark.asyncio


async def test_get_current_user_with_cookie(
    client: AsyncClient, logged_in_user: Dict[str, Any]
):
    """Test getting current user information via cookies"""
    # Make request with access_token cookie
    response = await client.get(
        "/users/me", cookies={"access_token": logged_in_user["access_token"]}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"] == logged_in_user["user"]["email"]
    assert UserSchema.model_validate(response.json())


async def test_get_current_user_with_header(
    client: AsyncClient, logged_in_user: Dict[str, Any]
):
    """Test getting current user information via authorization header"""
    # Make request with Authorization header
    response = await client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {logged_in_user['access_token']}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"] == logged_in_user["user"]["email"]
    assert UserSchema.model_validate(response.json())


async def test_get_current_user_unauthorized(client: AsyncClient):
    """Test getting current user information when unauthorized"""
    response = await client.get("/users/me")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "detail" in response.json()


async def test_get_current_user_invalid_token(client: AsyncClient):
    """Test getting current user information with invalid token"""
    response = await client.get("/users/me", cookies={"access_token": "invalid_token"})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "detail" in response.json()


async def test_get_current_user_expired_token(client: AsyncClient):
    """Test getting current user information with expired token (simulation)"""
    # Use explicitly invalid token (assumed to be treated as "expired")
    expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwiZXhwIjo5NTgzOTI5NTh9.invalid_signature"

    response = await client.get("/users/me", cookies={"access_token": expired_token})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "detail" in response.json()
