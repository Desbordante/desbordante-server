from asyncio import current_task
from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from src.db.config import settings

engine = create_async_engine(settings.postgres_dsn.unicode_string(), echo=True)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with async_session_factory() as session:
        yield session


@asynccontextmanager
async def scoped_session() -> AsyncIterator[AsyncSession]:
    scoped_factory = async_scoped_session(async_session_factory, scopefunc=current_task)
    try:
        async with scoped_factory() as session:
            yield session
    finally:
        await scoped_factory.remove()
