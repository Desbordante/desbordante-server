import logging
from typing import Any, AsyncGenerator, Dict

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from pytest_mock import MockerFixture, MockType
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    AsyncTransaction,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from src.crud.user_crud import UserCrud
from src.db.config import settings
from src.db.session import get_session
from src.usecases.auth.create_tokens import CreateTokensUseCase
from src.usecases.auth.register_user import RegisterUserUseCase

logger = logging.getLogger(__name__)

engine = create_async_engine(settings.postgres_dsn.unicode_string(), poolclass=NullPool)


@pytest_asyncio.fixture(scope="function")
async def connection():
    async with engine.connect() as connection:
        yield connection


@pytest_asyncio.fixture(scope="function")
async def transaction(
    connection: AsyncConnection,
) -> AsyncGenerator[AsyncTransaction, None]:
    async with connection.begin() as transaction:
        yield transaction


@pytest_asyncio.fixture(scope="function")
async def session(
    connection: AsyncConnection, transaction: AsyncTransaction
) -> AsyncGenerator[AsyncSession, None]:
    async_session = AsyncSession(
        bind=connection,
        join_transaction_mode="create_savepoint",
    )
    async with async_session:
        yield async_session

    await transaction.rollback()


@pytest_asyncio.fixture(scope="function")
async def client(session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    from src.main import app

    app.dependency_overrides[get_session] = lambda: session
    yield AsyncClient(base_url="http://test", transport=ASGITransport(app=app))
    del app.dependency_overrides[get_session]


@pytest_asyncio.fixture(scope="function")
async def user_crud(session: AsyncSession) -> UserCrud:
    return UserCrud(session=session)


@pytest_asyncio.fixture(scope="function")
async def register_user_use_case(user_crud: UserCrud) -> RegisterUserUseCase:
    return RegisterUserUseCase(user_crud=user_crud)


@pytest_asyncio.fixture(scope="function")
async def create_tokens_use_case() -> CreateTokensUseCase:
    return CreateTokensUseCase()


@pytest.fixture(scope="session")
def celery_config():
    return {
        "broker_url": "memory://",
        "result_backend": "rpc://",
        "task_always_eager": True,  # Tasks will be executed locally instead of being sent to the queue
        "task_eager_propagates": True,  # Propagate exceptions in eager mode
    }


@pytest.fixture(scope="session")
def celery_includes():
    return ["src.domain.account.tasks"]


@pytest.fixture(autouse=True)
def mock_smtp(mocker: MockerFixture) -> MockType:
    """
    Mock for SMTP, automatically applied to all tests in this module.
    Uses pytest-mock's mocker fixture for cleaner mocking.
    """
    smtp_mock = mocker.patch("src.domain.account.tasks.smtplib.SMTP_SSL")
    mock_smtp_instance = mocker.MagicMock(
        name="src.domain.account.tasks.smtplib.SMTP_SSL"
    )
    smtp_mock.return_value.__enter__.return_value = mock_smtp_instance
    return mock_smtp_instance


@pytest.fixture(autouse=True)
def mock_send_confirmation_email(mocker: MockerFixture):
    return mocker.patch("src.domain.account.tasks.send_confirmation_email.delay")


@pytest_asyncio.fixture(scope="function")
async def logged_in_user(
    client: AsyncClient,
) -> Dict[str, Any]:
    """Create a logged-in user and return user data with tokens"""
    # Register a user
    response = await client.post(
        "/auth/register",
        data={
            "email": "test_user@example.com",
            "password": "StrongPassword123!",
            "full_name": "Test User",
            "country": "Test Country",
            "company": "Test Company",
            "occupation": "Test Occupation",
        },
    )
    assert response.status_code == 201

    # Save tokens and user data
    access_token = response.json()["access_token"]
    refresh_token = response.cookies.get("refresh_token")
    user = response.json()["user"]

    return {"user": user, "access_token": access_token, "refresh_token": refresh_token}
