import pytest
from faker import Faker
from fastapi import status
from httpx import AsyncClient
from pytest_mock import MockType

from tests.integration.auth.constants import REGISTER_ENDPOINT
from tests.integration.auth.types import RegisteredUserResponse, RegisterUserData

pytestmark = pytest.mark.asyncio


async def test_register(
    client: AsyncClient,
    mock_send_confirmation_email: MockType,
    register_data: RegisterUserData,
):
    """Test successful user registration"""

    response = await client.post(
        REGISTER_ENDPOINT,
        data=register_data,
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert "access_token" in response.json()
    assert "refresh_token" not in response.json()
    assert "user" in response.json()

    # Check that the user is created with the correct data
    for key, value in register_data.items():
        if key != "password":
            assert response.json()["user"][key] == value

    # Check that cookies are set
    assert "access_token" in response.cookies
    assert "refresh_token" in response.cookies

    mock_send_confirmation_email.assert_called_once_with(
        to_email=register_data["email"]
    )


async def test_register_email_already_exists(
    client: AsyncClient, registered_user: RegisteredUserResponse, faker: Faker
):
    """Test registration with an already existing email"""

    # Try to register again with the same email
    response = await client.post(
        REGISTER_ENDPOINT,
        data={
            **registered_user["user"],
            "password": faker.password(length=16, digits=True, special_chars=True),
        },
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert "detail" in response.json()


async def test_register_invalid_email(
    client: AsyncClient, register_data: RegisterUserData
):
    """Test registration with an invalid email"""
    response = await client.post(
        REGISTER_ENDPOINT,
        data={**register_data, "email": "invalid-email"},
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_register_weak_password(
    client: AsyncClient, register_data: RegisterUserData, faker: Faker
):
    """Test registration with a weak password"""
    response = await client.post(
        REGISTER_ENDPOINT,
        data={
            **register_data,
            "password": faker.password(length=7, digits=False, special_chars=False),
        },
    )

    # Server should validate password strength
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_register_missing_required_fields(
    client: AsyncClient, register_data: RegisterUserData
):
    """Test registration with missing required fields"""
    data = {**register_data}
    del data["full_name"]
    del data["country"]
    del data["company"]
    del data["occupation"]

    response = await client.post(
        REGISTER_ENDPOINT,
        data=data,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
