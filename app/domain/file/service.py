from fastapi import UploadFile

from app.domain.file.models import File
from app.domain.file.schemas import FileFormat
from app.domain.file.utils import storage
from app.repository.repository import BaseRepository


class FileService:
    def __init__(self, repository: BaseRepository[File]):
        self._repository = repository

    def upload_file(self, file: UploadFile, owner_id: int) -> File:
        file_id = "{owner_id}/{file.filename}"

        # Upload to MinIO
        storage.upload_file(
            file_id=file_id,
            file=file.file,
            length=file.size,
            content_type=file.content_type,
        )

        # Create database record
        db_file = File(
            name=file.filename,
            owner_id=owner_id,
            path=file_id,
            file_format=FileFormat.CSV,
            byte_size=file.size,
        )
        db_file = self._repository.create(db_file)

        return db_file

    def get_user_files(self, user_id: int) -> list[File]:
        files = self._repository.get_many_by(field="owner_id", value=user_id)
        return files
