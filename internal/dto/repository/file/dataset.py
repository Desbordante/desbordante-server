from uuid import UUID

from internal.dto.repository.base_schema import (
    BaseSchema,
    BaseCreateSchema,
    BaseUpdateSchema,
    BaseResponseSchema,
    BaseFindSchema,
)


class DatasetBaseSchema(BaseSchema):
    file_id: UUID
    separator: str
    header: list[int]
    is_built_in: bool = False


class DatasetCreateSchema(DatasetBaseSchema, BaseCreateSchema): ...


class DatasetUpdateSchema(DatasetBaseSchema, BaseUpdateSchema): ...


class DatasetFindSchema(BaseFindSchema[UUID]): ...


class DatasetResponseSchema(DatasetBaseSchema, BaseResponseSchema[UUID]): ...


class DatasetNotFoundException(Exception):
    """
    Exception raised when a dataset is not found in some data storage.

    This exception may be thrown only by the repository.
    """

    def __init__(self):
        """
        Initializes an instance of DatasetNotFoundException with a default message.
        """
        super().__init__("Dataset not found")
