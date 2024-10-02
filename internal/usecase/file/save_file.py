import datetime
from typing import Protocol
from uuid import UUID
from pydantic import BaseModel

from internal.domain.file import File as FileEntity
from internal.dto.repository.file import (
    FileCreateSchema,
    File,
    FailedFileReadingException,
)
from internal.dto.repository.file import (
    FileMetadataCreateSchema,
    FileMetadataResponseSchema,
)
from internal.uow import DataStorageContext, UnitOfWork
from internal.usecase.file.exception import FailedReadFileException


class FileRepo(Protocol):

    async def create(
        self, file: File, file_info: FileCreateSchema, context: DataStorageContext
    ) -> None: ...


class FileMetadataRepo(Protocol):

    def create(
        self, file_metadata: FileMetadataCreateSchema, context: DataStorageContext
    ) -> FileMetadataResponseSchema: ...


class SaveFileUseCaseResult(BaseModel):
    id: UUID
    file_name: UUID
    original_file_name: str
    mime_type: str
    created_at: datetime.datetime | None
    updated_at: datetime.datetime | None


class SaveFile:

    def __init__(
        self,
        unit_of_work: UnitOfWork,
        file_repo: FileRepo,
        file_metadata_repo: FileMetadataRepo,
    ):

        self.unit_of_work = unit_of_work
        self.file_repo = file_repo
        self.file_metadata_repo = file_metadata_repo

    async def __call__(self, *, upload_file: File) -> SaveFileUseCaseResult:
        file = FileEntity()

        create_file_schema = FileCreateSchema(file_name=file.name_as_uuid)
        file_metadata_create_schema = FileMetadataCreateSchema(
            file_name=file.name_as_uuid,
            original_file_name=upload_file.filename,
            mime_type=upload_file.content_type,
        )

        with self.unit_of_work as context:
            try:
                response = self.file_metadata_repo.create(
                    file_metadata_create_schema, context
                )
                await self.file_repo.create(upload_file, create_file_schema, context)
            except FailedFileReadingException as e:
                raise FailedReadFileException(str(e))

        return SaveFileUseCaseResult(
            id=response.id,
            file_name=response.file_name,
            original_file_name=response.original_file_name,
            mime_type=response.mime_type,
            created_at=response.created_at,
            updated_at=response.updated_at,
        )
