import logging

import pytest
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy_utils import create_database, database_exists, drop_database
from starlette.config import environ

from src.db.config import settings
from src.db.session import get_session
from src.models.base_models import BaseModel

logger = logging.getLogger(__name__)

environ["POSTGRES_DB"] = "desbordante-test"


@pytest.fixture(scope="session")
def db_engine():
    engine = create_async_engine(settings.postgres_dsn.unicode_string())
    yield engine
    engine.sync_engine.dispose()


@pytest.fixture(scope="session")
async def create_db(db_engine: AsyncEngine):
    logger.info("Setup database: %s", settings.postgres_dsn.unicode_string())
    if database_exists(settings.postgres_dsn.unicode_string()):
        drop_database(settings.postgres_dsn.unicode_string())

    create_database(settings.postgres_dsn.unicode_string())

    async with db_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
    yield
    async with db_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)

    logger.info("Drop database: %s", settings.postgres_dsn.unicode_string())
    drop_database(settings.postgres_dsn.unicode_string())


@pytest.fixture(scope="session")
async def session(db_engine: AsyncEngine, create_db: None):
    async_session_factory = async_sessionmaker(db_engine, expire_on_commit=False)
    async with async_session_factory() as session:
        yield session


@pytest.fixture(scope="session")
def client(session: AsyncSession):
    from fastapi.testclient import TestClient

    from src.main import app

    app.dependency_overrides[get_session] = lambda: session

    return TestClient(app)
