import logging
from typing import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    AsyncTransaction,
    create_async_engine,
)

from src.db.config import settings
from src.db.session import get_session
from src.main import app

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
    app.dependency_overrides[get_session] = lambda: session

    yield AsyncClient(base_url="http://test", transport=ASGITransport(app=app))

    app.dependency_overrides = {}
