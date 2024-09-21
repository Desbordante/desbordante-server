from uuid import UUID

from internal.dto.repository.base_schema import (
    BaseSchema,
    BaseCreateSchema,
    BaseUpdateSchema,
    BaseResponseSchema,
    BaseFindSchema,
)


class FileMetadataNotFoundException(Exception):

    def __init__(self):
        super().__init__("File metadata not found")


class FileMetadataBaseSchema(BaseSchema):
    file_name: UUID
    original_file_name: str
    mime_type: str


class FileMetadataCreateSchema(FileMetadataBaseSchema, BaseCreateSchema): ...


class FileMetadataUpdateSchema(FileMetadataBaseSchema, BaseUpdateSchema): ...


class FileMetadataFindSchema(BaseFindSchema[UUID]): ...


class FileMetadataResponseSchema(FileMetadataBaseSchema, BaseResponseSchema[UUID]): ...
