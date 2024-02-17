import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from app.db import Base
from app.settings import get_settings


test_settings = get_settings()
test_settings.postgres_db = "desbordante-test"

test_engine = create_engine(test_settings.postgres_dsn.unicode_string())


@pytest.fixture(scope="session", autouse=True)
def prepare_db():
    if not database_exists(test_settings.postgres_dsn.unicode_string()):
        create_database(test_settings.postgres_dsn.unicode_string())
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)


@pytest.fixture(scope="session", autouse=True)
def session():
    session = sessionmaker(test_engine, expire_on_commit=False)
    yield session
