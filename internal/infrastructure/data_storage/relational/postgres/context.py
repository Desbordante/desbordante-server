from sqlalchemy import create_engine, NullPool
from sqlalchemy.orm import sessionmaker, Session

from internal.infrastructure.data_storage import settings

default_engine = create_engine(url=settings.postgres_dsn.unicode_string())
engine_without_pool = create_engine(
    url=settings.postgres_dsn.unicode_string(),
    poolclass=NullPool,
)

PostgresContextType = Session
PostgresContextMaker = sessionmaker(bind=default_engine)
PostgresContextMakerWithoutPool = sessionmaker(bind=engine_without_pool)


def get_postgres_context_maker() -> PostgresContextMaker:
    return PostgresContextMaker


def get_postgres_context_maker_without_pool() -> PostgresContextMakerWithoutPool:
    return PostgresContextMakerWithoutPool
