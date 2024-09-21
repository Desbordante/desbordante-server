from sqlalchemy import select
from sqlalchemy.orm import joinedload

from internal.infrastructure.data_storage.relational.context import (
    RelationalContextType,
)
from internal.infrastructure.data_storage.relational.model.file import DatasetORM
from internal.repository.relational import CRUD
from internal.dto.repository.file import (
    DatasetCreateSchema,
    DatasetUpdateSchema,
    DatasetFindSchema,
    DatasetResponseSchema,
    FileMetadataResponseSchema,
    DatasetNotFoundException,
)


class DatasetRepository(
    CRUD[
        DatasetORM,
        DatasetCreateSchema,
        DatasetUpdateSchema,
        DatasetFindSchema,
        DatasetResponseSchema,
    ]
):

    def __init__(self):
        super().__init__(orm_model=DatasetORM, response_schema=DatasetResponseSchema)

    def find_with_file_metadata(
        self,
        dataset_info: DatasetFindSchema,
        context: RelationalContextType,
    ) -> tuple[DatasetResponseSchema, FileMetadataResponseSchema]:

        dataset_find_dict = dataset_info.model_dump()
        stmt = (
            select(DatasetORM)
            .options(joinedload(DatasetORM.file_metadata))
            .filter_by(**dataset_find_dict)
        )
        dataset_orm_instance = context.execute(stmt).scalars().one_or_none()

        if not dataset_orm_instance:
            raise DatasetNotFoundException()

        dataset_response = DatasetResponseSchema.model_validate(dataset_orm_instance)
        file_metadata_response = FileMetadataResponseSchema.model_validate(
            dataset_orm_instance.file_metadata
        )

        return dataset_response, file_metadata_response
