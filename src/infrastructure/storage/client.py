from contextlib import asynccontextmanager
from typing import Any

from aiobotocore.session import get_session
from botocore.config import Config
from botocore.exceptions import ClientError

from src.exceptions import ResourceNotFoundException
from src.schemas.dataset_schemas import File

from .config import settings


class S3Storage:
    def __init__(
        self,
        *,
        endpoint_url: str,
        access_key: str,
        secret_key: str,
        bucket: str,
    ):
        self._endpoint_url = endpoint_url
        self._access_key = access_key
        self._secret_key = secret_key
        self._bucket = bucket
        self._session = get_session()
        self._config = Config(
            signature_version="s3v4",
            retries={"max_attempts": 3, "mode": "standard"},
        )

    def _client_params(self):
        return {
            "endpoint_url": self._endpoint_url,
            "aws_access_key_id": self._access_key,
            "aws_secret_access_key": self._secret_key,
            "region_name": "us-east-1",
            "config": self._config,
        }

    @asynccontextmanager
    async def get_client(self):
        async with self._session.create_client("s3", **self._client_params()) as client:
            yield client

    async def upload(self, *, file: File, path: str) -> str:
        """Upload file to S3 storage."""
        async with self.get_client() as client:
            file.data.seek(0)

            await client.put_object(
                Bucket=self._bucket,
                Key=path,
                Body=file.data,
                ContentType=file.content_type,
            )
        return path

    async def delete(self, *, path: str) -> None:
        """Delete file from S3 storage."""
        async with self.get_client() as client:
            await client.delete_object(Bucket=self._bucket, Key=path)

    async def download(self, *, path: str) -> bytes:
        """Download file from S3 storage."""
        async with self.get_client() as client:
            try:
                response = await client.get_object(Bucket=self._bucket, Key=path)
            except ClientError as e:
                if e.response.get("Error", {}).get("Code") == "NoSuchKey":
                    raise ResourceNotFoundException("File not found in storage") from e
                raise
            body: Any = response["Body"]
            return await body.read()


def get_storage() -> S3Storage:
    return S3Storage(
        endpoint_url=settings.minio_endpoint_url.unicode_string(),
        access_key=settings.MINIO_ROOT_USER,
        secret_key=settings.MINIO_ROOT_PASSWORD.get_secret_value(),
        bucket=settings.MINIO_BUCKET,
    )
