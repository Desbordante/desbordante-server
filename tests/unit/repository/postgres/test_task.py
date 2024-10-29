import pytest
from uuid import uuid4

from internal.domain.task.value_objects import TaskStatus, FdTaskConfig, PrimitiveName
from internal.domain.task.value_objects.fd import FdAlgoName
from internal.domain.task.value_objects.fd.algo_config import AidConfig
from internal.dto.repository.task import (
    TaskCreateSchema,
    TaskFindSchema,
    TaskUpdateSchema,
)
from internal.dto.repository.file import (
    DatasetCreateSchema,
    FileMetadataCreateSchema,
)
from internal.repository.relational.file import (
    DatasetRepository,
    FileMetadataRepository,
)
from internal.repository.relational.task import TaskRepository


@pytest.fixture
def file_create_schema():
    return FileMetadataCreateSchema(
        file_name=uuid4(),
        original_file_name="text.csv",
        mime_type="text/plain",
    )


@pytest.fixture
def file_id(file_create_schema, postgres_context):
    file_metadata_repo = FileMetadataRepository()
    response = file_metadata_repo.create(file_create_schema, postgres_context)
    return response.id


@pytest.fixture
def dataset_create_schema(file_id):
    return DatasetCreateSchema(file_id=file_id, separator=",", header=[0])


@pytest.fixture
def dataset_id(dataset_create_schema, postgres_context):
    dataset_repo = DatasetRepository()
    response = dataset_repo.create(dataset_create_schema, postgres_context)
    return response.id


@pytest.fixture
def get_config():
    return FdTaskConfig(
        primitive_name=PrimitiveName.fd,
        config=AidConfig(algo_name=FdAlgoName.Aid, max_lhs=1),
    )


@pytest.fixture
def repo():
    return TaskRepository()


@pytest.fixture
def create_schema(dataset_id, get_config):
    return TaskCreateSchema(
        dataset_id=dataset_id, status=TaskStatus.CREATED, config=get_config
    )


@pytest.fixture
def update_schema():
    return TaskUpdateSchema(
        failure_reason="memory_limit_exceeded", status=TaskStatus.COMPLETED
    )  # type: ignore


class TestDatasetRepository:
    def test_create(self, repo, create_schema, postgres_context):
        response = repo.create(create_schema, postgres_context)

        assert response is not None
        assert response.dataset_id == create_schema.dataset_id
        assert response.status == create_schema.status
        assert response.config == create_schema.config
        assert response.result is None
        assert response.failure_reason is None
        assert response.raised_exception_name is None
        assert response.traceback is None

    def test_create_and_find(
        self,
        repo,
        create_schema,
        postgres_context,
    ):
        empty_response = repo.find(TaskFindSchema(id=uuid4()), postgres_context)
        assert empty_response is None

        created_response = repo.create(create_schema, postgres_context)
        response = repo.find(TaskFindSchema(id=created_response.id), postgres_context)
        assert response is not None
        assert response.dataset_id == create_schema.dataset_id
        assert response.status == create_schema.status
        assert response.config == create_schema.config

    def test_update(self, repo, create_schema, update_schema, postgres_context):
        created_response = repo.create(create_schema, postgres_context)
        find_schema = TaskFindSchema(id=created_response.id)

        repo.update(find_schema, update_schema, None, postgres_context)

        response = repo.find(find_schema, postgres_context)
        assert response is not None
        assert response.dataset_id == create_schema.dataset_id
        assert response.status == update_schema.status
        assert response.config == create_schema.config
        assert response.failure_reason == update_schema.failure_reason

    def test_delete(self, repo, create_schema, postgres_context):
        created_response = repo.create(create_schema, postgres_context)
        find_schema = TaskFindSchema(id=created_response.id)

        response = repo.find(find_schema, postgres_context)
        assert response is not None

        repo.delete(find_schema, postgres_context)

        response = repo.find(find_schema, postgres_context)
        assert response is None
