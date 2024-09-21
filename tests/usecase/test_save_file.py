from datetime import datetime
from uuid import uuid4

import pytest
from pytest_mock import MockerFixture

from internal.domain.file import File as FileEntity
from internal.dto.repository.file import (
    FileMetadataResponseSchema,
    File,
    FileMetadataCreateSchema,
    FileCreateSchema,
    FileResponseSchema,
    FailedFileReadingException,
)
from internal.uow import UnitOfWork, DataStorageContext
from internal.usecase.file.exception import FailedReadFileException
from internal.usecase.file.save_file import (
    FileMetadataRepo,
    FileRepo,
    SaveFile,
    SaveFileUseCaseResult,
)


@pytest.fixture
def unit_of_work_mock(mocker: MockerFixture) -> UnitOfWork:
    mock = mocker.MagicMock()
    mock.__enter__.return_value = mocker.Mock(
        return_value=mocker.Mock(), spec=DataStorageContext
    )
    mock.__exit__.return_value = None

    def exit_side_effect(exc_type, exc_value, traceback) -> bool:
        if exc_type:
            raise exc_value
        return False

    mock.__exit__.side_effect = exit_side_effect
    return mock


@pytest.fixture
def file_entity_mock(mocker: MockerFixture) -> FileEntity:
    mock = mocker.Mock(spec=FileEntity)
    mock.name_as_uuid = uuid4()
    mock.name = str(mock.name_as_uuid)
    return mock


@pytest.fixture
def file_repo_mock(mocker: MockerFixture) -> FileRepo:
    mock = mocker.Mock(spec=FileRepo)
    return mock


@pytest.fixture
def file_metadata_repo_mock(mocker: MockerFixture) -> FileMetadataRepo:
    mock = mocker.Mock(spec=FileMetadataRepo)
    return mock


@pytest.fixture
def save_file(
    mocker: MockerFixture,
    unit_of_work_mock: UnitOfWork,
    file_repo_mock: FileRepo,
    file_metadata_repo_mock: FileMetadataRepo,
    file_entity_mock: FileEntity,
) -> SaveFile:
    mocker.patch(
        "internal.usecase.file.save_file.FileEntity", return_value=file_entity_mock
    )
    return SaveFile(
        file_unit_of_work=unit_of_work_mock,
        file_info_unit_of_work=unit_of_work_mock,
        file_repo=file_repo_mock,
        file_metadata_repo=file_metadata_repo_mock,
    )


@pytest.mark.asyncio
async def test_save_file(
    mocker: MockerFixture,
    save_file: SaveFile,
    unit_of_work_mock: UnitOfWork,
    file_repo_mock: FileRepo,
    file_metadata_repo_mock: FileMetadataRepo,
    file_entity_mock: FileEntity,
) -> None:
    # Prepare data
    file_id = uuid4()
    file_name = file_entity_mock.name_as_uuid
    original_file_name = "example.txt"
    mime_type = "text/plain"
    created_at = datetime.now()
    updated_at = datetime.now()

    # Make mocks for entities and repositories responses
    file_metadata_response = FileMetadataResponseSchema(
        id=file_id,
        file_name=file_name,
        original_file_name=original_file_name,
        mime_type=mime_type,
        created_at=created_at,
        updated_at=updated_at,
    )

    file_response = FileResponseSchema

    file_repo_mock.create.return_value = file_response
    file_metadata_repo_mock.create.return_value = file_metadata_response

    upload_file_mock = mocker.Mock(spec=File)
    upload_file_mock.filename = original_file_name
    upload_file_mock.content_type = mime_type

    # Act
    result = await save_file(upload_file=upload_file_mock)

    # Check that the repositories' create methods were called with the correct arguments
    file_metadata_repo_mock.create.assert_called_once_with(
        FileMetadataCreateSchema(
            file_name=file_name,
            original_file_name=original_file_name,
            mime_type=mime_type,
        ),
        unit_of_work_mock.__enter__.return_value,
    )

    file_repo_mock.create.assert_called_once_with(
        upload_file_mock,
        FileCreateSchema(file_name=file_name),
        unit_of_work_mock.__enter__.return_value,
    )

    # Verify that UnitOfWork was used correctly
    assert unit_of_work_mock.__enter__.call_count == 2
    assert unit_of_work_mock.__exit__.call_count == 2

    # Verify that the result matches the expected SaveFileUseCaseResult
    assert result == SaveFileUseCaseResult(
        id=file_id,
        file_name=file_name,
        original_file_name=original_file_name,
        mime_type=mime_type,
        created_at=created_at,
        updated_at=updated_at,
    )


@pytest.mark.asyncio
async def test_save_file_failed_read_file_exception(
    mocker: MockerFixture,
    save_file: SaveFile,
    unit_of_work_mock: UnitOfWork,
    file_repo_mock: FileRepo,
    file_metadata_repo_mock: FileMetadataRepo,
    file_entity_mock: FileEntity,
) -> None:
    # Prepare the mock to raise the exception
    file_repo_mock.create.side_effect = FailedFileReadingException(
        "File reading failed"
    )

    upload_file_mock = mocker.Mock(spec=File)
    upload_file_mock.filename = "example.txt"
    upload_file_mock.content_type = "text/plain"

    # Act & Assert
    with pytest.raises(FailedReadFileException, match="File reading failed"):
        await save_file(upload_file=upload_file_mock)

    # Check that the repositories' create methods were called
    file_metadata_repo_mock.create.assert_called_once()
    file_repo_mock.create.assert_called_once()

    # Verify that UnitOfWork was used correctly
    assert unit_of_work_mock.__enter__.call_count == 2
    assert unit_of_work_mock.__exit__.call_count == 2
