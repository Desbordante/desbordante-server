from uuid import uuid4

import pytest
import pandas as pd
from pytest_mock import MockFixture

from internal.dto.repository.file import (
    FileCreateSchema,
    File,
    FailedFileReadingException,
    CSVFileFindSchema,
)
from internal.repository.flat import FileRepository


@pytest.fixture
def file_repository():
    return FileRepository()


@pytest.mark.asyncio
async def test_create_file_success(mocker: MockFixture, file_repository):
    file_name = uuid4()
    file_info = FileCreateSchema(file_name=file_name)

    mock_file = mocker.AsyncMock(spec=File)
    mock_file.read = mocker.AsyncMock()

    mock_context = mocker.MagicMock()
    mock_context.async_flush = mocker.AsyncMock()

    await file_repository.create(mock_file, file_info, mock_context)

    mock_context.add.assert_called_once()
    mock_context.async_flush.assert_called_once()


def test_find_file_success(file_repository, context):
    file_name = uuid4()
    file_content = "col1,col2\n1,2\n3,4"
    file_path = context.flat_context.upload_directory_path / str(file_name)

    with open(file_path, "w") as f:
        f.write(file_content)

    file_info = CSVFileFindSchema(file_name=file_name, separator=",", header=[0])

    result = file_repository.find(file_info, context)

    expected_df = pd.DataFrame({"col1": [1, 3], "col2": [2, 4]})
    pd.testing.assert_frame_equal(result, expected_df)


@pytest.mark.asyncio
async def test_create_file_failure(mocker: MockFixture, file_repository):
    file_name = uuid4()
    file_info = FileCreateSchema(file_name=file_name)

    mock_file = mocker.AsyncMock(spec=File)

    mock_context = mocker.MagicMock()
    mock_context.async_flush = mocker.AsyncMock(side_effect=Exception("Read error"))

    with pytest.raises(
        FailedFileReadingException, match="The sent file could not be read."
    ):
        await file_repository.create(mock_file, file_info, mock_context)


def test_find_file_failure(file_repository, context):
    file_info = CSVFileFindSchema(file_name=uuid4(), separator=",", header=[0])

    with pytest.raises(FileNotFoundError):
        file_repository.find(file_info, context)
