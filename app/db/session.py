from contextlib import contextmanager
import datetime
from typing import Generator
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from app.settings import settings
from sqlalchemy.pool import NullPool
from sqlalchemy_mixins import AllFeaturesMixin
from sqlalchemy_mixins.timestamp import TimestampsMixin
from sqlalchemy_mixins.eagerload import EagerLoadMixin
from sqlalchemy.orm import DeclarativeBase


class ORMBase(AllFeaturesMixin, TimestampsMixin, EagerLoadMixin, DeclarativeBase):
    __abstract__ = True


class ORMBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    created_at: datetime.datetime
    updated_at: datetime.datetime


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


# Default session with pooling
with get_session() as session:
    ORMBase.set_session(session)


@contextmanager
def no_pooling() -> Generator[None, None, None]:
    """
    Operations without pooling in contextmanager scoupe
    Example:

    # operations with pooling
    with no_pooling():
        # operations WITHOUT pooling
    # operations with pooling
    """
    old_session = ORMBase.session
    with get_session(with_pool=False) as session:
        ORMBase.set_session(session)
        yield
    ORMBase.set_session(old_session)
