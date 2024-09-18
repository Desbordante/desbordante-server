from typing import Protocol
from uuid import UUID

from internal.dto.repository.base_schema import BaseCreateSchema, BaseUpdateSchema, BaseSchema


class FailedFileReadingException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class File(Protocol):

    filename: str | None
    content_type: str | None

    async def read(self, chunk_size: int) -> bytes: ...


class FileBaseSchema(BaseSchema):
    file_name: UUID


class FileCreateSchema(FileBaseSchema, BaseCreateSchema): ...


class FileUpdateSchema(FileBaseSchema, BaseUpdateSchema[UUID]): ...


class FileFindSchema(FileBaseSchema, BaseSchema): ... # it's not a typo

FileResponseSchema = None
