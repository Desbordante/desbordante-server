import pytest
import pytest_asyncio
from faker import Faker
from fastapi import status
from httpx import AsyncClient
from pytest_mock import MockerFixture

from tests.integration.auth.constants import REGISTER_ENDPOINT
from tests.integration.auth.types import (
    LoginUserData,
    RegisteredUserResponse,
    RegisterUserData,
)


@pytest.fixture(autouse=True)
def mock_send_confirmation_email(mocker: MockerFixture):
    return mocker.patch("src.domain.account.tasks.send_confirmation_email.delay")


@pytest.fixture(autouse=True)
def mock_send_reset_email(mocker: MockerFixture):
    return mocker.patch("src.domain.auth.tasks.send_reset_email.delay")


@pytest.fixture(scope="function")
def register_data(faker: Faker) -> RegisterUserData:
    return {
        "email": faker.email(),
        "password": faker.password(length=16, digits=True, special_chars=True),
        "full_name": faker.name(),
        "country": faker.country(),
        "company": faker.company(),
        "occupation": faker.job(),
    }


@pytest.fixture(scope="function")
def login_data(register_data: RegisterUserData) -> LoginUserData:
    return {
        "email": register_data["email"],
        "password": register_data["password"],
    }


@pytest_asyncio.fixture(scope="function")
async def registered_user(
    client: AsyncClient,
    register_data: RegisterUserData,
) -> RegisteredUserResponse:
    response = await client.post(
        REGISTER_ENDPOINT,
        data=register_data,
    )
    assert response.status_code == status.HTTP_201_CREATED

    # Save tokens and user data
    access_token = response.json()["access_token"]
    refresh_token = response.cookies.get("refresh_token")
    assert refresh_token is not None
    user = response.json()["user"]

    return {
        "user": user,
        "access_token": access_token,
        "refresh_token": refresh_token,
    }
