
from internal.infrastructure.data_storage.relational.model.file import DatasetORM
from internal.repository.relational import CRUD
from internal.dto.repository.file import (DatasetCreateSchema, DatasetUpdateSchema,
                                          DatasetFindSchema, DatasetResponseSchema)


class DatasetRepository(
    CRUD[
        DatasetORM,
        DatasetCreateSchema,
        DatasetUpdateSchema,
        DatasetFindSchema,
        DatasetResponseSchema
    ]
):

    def __init__(self):
        super().__init__(orm_model=DatasetORM, response_schema=DatasetResponseSchema)
