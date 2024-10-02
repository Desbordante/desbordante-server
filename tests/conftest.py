import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
import logging

from internal.infrastructure.data_storage.relational.model import ORMBaseModel
from internal.infrastructure.data_storage import settings, ContextMaker
from internal.infrastructure.data_storage.flat import get_flat_context_maker

# https://stackoverflow.com/questions/61582142/test-pydantic-settings-in-fastapi
# Maybe should be overriden by env vars for testing only
settings.postgres_db = "desbordante-test"

test_engine = create_engine(settings.postgres_dsn.unicode_string())


@pytest.fixture
def tmp_upload_dir(tmp_path):
    return tmp_path


@pytest.fixture(scope="session", autouse=True)
def prepare_postgres():
    logging.info("Setup database: %s", settings.postgres_dsn.unicode_string())
    if not database_exists(settings.postgres_dsn.unicode_string()):
        create_database(settings.postgres_dsn.unicode_string())
    ORMBaseModel.metadata.drop_all(bind=test_engine)
    ORMBaseModel.metadata.create_all(bind=test_engine)


@pytest.fixture(scope="function")
def postgres_context_maker():
    return sessionmaker(bind=test_engine)


@pytest.fixture(scope="function")
def postgres_context(postgres_context_maker):
    return postgres_context_maker()


@pytest.fixture(scope="function")
def flat_context_maker(tmp_upload_dir):
    return get_flat_context_maker(uploaded_files_dir_path=tmp_upload_dir)


@pytest.fixture
def flat_context(flat_context_maker):
    return flat_context_maker()


@pytest.fixture(scope="function")
def context_maker(postgres_context_maker, flat_context_maker):
    context_maker = ContextMaker(
        postgres_context_maker=postgres_context_maker,
        flat_context_maker=flat_context_maker,
    )
    return context_maker


@pytest.fixture(scope="function")
def context(context_maker):
    context = context_maker()

    yield context

    context.close()


@pytest.fixture(autouse=True)
def clean_tables(postgres_context):
    for table in reversed(ORMBaseModel.metadata.sorted_tables):
        postgres_context.execute(table.delete())
    postgres_context.commit()
