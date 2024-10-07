import pytest
from uuid import uuid4

from internal.repository.relational.file import (
    DatasetRepository,
    FileMetadataRepository,
)
from internal.dto.repository.file import (
    DatasetCreateSchema,
    DatasetFindSchema,
    DatasetUpdateSchema,
    FileMetadataCreateSchema,
)


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
def repo():
    return DatasetRepository()


@pytest.fixture
def create_schema(file_id):
    return DatasetCreateSchema(file_id=file_id, separator=",", header=[0])


@pytest.fixture
def update_schema():
    return DatasetUpdateSchema(separator=",", header=[1])  # type: ignore


class TestDatasetRepository:
    def test_create(self, repo, create_schema, postgres_context):
        response = repo.create(create_schema, postgres_context)

        assert response is not None
        assert response.file_id == create_schema.file_id
        assert response.separator == create_schema.separator
        assert response.header == create_schema.header

    def test_create_and_find(
        self,
        repo,
        create_schema,
        postgres_context,
    ):
        empty_response = repo.find(DatasetFindSchema(id=uuid4()), postgres_context)
        assert empty_response is None

        created_response = repo.create(create_schema, postgres_context)
        response = repo.find(
            DatasetFindSchema(id=created_response.id), postgres_context
        )
        assert response is not None
        assert response.file_id == create_schema.file_id
        assert response.separator == create_schema.separator
        assert response.header == create_schema.header

    def test_update(self, repo, create_schema, update_schema, postgres_context):
        created_response = repo.create(create_schema, postgres_context)
        find_schema = DatasetFindSchema(id=created_response.id)

        repo.update(find_schema, update_schema, None, postgres_context)

        response = repo.find(find_schema, postgres_context)
        assert response is not None
        assert response.file_id == create_schema.file_id
        assert response.separator == update_schema.separator
        assert response.header == update_schema.header

    def test_delete(self, repo, create_schema, postgres_context):
        created_response = repo.create(create_schema, postgres_context)
        find_schema = DatasetFindSchema(id=created_response.id)

        response = repo.find(find_schema, postgres_context)
        assert response is not None

        repo.delete(find_schema, postgres_context)

        response = repo.find(find_schema, postgres_context)
        assert response is None
