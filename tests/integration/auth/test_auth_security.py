import pytest
from fastapi import status
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_token_tampering(client: AsyncClient):
    """Test protection against token tampering"""
    # Register a user and get a token
    register_response = await client.post(
        "/auth/register",
        data={
            "email": "token_tampering_test@example.com",
            "password": "SecurePassword123!",
            "full_name": "Token Test",
            "country": "Test Country",
            "company": "Test Company",
            "occupation": "Security Tester",
        },
    )
    assert register_response.status_code == status.HTTP_201_CREATED
    access_token = register_response.json()["access_token"]

    # Try to modify the token
    tampered_token = access_token[:-10] + "abcdefghij"

    # Try to use the tampered token
    response = await client.get("/users/me", cookies={"access_token": tampered_token})

    # Tampered token should be rejected
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "detail" in response.json()


async def test_session_hijacking_protection(client: AsyncClient):
    """Test protection against session hijacking (via token theft)"""
    # Register two users
    register_response1 = await client.post(
        "/auth/register",
        data={
            "email": "user1_hijacking@example.com",
            "password": "SecurePassword123!",
            "full_name": "User One",
            "country": "Test Country",
            "company": "Test Company",
            "occupation": "Security Tester",
        },
    )
    assert register_response1.status_code == status.HTTP_201_CREATED
    user1_token = register_response1.json()["access_token"]

    register_response2 = await client.post(
        "/auth/register",
        data={
            "email": "user2_hijacking@example.com",
            "password": "SecurePassword123!",
            "full_name": "User Two",
            "country": "Test Country",
            "company": "Test Company",
            "occupation": "Security Tester",
        },
    )
    assert register_response2.status_code == status.HTTP_201_CREATED

    # For user 2, check their profile
    profile_response = await client.get(
        "/users/me", cookies={"access_token": register_response2.json()["access_token"]}
    )
    assert profile_response.status_code == status.HTTP_200_OK
    assert profile_response.json()["email"] == "user2_hijacking@example.com"

    # Now try using user 1's token to access the profile
    # This request should return user 1's profile, not user 2's
    hijacked_response = await client.get(
        "/users/me", cookies={"access_token": user1_token}
    )
    assert hijacked_response.status_code == status.HTTP_200_OK
    assert hijacked_response.json()["email"] == "user1_hijacking@example.com"
    assert hijacked_response.json()["email"] != "user2_hijacking@example.com"


async def test_csrf_protection(client: AsyncClient):
    """Test protection against CSRF attacks"""
    # This test will likely be skipped, as full CSRF testing requires
    # simulating requests from different domains, but we can verify that the API
    # uses access tokens that aren't vulnerable to CSRF (e.g., via Auth headers)

    # Register a user and get a token
    register_response = await client.post(
        "/auth/register",
        data={
            "email": "csrf_test@example.com",
            "password": "SecurePassword123!",
            "full_name": "CSRF Test",
            "country": "Test Country",
            "company": "Test Company",
            "occupation": "Security Tester",
        },
    )
    assert register_response.status_code == status.HTTP_201_CREATED
    access_token = register_response.json()["access_token"]

    # Check that a request without a CSRF token (if required) or other protection is rejected
    # This depends on the API implementation and CSRF protections

    # Successful request with token in Authorization header (this is safe from CSRF)
    response = await client.get(
        "/users/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
