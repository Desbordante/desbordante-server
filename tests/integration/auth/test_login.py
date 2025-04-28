from typing import Any, Dict

import pytest
from fastapi import status
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_login_success(client: AsyncClient, logged_in_user: Dict[str, Any]):
    """Test successful login"""
    response = await client.post(
        "/auth/login",
        data={"email": "test_user@example.com", "password": "StrongPassword123!"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert "user" in response.json()
    assert response.json()["user"]["email"] == logged_in_user["user"]["email"]

    # Check that cookies are set
    assert "access_token" in response.cookies
    assert "refresh_token" in response.cookies


async def test_login_wrong_email(client: AsyncClient, logged_in_user: Dict[str, Any]):
    """Test login with wrong email"""
    response = await client.post(
        "/auth/login",
        data={"email": "wrong_email@example.com", "password": "StrongPassword123!"},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "detail" in response.json()


async def test_login_wrong_password(
    client: AsyncClient, logged_in_user: Dict[str, Any]
):
    """Test login with wrong password"""
    response = await client.post(
        "/auth/login",
        data={"email": "test_user@example.com", "password": "WrongPassword123!"},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "detail" in response.json()


async def test_login_wrong_email_and_password_same_error(
    client: AsyncClient, logged_in_user: Dict[str, Any]
):
    """Test login with wrong email and password"""
    response = await client.post(
        "/auth/login",
        data={"email": "wrong_email@example.com", "password": "WrongPassword123!"},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    wrong_email_detail = response.json()["detail"]

    response = await client.post(
        "/auth/login",
        data={
            "email": logged_in_user["user"]["email"],
            "password": "WrongPassword123!",
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    wrong_password_detail = response.json()["detail"]

    assert wrong_email_detail == wrong_password_detail


async def test_login_invalid_data_format(client: AsyncClient):
    """Test login with invalid data format"""
    response = await client.post(
        "/auth/login",
        json={  # Sending JSON instead of form-data
            "email": "user@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
