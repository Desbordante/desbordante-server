from internal.dto.repository.file import (
    FileMetadataCreateSchema,
    FileMetadataUpdateSchema,
    FileMetadataFindSchema,
    FileMetadataResponseSchema,
)
from internal.infrastructure.data_storage.relational.model.file import FileMetadataORM
from internal.repository.relational import CRUD


class FileMetadataRepository(
    CRUD[
        FileMetadataORM,
        FileMetadataCreateSchema,
        FileMetadataUpdateSchema,
        FileMetadataFindSchema,
        FileMetadataResponseSchema,
    ]
):
    def __init__(self):
        super().__init__(
            orm_model=FileMetadataORM, response_schema=FileMetadataResponseSchema
        )
