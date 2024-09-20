import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
import logging

from internal.infrastructure.data_storage.relational.model import ORMBaseModel
from internal.infrastructure.data_storage import settings

# https://stackoverflow.com/questions/61582142/test-pydantic-settings-in-fastapi
# Maybe should be overriden by env vars for testing only
settings.postgres_db = "desbordante-test"

test_engine = create_engine(settings.postgres_dsn.unicode_string())


@pytest.fixture(scope="session", autouse=True)
def prepare_postgres():
    logging.info("Setup database: %s", settings.postgres_dsn.unicode_string())
    if not database_exists(settings.postgres_dsn.unicode_string()):
        create_database(settings.postgres_dsn.unicode_string())
    ORMBaseModel.metadata.drop_all(bind=test_engine)
    ORMBaseModel.metadata.create_all(bind=test_engine)


@pytest.fixture(scope="session")
def postgres_context_maker():
    return sessionmaker(test_engine, expire_on_commit=False)


@pytest.fixture(scope="function")
def postgres_context(postgres_context_maker):
    context = postgres_context_maker()

    yield context

    context.close()


@pytest.fixture(autouse=True)
def clean_tables(session):
    for table in reversed(ORMBaseModel.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()
