import logging
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from fakeredis import FakeAsyncRedis
from httpx import ASGITransport, AsyncClient
from moto.server import ThreadedMotoServer
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    AsyncTransaction,
    create_async_engine,
)

from src.api.dependencies import get_redis, get_storage
from src.db.config import settings
from src.db.session import get_session
from src.infrastructure.session.manager import SessionManager
from src.infrastructure.storage.client import S3Storage
from src.main import app
from tests.integration.storage.constants import TEST_BUCKET

logger = logging.getLogger(__name__)

engine = create_async_engine(settings.postgres_dsn.unicode_string(), poolclass=NullPool)


@pytest.fixture(scope="function")
def moto_server():
    """Start moto S3 mock server. State is cleared when server stops."""
    server = ThreadedMotoServer(port=0)
    try:
        server.start()
        host, port = server.get_host_and_port()
        yield f"http://{host}:{port}"
    finally:
        server.stop()


@pytest_asyncio.fixture(scope="function")
async def s3_storage(moto_server: str) -> S3Storage:
    """S3 storage using moto mock server. No cleanup needed — server state is fresh per test."""
    storage = S3Storage(
        endpoint_url=moto_server,
        access_key="testing",
        secret_key="testing",
        bucket=TEST_BUCKET,
    )
    async with storage.get_client() as client:
        await client.create_bucket(Bucket=TEST_BUCKET)
    return storage


@pytest_asyncio.fixture(scope="function")
async def redis() -> AsyncGenerator[FakeAsyncRedis, None]:
    client = FakeAsyncRedis(decode_responses=True)
    yield client
    await client.aclose()


@pytest_asyncio.fixture(scope="function")
async def session_manager(redis: FakeAsyncRedis) -> SessionManager:
    return SessionManager(redis)


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
        expire_on_commit=False,
    )
    async with async_session:
        yield async_session

    await transaction.rollback()


@pytest_asyncio.fixture(scope="function")
async def client() -> AsyncGenerator[AsyncClient, None]:
    yield AsyncClient(base_url="http://test", transport=ASGITransport(app=app))


@pytest.fixture(autouse=True)
def apply_dependency_overrides(
    session: AsyncSession,
    s3_storage: S3Storage,
    redis: FakeAsyncRedis,
) -> Generator[None, None, None]:
    app.dependency_overrides[get_session] = lambda: session
    app.dependency_overrides[get_storage] = lambda: s3_storage
    app.dependency_overrides[get_redis] = lambda: redis

    yield

    app.dependency_overrides.pop(get_session, None)
    app.dependency_overrides.pop(get_storage, None)
    app.dependency_overrides.pop(get_redis, None)
