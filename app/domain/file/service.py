from typing import List
from uuid import UUID
from fastapi import UploadFile
from .repository import FileRepository
from .models import File
from .schemas import FileSchema
from .utils import storage
from .exceptions import FileAccessDeniedException


class FileService:
    def __init__(self, repository: FileRepository):
        self._repository = repository

    async def upload_file(self, file: UploadFile, owner_id: int) -> FileSchema:
        # Create database record
        db_file = File(name=file.filename, owner_id=owner_id)
        db_file = await self._repository.create(db_file)

        # Upload to MinIO
        storage.upload_file(
            str(db_file.id), file.file, file.size, content_type=file.content_type
        )

        return FileSchema.model_validate(db_file)

    async def get_file(self, file_id: UUID, user_id: int) -> FileSchema:
        file = await self._repository.get_by_id(file_id)
        if file.owner_id != user_id:
            raise FileAccessDeniedException()

        # Generate presigned URL for download
        url = storage.get_presigned_url(str(file.id))

        file_schema = FileSchema.model_validate(file)
        file_schema.download_url = url
        return file_schema

    async def get_user_files(self, user_id: int) -> List[FileSchema]:
        files = await self._repository.get_user_files(user_id)
        return [FileSchema.model_validate(file) for file in files]

    async def delete_file(self, file_id: UUID, user_id: int) -> None:
        file = await self._repository.get_by_id(file_id)
        if file.owner_id != user_id:
            raise FileAccessDeniedException()

        # Delete from MinIO
        storage.delete_file(str(file_id))
        # Delete from database
        await self._repository.delete(file)
