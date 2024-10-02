import pytest
import shutil
from sqlalchemy import create_engine, NullPool
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
import logging

from internal.infrastructure.data_storage.relational.model import ORMBaseModel
from internal.infrastructure.data_storage import settings, ContextMaker
from internal.infrastructure.data_storage.flat import get_flat_context_maker
from internal.repository.flat import FileRepository
from internal.repository.relational.file import (
    FileMetadataRepository,
    DatasetRepository,
)
from internal.repository.relational.task import TaskRepository
from internal.worker.celery import ProfilingTaskWorker
from internal.usecase.file import (
    SaveFile,
    SaveDataset,
    CheckContentType,
    RetrieveDataset,
)
from internal.usecase.task import RetrieveTask, SetTask, ProfileTask, UpdateTaskInfo
from internal.uow import UnitOfWork

from internal.rest.http.file.di import (
    get_save_file_use_case,
    get_save_dataset_use_case,
    get_check_content_type_use_case,
    get_retrieve_dataset_use_case,
)
from internal.rest.http.task.di import get_set_task_use_case, get_retrieve_task_use_case

# https://stackoverflow.com/questions/61582142/test-pydantic-settings-in-fastapi
# Maybe should be overriden by env vars for testing only
settings.postgres_db = "desbordante-test"

test_engine = create_engine(settings.postgres_dsn.unicode_string())
test_engine_without_pool = create_engine(
    settings.postgres_dsn.unicode_string(), poolclass=NullPool
)


@pytest.fixture(scope="session", autouse=True)
def prepare_postgres():
    logging.info("Setup database: %s", settings.postgres_dsn.unicode_string())
    if not database_exists(settings.postgres_dsn.unicode_string()):
        create_database(settings.postgres_dsn.unicode_string())
    ORMBaseModel.metadata.drop_all(bind=test_engine)
    ORMBaseModel.metadata.create_all(bind=test_engine)


@pytest.fixture(scope="session")
def tmp_upload_dir(tmp_path_factory):
    temp_dir = tmp_path_factory.mktemp("uploads")

    yield temp_dir

    shutil.rmtree(temp_dir)


@pytest.fixture(scope="session")
def postgres_context_maker():
    return sessionmaker(bind=test_engine)


@pytest.fixture(scope="function")
def postgres_context(postgres_context_maker):
    return postgres_context_maker()


@pytest.fixture(scope="session")
def postgres_context_maker_without_pool():
    return sessionmaker(bind=test_engine_without_pool)


@pytest.fixture(scope="function")
def postgres_context_without_pool(postgres_context_maker_without_pool):
    return postgres_context_maker_without_pool()


@pytest.fixture(scope="session")
def flat_context_maker(tmp_upload_dir):
    return get_flat_context_maker(uploaded_files_dir_path=tmp_upload_dir)


@pytest.fixture(scope="function")
def flat_context(flat_context_maker):
    return flat_context_maker()


@pytest.fixture(
    scope="session",
)
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


@pytest.fixture(scope="session")
def context_maker_without_pool(postgres_context_maker_without_pool, flat_context_maker):
    context_maker = ContextMaker(
        postgres_context_maker=postgres_context_maker_without_pool,
        flat_context_maker=flat_context_maker,
    )
    return context_maker


@pytest.fixture(scope="function")
def context_without_pool(context_maker_without_pool):
    context = context_maker_without_pool()

    yield context

    context.close()


@pytest.fixture(autouse=True)
def clean_tables(postgres_context):
    for table in reversed(ORMBaseModel.metadata.sorted_tables):
        postgres_context.execute(table.delete())
    postgres_context.commit()


@pytest.fixture(autouse=True)
def clear_tmp_upload_dir(tmp_upload_dir):
    yield
    for item in tmp_upload_dir.iterdir():
        if item.is_file():
            item.unlink()
        else:
            shutil.rmtree(item)


@pytest.fixture(scope="session")
def unit_of_work(context_maker):
    return UnitOfWork(context_maker)


@pytest.fixture(scope="session")
def unit_of_work_without_pool(context_maker_without_pool):
    return UnitOfWork(context_maker_without_pool)


@pytest.fixture(scope="session")
def file_repo():
    return FileRepository()


@pytest.fixture(scope="session")
def file_metadata_repo():
    return FileMetadataRepository()


@pytest.fixture(scope="session")
def dataset_repo():
    return DatasetRepository()


@pytest.fixture(scope="session")
def task_repo():
    return TaskRepository()


@pytest.fixture(scope="session")
def check_content_type_use_case():
    return CheckContentType()


@pytest.fixture(scope="session")
def save_file_use_case(unit_of_work, file_repo, file_metadata_repo):
    return SaveFile(
        unit_of_work=unit_of_work,
        file_repo=file_repo,
        file_metadata_repo=file_metadata_repo,
    )


@pytest.fixture(scope="session")
def save_dataset_use_case(unit_of_work, dataset_repo):
    return SaveDataset(
        unit_of_work=unit_of_work,
        dataset_repo=dataset_repo,
    )


@pytest.fixture(scope="session")
def retrieve_dataset_use_case(unit_of_work, dataset_repo):
    return RetrieveDataset(
        unit_of_work=unit_of_work,
        dataset_repo=dataset_repo,
    )


@pytest.fixture(scope="session")
def profiling_task_worker():
    return ProfilingTaskWorker()


@pytest.fixture(scope="session")
def retrieve_task_use_case(unit_of_work, task_repo):
    return RetrieveTask(unit_of_work=unit_of_work, task_repo=task_repo)


@pytest.fixture(scope="session")
def set_task_use_case(unit_of_work, task_repo, dataset_repo, profiling_task_worker):
    return SetTask(
        unit_of_work=unit_of_work,
        task_repo=task_repo,
        dataset_repo=dataset_repo,
        profiling_task_worker=profiling_task_worker,
    )


@pytest.fixture(scope="session")
def profile_task_use_case(unit_of_work_without_pool, dataset_repo, file_repo):
    return ProfileTask(
        unit_of_work=unit_of_work_without_pool,
        dataset_repo=task_repo,
        file_repo=file_repo,
    )


@pytest.fixture(scope="session")
def update_task_info_use_case(unit_of_work_without_pool, task_repo):
    return UpdateTaskInfo(
        unit_of_work=unit_of_work_without_pool,
        task_repo=task_repo,
    )


@pytest.fixture(scope="session")
def client(
    save_file_use_case,
    save_dataset_use_case,
    check_content_type_use_case,
    set_task_use_case,
    retrieve_dataset_use_case,
    retrieve_task_use_case,
):
    from fastapi.testclient import TestClient
    from internal import app

    app.dependency_overrides[get_save_file_use_case] = lambda: save_file_use_case
    app.dependency_overrides[get_save_dataset_use_case] = lambda: save_dataset_use_case
    app.dependency_overrides[get_check_content_type_use_case] = (
        lambda: check_content_type_use_case
    )
    app.dependency_overrides[get_retrieve_dataset_use_case] = (
        lambda: retrieve_dataset_use_case
    )
    app.dependency_overrides[get_set_task_use_case] = lambda: set_task_use_case
    app.dependency_overrides[get_retrieve_task_use_case] = (
        lambda: retrieve_task_use_case
    )

    return TestClient(app)
