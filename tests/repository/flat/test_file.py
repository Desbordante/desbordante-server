from uuid import uuid4

import pytest
import aiofiles
import pandas as pd
from pytest_mock import MockFixture

from internal.dto.repository.file import (
    FileCreateSchema,
    File,
    FailedFileReadingException,
    CSVFileFindSchema,
)
from internal.infrastructure.data_storage.flat import FlatContext
from internal.repository.flat import FileRepository


@pytest.fixture
def mock_flat_context(tmp_path, mocker: MockFixture):
    context = mocker.MagicMock(spec=FlatContext)
    context.upload_directory_path = tmp_path
    return context


@pytest.fixture
def file_repository():
    return FileRepository()


@pytest.mark.asyncio
async def test_create_file_success(
    mocker: MockFixture, file_repository, mock_flat_context
):
    file_name = uuid4()
    file_content = b"Hello, World!"
    file_info = FileCreateSchema(file_name=file_name)

    mock_file = mocker.AsyncMock(spec=File)
    mock_file.read = mocker.AsyncMock(
        side_effect=[file_content, b""]
    )  # Читаем содержимое файла

    await file_repository.create(mock_file, file_info, mock_flat_context)

    created_file_path = mock_flat_context.upload_directory_path / str(file_name)
    assert created_file_path.is_file()

    async with aiofiles.open(created_file_path, "rb") as f:
        content = await f.read()
        assert content == file_content


def test_find_file_success(file_repository, mock_flat_context):
    file_name = uuid4()
    file_content = "col1,col2\n1,2\n3,4"
    file_path = mock_flat_context.upload_directory_path / file_name

    with open(file_path, "w") as f:
        f.write(file_content)

    file_info = CSVFileFindSchema(file_name=file_name, separator=",", header=[0])

    result = file_repository.find(file_info, mock_flat_context)

    expected_df = pd.DataFrame({"col1": [1, 3], "col2": [2, 4]})
    pd.testing.assert_frame_equal(result, expected_df)


@pytest.mark.asyncio
async def test_create_file_failure(
    mocker: MockFixture, file_repository, mock_flat_context
):
    file_name = uuid4()
    file_info = FileCreateSchema(file_name=file_name)

    mock_file = mocker.AsyncMock(spec=File)
    mock_file.read = mocker.AsyncMock(side_effect=Exception("Read error"))

    with pytest.raises(
        FailedFileReadingException, match="The sent file could not be read."
    ):
        await file_repository.create(mock_file, file_info, mock_flat_context)


def test_find_file_failure(file_repository, mock_flat_context):
    file_info = CSVFileFindSchema(file_name=uuid4(), separator=",", header=[0])

    with pytest.raises(FileNotFoundError):
        file_repository.find(file_info, mock_flat_context)
