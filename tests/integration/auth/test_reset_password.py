from datetime import timedelta

import pytest
from faker import Faker
from fastapi import status
from httpx import AsyncClient

from src.domain.auth.config import settings
from src.domain.security.utils import create_token
from src.schemas.email_schemas import ResetPasswordTokenPayloadSchema
from tests.integration.auth.constants import RESET_PASSWORD_ENDPOINT
from tests.integration.auth.types import RegisteredUserResponse

pytestmark = pytest.mark.asyncio


async def test_reset_password(
    client: AsyncClient, registered_user: RegisteredUserResponse, faker: Faker
):
    """Test successful reset password"""
    token = create_token(
        schema=ResetPasswordTokenPayloadSchema,
        payload={"email": registered_user["user"]["email"]},
        expires_delta=timedelta(minutes=settings.RESET_PASSWORD_EMAIL_EXPIRE_MINUTES),
    ).token

    response = await client.put(
        RESET_PASSWORD_ENDPOINT,
        data={
            "new_password": faker.password(length=16, digits=True, special_chars=True)
        },
        params={"token": token},
    )

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert "user" in response.json()
    assert response.json()["user"]["email"] == registered_user["user"]["email"]

    # Check that cookies are set
    assert "access_token" in response.cookies
    assert "refresh_token" in response.cookies


async def test_reset_password_invalid_token(client: AsyncClient, faker: Faker):
    """Test reset password with invalid token"""
    invalid_token = "invalid-token-string"

    response = await client.put(
        RESET_PASSWORD_ENDPOINT,
        data={
            "new_password": faker.password(length=16, digits=True, special_chars=True)
        },
        params={"token": invalid_token},
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in response.json()


async def test_reset_password_expired_token(
    client: AsyncClient, registered_user: RegisteredUserResponse, faker: Faker
):
    """Test reset password with expired token"""
    # Create token with negative expiry (already expired)
    expired_token = create_token(
        schema=ResetPasswordTokenPayloadSchema,
        payload={"email": registered_user["user"]["email"]},
        expires_delta=timedelta(minutes=-1),  # Expired 1 minute ago
    ).token

    response = await client.put(
        RESET_PASSWORD_ENDPOINT,
        data={
            "new_password": faker.password(length=16, digits=True, special_chars=True)
        },
        params={"token": expired_token},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == "Token has expired"


async def test_reset_password_missing_token(client: AsyncClient, faker: Faker):
    """Test reset password without token parameter"""
    response = await client.put(
        RESET_PASSWORD_ENDPOINT,
        data={
            "new_password": faker.password(length=16, digits=True, special_chars=True)
        },
    )

    # FastAPI should return 422 for missing required query parameter
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_reset_password_weak_password(
    client: AsyncClient, registered_user: RegisteredUserResponse
):
    """Test reset password with weak password"""
    token = create_token(
        schema=ResetPasswordTokenPayloadSchema,
        payload={"email": registered_user["user"]["email"]},
        expires_delta=timedelta(minutes=settings.RESET_PASSWORD_EMAIL_EXPIRE_MINUTES),
    ).token

    # Test various weak passwords
    weak_passwords = [
        "123456",  # Too short, no letters
        "password",  # Common password, no digits/special chars
        "12345678",  # Only digits
        "abcdefgh",  # Only letters, no digits/special chars
        "Pass123",  # Less than 8 chars
    ]

    for weak_password in weak_passwords:
        response = await client.put(
            RESET_PASSWORD_ENDPOINT,
            data={"new_password": weak_password},
            params={"token": token},
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "detail" in response.json()


async def test_reset_password_user_not_found(client: AsyncClient, faker: Faker):
    """Test reset password when user from token doesn't exist"""
    non_existent_email = faker.email()

    token = create_token(
        schema=ResetPasswordTokenPayloadSchema,
        payload={"email": non_existent_email},
        expires_delta=timedelta(minutes=settings.RESET_PASSWORD_EMAIL_EXPIRE_MINUTES),
    ).token

    response = await client.put(
        RESET_PASSWORD_ENDPOINT,
        data={
            "new_password": faker.password(length=16, digits=True, special_chars=True)
        },
        params={"token": token},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_reset_password_missing_password(
    client: AsyncClient, registered_user: RegisteredUserResponse
):
    """Test reset password without new_password field"""
    token = create_token(
        schema=ResetPasswordTokenPayloadSchema,
        payload={"email": registered_user["user"]["email"]},
        expires_delta=timedelta(minutes=settings.RESET_PASSWORD_EMAIL_EXPIRE_MINUTES),
    ).token

    response = await client.put(
        RESET_PASSWORD_ENDPOINT,
        data={},  # Missing new_password field
        params={"token": token},
    )

    # FastAPI should return 422 for missing required field
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_reset_password_empty_password(
    client: AsyncClient, registered_user: RegisteredUserResponse
):
    """Test reset password with empty password"""
    token = create_token(
        schema=ResetPasswordTokenPayloadSchema,
        payload={"email": registered_user["user"]["email"]},
        expires_delta=timedelta(minutes=settings.RESET_PASSWORD_EMAIL_EXPIRE_MINUTES),
    ).token

    response = await client.put(
        RESET_PASSWORD_ENDPOINT,
        data={"new_password": ""},
        params={"token": token},
    )

    # Should return 422 for validation error (empty password)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
