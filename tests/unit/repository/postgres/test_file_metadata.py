import pytest
from uuid import uuid4

from internal.repository.relational.file import FileMetadataRepository
from internal.dto.repository.file import (
    FileMetadataCreateSchema,
    FileMetadataFindSchema,
    FileMetadataUpdateSchema,
)


@pytest.fixture
def repo():
    return FileMetadataRepository()


@pytest.fixture
def create_schema():
    return FileMetadataCreateSchema(
        file_name=uuid4(),
        original_file_name="text.csv",
        mime_type="text/plain",
    )


@pytest.fixture
def update_schema():
    return FileMetadataUpdateSchema(
        original_file_name="new_test.csv",
    )  # type: ignore


class TestFileMetadataRepository:
    def test_create(self, repo, create_schema, postgres_context):
        response = repo.create(create_schema, postgres_context)

        assert response is not None
        assert response.file_name == create_schema.file_name
        assert response.original_file_name == create_schema.original_file_name
        assert response.mime_type == create_schema.mime_type

    def test_create_and_find(
        self,
        repo,
        create_schema,
        postgres_context,
    ):
        empty_response = repo.find(FileMetadataFindSchema(id=uuid4()), postgres_context)
        assert empty_response is None

        created_response = repo.create(create_schema, postgres_context)
        response = repo.find(
            FileMetadataFindSchema(id=created_response.id), postgres_context
        )
        assert response is not None
        assert response.file_name == create_schema.file_name
        assert response.original_file_name == create_schema.original_file_name
        assert response.mime_type == create_schema.mime_type

    def test_update(self, repo, create_schema, update_schema, postgres_context):
        created_response = repo.create(create_schema, postgres_context)
        find_schema = FileMetadataFindSchema(id=created_response.id)

        repo.update(find_schema, update_schema, None, postgres_context)

        response = repo.find(find_schema, postgres_context)
        assert response is not None
        assert response.file_name == create_schema.file_name
        assert response.original_file_name == update_schema.original_file_name
        assert response.mime_type == create_schema.mime_type

    def test_delete(self, repo, create_schema, postgres_context):
        created_response = repo.create(create_schema, postgres_context)
        find_schema = FileMetadataFindSchema(id=created_response.id)

        response = repo.find(find_schema, postgres_context)
        assert response is not None

        repo.delete(find_schema, postgres_context)

        response = repo.find(find_schema, postgres_context)
        assert response is None
