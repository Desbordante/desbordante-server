import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
import logging

from app.db import ORMBase
from app.settings import settings

# https://stackoverflow.com/questions/61582142/test-pydantic-settings-in-fastapi
# Maybe should be overriden by env vars for testing only
settings.postgres_db = "desbordante-test"

test_engine = create_engine(settings.postgres_dsn.unicode_string())


@pytest.fixture(scope="session", autouse=True)
def prepare_db():
    logging.info("Setup database: %s", settings.postgres_dsn.unicode_string())
    if not database_exists(settings.postgres_dsn.unicode_string()):
        create_database(settings.postgres_dsn.unicode_string())
    ORMBase.metadata.drop_all(bind=test_engine)
    ORMBase.metadata.create_all(bind=test_engine)


@pytest.fixture(scope="session", autouse=True)
def session():
    session = sessionmaker(test_engine, expire_on_commit=False)
    yield session
