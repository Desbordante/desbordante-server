import pytest
from fastapi import status
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_register_success(client: AsyncClient):
    """Test successful user registration"""
    response = await client.post(
        "/auth/register",
        data={
            "email": "new_user@example.com",
            "password": "StrongPassword123!",
            "full_name": "New User",
            "country": "Test Country",
            "company": "Test Company",
            "occupation": "Software Developer",
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert "access_token" in response.json()
    assert "user" in response.json()
    assert response.json()["user"]["email"] == "new_user@example.com"

    # Check that cookies are set
    assert "access_token" in response.cookies
    assert "refresh_token" in response.cookies


async def test_register_email_already_exists(client: AsyncClient):
    """Test registration with an already existing email"""
    # First register a user
    await client.post(
        "/auth/register",
        data={
            "email": "existing_user@example.com",
            "password": "StrongPassword123!",
            "full_name": "Existing User",
            "country": "Test Country",
            "company": "Test Company",
            "occupation": "Test Occupation",
        },
    )

    # Try to register again with the same email
    response = await client.post(
        "/auth/register",
        data={
            "email": "existing_user@example.com",
            "password": "AnotherPassword123!",
            "full_name": "Another User",
            "country": "Another Country",
            "company": "Another Company",
            "occupation": "Another Occupation",
        },
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert "detail" in response.json()


async def test_register_invalid_email(client: AsyncClient):
    """Test registration with an invalid email"""
    response = await client.post(
        "/auth/register",
        data={
            "email": "invalid-email",
            "password": "StrongPassword123!",
            "full_name": "Invalid Email User",
            "country": "Test Country",
            "company": "Test Company",
            "occupation": "Test Occupation",
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_register_weak_password(client: AsyncClient):
    """Test registration with a weak password"""
    response = await client.post(
        "/auth/register",
        data={
            "email": "weak_password@example.com",
            "password": "weak",
            "full_name": "Weak Password User",
            "country": "Test Country",
            "company": "Test Company",
            "occupation": "Test Occupation",
        },
    )

    # Server should validate password strength
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_register_missing_required_fields(client: AsyncClient):
    """Test registration with missing required fields"""
    response = await client.post(
        "/auth/register",
        data={
            "email": "missing_fields@example.com",
            "password": "StrongPassword123!",
            # Missing full_name, country, company, occupation
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
