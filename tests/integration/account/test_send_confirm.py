from typing import Any, Dict

import pytest
from fastapi import status
from httpx import AsyncClient
from pytest_mock import MockType

pytestmark = pytest.mark.asyncio


async def test_confirm_email_success(
    client: AsyncClient,
    logged_in_user: Dict[str, Any],
    mock_send_confirmation_email: MockType,
):
    """Test successful send confirmation email"""
    mock_send_confirmation_email.assert_called_once_with(
        to_email=logged_in_user["user"]["email"]
    )

    access_token = logged_in_user["access_token"]
    client.cookies.set("access_token", access_token)

    response = await client.post("/account/confirm")

    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert mock_send_confirmation_email.call_count == 2
    mock_send_confirmation_email.assert_called_with(
        to_email=logged_in_user["user"]["email"]
    )
