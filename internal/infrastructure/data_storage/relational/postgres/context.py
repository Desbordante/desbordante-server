from sqlalchemy import create_engine, NullPool
from sqlalchemy.orm import sessionmaker, Session

from internal.infrastructure.data_storage import settings

default_engine = create_engine(url=settings.postgres_dsn.unicode_string())
engine_without_pool = create_engine(
    url=settings.postgres_dsn.unicode_string(),
    poolclass=NullPool,
)

type PostgresContextType = Session
type PostgresContextMakerType = sessionmaker[Session]
PostgresContextMaker = sessionmaker(bind=default_engine)
PostgresContextMakerWithoutPool = sessionmaker(bind=engine_without_pool)


def get_postgres_context() -> PostgresContextType:
    return PostgresContextMaker()


def get_postgres_context_without_pool() -> PostgresContextType:
    return PostgresContextMakerWithoutPool()


def get_postgres_context_maker() -> PostgresContextMakerType:
    return PostgresContextMaker


def get_postgres_context_maker_without_pool() -> PostgresContextMakerType:
    return PostgresContextMakerWithoutPool
