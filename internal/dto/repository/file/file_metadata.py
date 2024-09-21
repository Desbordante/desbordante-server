from uuid import UUID

from internal.dto.repository.base_schema import (
    BaseSchema,
    BaseCreateSchema,
    BaseUpdateSchema,
    BaseResponseSchema,
    BaseFindSchema,
)


class FileMetadataBaseSchema(BaseSchema):
    file_name: UUID
    original_file_name: str
    mime_type: str


class FileMetadataCreateSchema(FileMetadataBaseSchema, BaseCreateSchema): ...


class FileMetadataUpdateSchema(FileMetadataBaseSchema, BaseUpdateSchema): ...


class FileMetadataFindSchema(BaseFindSchema[UUID]): ...


class FileMetadataResponseSchema(FileMetadataBaseSchema, BaseResponseSchema[UUID]): ...


class FileMetadataNotFoundException(Exception):
    """
    Exception raised when a file metadata is not found in some data storage.

    This exception may be thrown only by the repository.
    """

    def __init__(self):
        """
        Initializes an instance of FileMetadataNotFoundException with a default message.
        """
        super().__init__("File metadata not found")
