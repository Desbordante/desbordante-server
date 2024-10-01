import pytest
from pytest_mock import MockerFixture
import aiofiles
from pathlib import Path
from internal.infrastructure.data_storage.flat import FlatContext, FlatAddModel
from internal.dto.repository.file import File


@pytest.fixture
def tmp_upload_dir(tmp_path):
    return tmp_path


@pytest.fixture
def flat_context(tmp_upload_dir):
    return FlatContext(upload_directory_path=tmp_upload_dir)


@pytest.fixture
def mock_file(mocker: MockerFixture):
    mock = mocker.AsyncMock(spec=File)
    mock.read = mocker.AsyncMock(side_effect=[b"Hello", b" ", b"World", b""])
    return mock


@pytest.fixture
def mock_sync_file(mocker: MockerFixture):
    mock = mocker.Mock()
    mock.read.side_effect = [b"Hello World", b""]
    return mock


@pytest.fixture
def file_name():
    return "test_file.txt"


@pytest.mark.asyncio
async def test_add_and_flush_file(flat_context, mock_file, file_name):
    file_model = FlatAddModel(file=mock_file, file_name=file_name)
    flat_context.add(file_model)
    await flat_context.async_flush()
    added_file_path = Path(flat_context.upload_directory_path) / file_name
    assert added_file_path.exists()
    async with aiofiles.open(added_file_path, "rb") as f:
        content = await f.read()
        assert content == b"Hello World"


def test_add_and_sync_flush_file(flat_context, mock_sync_file, file_name):
    file_model = FlatAddModel(file=mock_sync_file, file_name=file_name)
    flat_context.add(file_model)
    flat_context.flush()
    added_file_path = Path(flat_context.upload_directory_path) / file_name
    assert added_file_path.exists()
    with open(added_file_path, "rb") as f:
        content = f.read()
        assert content == b"Hello World"


@pytest.mark.asyncio
async def test_rollback_on_flush_failure(
    flat_context, mock_file, file_name, mocker: MockerFixture
):
    file_model = FlatAddModel(file=mock_file, file_name=file_name)
    flat_context.add(file_model)
    mocker.patch("aiofiles.open", side_effect=Exception("Failed to write file"))
    with pytest.raises(Exception, match="Failed to write file"):
        await flat_context.async_flush()
    assert not Path(flat_context.upload_directory_path / file_name).exists()


@pytest.mark.asyncio
async def test_commit_clears_added_list(flat_context, mock_file, file_name):
    file_model = FlatAddModel(file=mock_file, file_name=file_name)
    flat_context.add(file_model)
    await flat_context.async_flush()
    flat_context.commit()
    added_file_path = Path(flat_context.upload_directory_path) / file_name
    assert added_file_path.exists()
    assert not flat_context._added


@pytest.mark.asyncio
async def test_rollback_clears_files(flat_context, mock_file, file_name):
    file_model = FlatAddModel(file=mock_file, file_name=file_name)
    flat_context.add(file_model)
    await flat_context.async_flush()
    added_file_path = Path(flat_context.upload_directory_path) / file_name
    assert added_file_path.exists()
    flat_context.rollback()
    assert not added_file_path.exists()


@pytest.mark.asyncio
async def test_close_without_files(flat_context):
    flat_context.close()
    assert flat_context._is_closed == True
    assert flat_context._to_add == []
    assert flat_context._added == []


@pytest.mark.asyncio
async def test_close_with_rollback(flat_context, mock_file, file_name):
    file_model = FlatAddModel(file=mock_file, file_name=file_name)
    flat_context.add(file_model)
    await flat_context.async_flush()
    added_file_path = Path(flat_context.upload_directory_path) / file_name
    assert added_file_path.exists()
    flat_context.close()
    assert not added_file_path.exists()
    assert flat_context._is_closed == True
    assert flat_context._to_add == []
    assert flat_context._added == []
