import pytest
from faker import Faker
from fastapi import status
from httpx import AsyncClient

from tests.integration.auth.constants import LOGIN_ENDPOINT
from tests.integration.auth.types import LoginUserData, RegisteredUserResponse

pytestmark = pytest.mark.asyncio


async def test_login(
    client: AsyncClient,
    registered_user: RegisteredUserResponse,
    login_data: LoginUserData,
):
    """Test successful login"""
    response = await client.post(
        LOGIN_ENDPOINT,
        data=login_data,
    )

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert "user" in response.json()
    assert response.json()["user"]["email"] == registered_user["user"]["email"]

    # Check that cookies are set
    assert "access_token" in response.cookies
    assert "refresh_token" in response.cookies


async def test_login_wrong_email(
    client: AsyncClient,
    registered_user: RegisteredUserResponse,
    login_data: LoginUserData,
    faker: Faker,
):
    """Test login with wrong email"""
    response = await client.post(
        LOGIN_ENDPOINT,
        data={**login_data, "email": faker.email()},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "detail" in response.json()


async def test_login_wrong_password(
    client: AsyncClient,
    registered_user: RegisteredUserResponse,
    login_data: LoginUserData,
    faker: Faker,
):
    """Test login with wrong password"""
    response = await client.post(
        LOGIN_ENDPOINT,
        data={
            **login_data,
            "password": faker.password(length=16, digits=True, special_chars=True),
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "detail" in response.json()


async def test_login_wrong_email_and_password_same_error(
    client: AsyncClient,
    registered_user: RegisteredUserResponse,
    login_data: LoginUserData,
    faker: Faker,
):
    """Test login with wrong email and password"""
    response = await client.post(
        LOGIN_ENDPOINT,
        data={
            **login_data,
            "email": faker.email(),
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    wrong_email_detail = response.json()["detail"]

    response = await client.post(
        LOGIN_ENDPOINT,
        data={
            "email": registered_user["user"]["email"],
            "password": faker.password(length=16, digits=True, special_chars=True),
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    wrong_password_detail = response.json()["detail"]

    assert wrong_email_detail == wrong_password_detail
