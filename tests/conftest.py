import logging
from typing import Any, AsyncGenerator, Dict

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
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
