from datetime import timedelta
from typing import BinaryIO

from minio import Minio

from app.domain.storage.config import settings


class MinioClient:
    def __init__(
        self,
        minio_endpoint: str,
        access_key: str,
        secret_key: str,
        bucket: str,
        secure: bool = False,
    ):
        self.client = Minio(
            minio_endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure,
        )
        self.bucket = bucket

        # Ensure bucket exists
        if not self.client.bucket_exists(self.bucket):
            self.client.make_bucket(self.bucket)

    def upload_file(
        self,
        *,
        file_id: str,
        file: BinaryIO,
        length: int,
        content_type: str | None = None,
    ) -> None:
        """Upload file to MinIO storage"""
        self.client.put_object(
            bucket_name=self.bucket,
            object_name=file_id,
            data=file,
            length=length,
            content_type=content_type,
        )

    def download_file(self, name: str) -> bytes:
        response = self.client.get_object(self.bucket, name)
        data = response.read()
        response.close()
        return data

    def get_presigned_url(self, file_id: str) -> str:
        """Generate presigned URL for file download"""
        expires = timedelta(minutes=settings.MINIO_PRESIGNED_URL_EXPIRE_MINUTES)
        return self.client.presigned_get_object(self.bucket, file_id, expires=expires)

    def delete_file(self, file_id: str) -> None:
        """Delete file from MinIO storage"""
        self.client.remove_object(self.bucket, file_id)


# Create singleton instance
storage = MinioClient(
    minio_endpoint=settings.minio_endpoint,
    access_key=settings.MINIO_ROOT_USER,
    secret_key=settings.MINIO_ROOT_PASSWORD,
    bucket=settings.MINIO_BUCKET,
    secure=settings.MINIO_SECURE,
)
