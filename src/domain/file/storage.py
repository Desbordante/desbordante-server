import asyncio
import os
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from typing import Any, Callable, Optional, TypeVar
from uuid import uuid4

from minio import Minio

from src.schemas.file_schemas import File

from .config import settings

T = TypeVar("T")


class AsyncMinioClient:
    def __init__(
        self,
        minio_endpoint: str,
        access_key: str,
        secret_key: str,
        bucket: str,
        secure: bool = False,
        max_workers: Optional[int] = None,
    ):
        self.client = Minio(
            minio_endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure,
        )
        self.bucket = bucket
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

        # Initialize bucket in a sync manner
        # This is typically done once at startup
        if not self.client.bucket_exists(self.bucket):
            self.client.make_bucket(self.bucket)

    async def _run_in_executor(
        self, func: Callable[..., T], *args: Any, **kwargs: Any
    ) -> T:
        """Run a function in the executor."""
        partial_func = partial(func, *args, **kwargs)
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, partial_func)

    async def bucket_exists(self, bucket_name: str) -> bool:
        """Check if bucket exists asynchronously."""
        return await self._run_in_executor(self.client.bucket_exists, bucket_name)

    async def make_bucket(self, bucket_name: str) -> None:
        """Create bucket asynchronously."""
        await self._run_in_executor(self.client.make_bucket, bucket_name)

    async def upload_file(
        self,
        *,
        file: File,
        owner_id: int,
    ) -> str:
        """Upload file to MinIO storage asynchronously."""
        _, file_extension = os.path.splitext(file.name)
        file_id = f"{owner_id}/{file.type}/{uuid4()}{file_extension}"

        await self._run_in_executor(
            self.client.put_object,
            bucket_name=self.bucket,
            object_name=file_id,
            data=file.data,
            length=file.size,
            content_type=file.content_type,
        )

        return file_id


storage = AsyncMinioClient(
    minio_endpoint=settings.minio_endpoint,
    access_key=settings.MINIO_ROOT_USER,
    secret_key=settings.MINIO_ROOT_PASSWORD.get_secret_value(),
    bucket=settings.MINIO_BUCKET,
    secure=settings.MINIO_SECURE,
)
