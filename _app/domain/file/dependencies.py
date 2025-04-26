from typing import Annotated

from fastapi import Depends


from _app.domain.file.storage.client import MinioClient
from _app.domain.file.storage.config import settings


def get_storage_client() -> MinioClient:
    return MinioClient(
        minio_endpoint=settings.minio_endpoint,
        access_key=settings.MINIO_ROOT_USER,
        secret_key=settings.MINIO_ROOT_PASSWORD,
        bucket=settings.MINIO_BUCKET,
        secure=settings.MINIO_SECURE,
    )


StorageClientDep = Annotated[MinioClient, Depends(get_storage_client)]
