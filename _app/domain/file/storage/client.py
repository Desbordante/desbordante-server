import os
from datetime import timedelta
from uuid import uuid4

from fastapi import UploadFile
from minio import Minio

from _app.domain.file.schemas import FileType

from .config import settings


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
        file: UploadFile,
        type: FileType,
        owner_id: int,
    ) -> str:
        _, file_extension = os.path.splitext(file.filename)
        file_id = (
            f"{owner_id if owner_id else 'public'}/{type}/{uuid4()}{file_extension}"
        )
        """Upload file to MinIO storage"""
        self.client.put_object(
            bucket_name=self.bucket,
            object_name=file_id,
            data=file.file,
            length=file.size,
            content_type=file.content_type,
        )

        return file_id

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
