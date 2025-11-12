import pytest
from faker import Faker
from fastapi import status
from httpx import AsyncClient
from pytest_mock import MockType

from tests.integration.auth.constants import SEND_RESET_EMAIL_ENDPOINT
from tests.integration.auth.types import RegisteredUserResponse

pytestmark = pytest.mark.asyncio


async def test_send_reset_email(
    client: AsyncClient,
    registered_user: RegisteredUserResponse,
    mock_send_reset_email: MockType,
):
    """Test successful send password reset email"""

    response = await client.post(
        SEND_RESET_EMAIL_ENDPOINT, data={"email": registered_user["user"]["email"]}
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT

    mock_send_reset_email.assert_called_once_with(
        to_email=registered_user["user"]["email"]
    )


async def test_send_reset_email_user_not_found(
    client: AsyncClient,
    faker: Faker,
    mock_send_reset_email: MockType,
):
    """Test send password reset email when user does not exist"""
    non_existent_email = faker.email()

    response = await client.post(
        SEND_RESET_EMAIL_ENDPOINT, data={"email": non_existent_email}
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert (
        response.json()["detail"] == f"User with email {non_existent_email} not found"
    )

    # Ensure email task was not called when user doesn't exist
    mock_send_reset_email.assert_not_called()


async def test_send_reset_email_invalid_email_format(
    client: AsyncClient,
    mock_send_reset_email: MockType,
):
    """Test send password reset email with invalid email format"""
    invalid_email = "invalid-email-format"

    response = await client.post(
        SEND_RESET_EMAIL_ENDPOINT, data={"email": invalid_email}
    )

    # FastAPI should return 422 for validation errors
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # Ensure email task was not called for invalid email
    mock_send_reset_email.assert_not_called()


async def test_send_reset_email_empty_email(
    client: AsyncClient,
    mock_send_reset_email: MockType,
):
    """Test send password reset email with empty email"""
    response = await client.post(SEND_RESET_EMAIL_ENDPOINT, data={"email": ""})

    # FastAPI should return 422 for validation errors
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # Ensure email task was not called for empty email
    mock_send_reset_email.assert_not_called()


async def test_send_reset_email_missing_email_field(
    client: AsyncClient,
    mock_send_reset_email: MockType,
):
    """Test send password reset email with missing email field"""
    response = await client.post(SEND_RESET_EMAIL_ENDPOINT, data={})

    # FastAPI should return 422 for missing required field
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # Ensure email task was not called when email field is missing
    mock_send_reset_email.assert_not_called()
