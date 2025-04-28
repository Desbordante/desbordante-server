import asyncio

import pytest
from fastapi import status
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_complete_auth_flow(client: AsyncClient):
    """Test complete authentication flow: register, login, refresh token, check profile and logout"""

    # 1. Register a new user
    register_response = await client.post(
        "/auth/register",
        data={
            "email": "flow_test_user@example.com",
            "password": "StrongPassword123!",
            "full_name": "Flow Test User",
            "country": "Test Country",
            "company": "Test Company",
            "occupation": "Tester",
        },
    )
    assert register_response.status_code == status.HTTP_201_CREATED
    user_data = register_response.json()["user"]

    # Save tokens
    access_token = register_response.json()["access_token"]
    refresh_token = register_response.cookies["refresh_token"]

    # 2. Logout
    logout_response = await client.post(
        "/auth/logout",
        cookies={"access_token": access_token, "refresh_token": refresh_token},
    )
    assert logout_response.status_code == status.HTTP_204_NO_CONTENT

    await asyncio.sleep(1)

    # 3. Login back
    login_response = await client.post(
        "/auth/login",
        data={"email": "flow_test_user@example.com", "password": "StrongPassword123!"},
    )
    assert login_response.status_code == status.HTTP_200_OK

    # Get new tokens
    new_access_token = login_response.json()["access_token"]
    new_refresh_token = login_response.cookies["refresh_token"]

    # Verify tokens have changed
    assert new_access_token != access_token

    # 4. Check user profile with new token
    profile_response = await client.get(
        "/users/me", cookies={"access_token": new_access_token}
    )
    assert profile_response.status_code == status.HTTP_200_OK
    assert profile_response.json()["email"] == user_data["email"]

    await asyncio.sleep(1)

    # 5. Refresh token
    refresh_response = await client.post(
        "/auth/refresh", cookies={"refresh_token": new_refresh_token}
    )
    assert refresh_response.status_code == status.HTTP_200_OK

    # Get refreshed tokens
    refreshed_access_token = refresh_response.json()["access_token"]
    refreshed_refresh_token = refresh_response.cookies["refresh_token"]

    # Verify tokens have changed
    assert refreshed_access_token != new_access_token

    # 6. Check user profile with refreshed token
    new_profile_response = await client.get(
        "/users/me", cookies={"access_token": refreshed_access_token}
    )
    assert new_profile_response.status_code == status.HTTP_200_OK
    assert new_profile_response.json()["email"] == user_data["email"]

    # 7. Final logout
    final_logout_response = await client.post(
        "/auth/logout",
        cookies={
            "access_token": refreshed_access_token,
            "refresh_token": refreshed_refresh_token,
        },
    )
    assert final_logout_response.status_code == status.HTTP_204_NO_CONTENT

    # 8. Verify access is now forbidden
    final_profile_response = await client.get("/users/me")
    assert final_profile_response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_token_precedence(client: AsyncClient):
    """Test token precedence from different sources"""
    # Register a user
    register_response = await client.post(
        "/auth/register",
        data={
            "email": "precedence_test@example.com",
            "password": "StrongPassword123!",
            "full_name": "Precedence Test User",
            "country": "Test Country",
            "company": "Test Company",
            "occupation": "Tester",
        },
    )
    assert register_response.status_code == status.HTTP_201_CREATED

    access_token = register_response.json()["access_token"]

    # Test precedence: header should take precedence over cookie
    # Send request with different tokens in different places
    response = await client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
        cookies={"access_token": "invalid token"},
    )

    assert response.status_code == status.HTTP_200_OK
