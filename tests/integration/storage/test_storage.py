import pytest
from botocore.exceptions import ClientError

from src.infrastructure.storage.client import S3Storage

from .helpers import make_test_path

pytestmark = [pytest.mark.asyncio, pytest.mark.integration]


async def test_upload_and_download(s3_storage: S3Storage, make_file) -> None:
    """Upload file and download it back."""
    path = make_test_path("file.csv")
    file = make_file(content=b"col1,col2\n1,2\n3,4")

    result_path = await s3_storage.upload(file=file, path=path)
    assert result_path == path

    data = await s3_storage.download(path=path)
    assert data == b"col1,col2\n1,2\n3,4"


async def test_delete_removes_file(s3_storage: S3Storage, make_file) -> None:
    """Delete removes the file from storage."""
    path = make_test_path("file.csv")
    file = make_file(content=b"to be deleted")

    await s3_storage.upload(file=file, path=path)
    await s3_storage.delete(path=path)

    with pytest.raises(ClientError):
        await s3_storage.download(path=path)


async def test_upload_overwrites_existing(s3_storage: S3Storage, make_file) -> None:
    """Uploading to same path overwrites the file."""
    path = make_test_path("file.csv")

    file1 = make_file(content=b"first content")
    await s3_storage.upload(file=file1, path=path)

    file2 = make_file(content=b"second content")
    await s3_storage.upload(file=file2, path=path)

    data = await s3_storage.download(path=path)
    assert data == b"second content"


async def test_download_nonexistent_raises(s3_storage: S3Storage) -> None:
    """Downloading non-existent file raises."""
    path = make_test_path("nonexistent.csv")

    with pytest.raises(ClientError):
        await s3_storage.download(path=path)


async def test_delete_nonexistent_succeeds(s3_storage: S3Storage) -> None:
    """Deleting non-existent file does not raise (S3 behavior)."""
    path = make_test_path("nonexistent.csv")

    await s3_storage.delete(path=path)  # should not raise
