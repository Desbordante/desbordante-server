from contextlib import contextmanager
from typing import Generator
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from app.settings import settings
from sqlalchemy.pool import NullPool

default_engine = create_engine(url=settings.postgres_dsn.unicode_string())
engine_without_pool = create_engine(
    url=settings.postgres_dsn.unicode_string(),
    poolclass=NullPool,
)

SessionLocal = sessionmaker(bind=default_engine)
SessionLocalWithoutPool = sessionmaker(bind=engine_without_pool)


@contextmanager
def get_session(with_pool=True) -> Generator[Session, None, None]:
    """
    Returns a generator that yields a session object for database operations.

    Parameters:
    with_pool (bool): A flag to determine if the session uses a connection pool.
                      Set to False when used in a Celery task. Defaults to True.
    """
    maker = SessionLocal if with_pool else SessionLocalWithoutPool
    with maker() as session:
        yield session
