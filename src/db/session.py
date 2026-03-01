from typing import AsyncIterator

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.db.config import settings

engine = create_async_engine(settings.postgres_dsn.unicode_string(), echo=True)
engine_without_pool = create_async_engine(
    url=settings.postgres_dsn.unicode_string(),
    poolclass=NullPool,
)

async_session_factory = async_sessionmaker(engine, expire_on_commit=False)
async_session_factory_without_pool = async_sessionmaker(
    engine_without_pool, expire_on_commit=False
)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with async_session_factory() as session:
        yield session
