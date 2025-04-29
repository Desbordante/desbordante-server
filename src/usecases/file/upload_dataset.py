from typing import Protocol

from src.domain.file.storage import storage
from src.models.file_models import DatasetModel, FileModel
from src.models.user_models import UserModel
from src.schemas.file_schemas import (
    DatasetType,
    File,
    GraphDatasetParams,
    OneOfDatasetParams,
    OneOfUploadDatasetSchema,
    TabularDatasetParams,
    TransactionalDatasetParams,
)


class DatasetCrud(Protocol):
    async def create(self, entity: DatasetModel) -> DatasetModel: ...


class UploadDatasetUseCase:
    def __init__(
        self,
        *,
        dataset_crud: DatasetCrud,
        user: UserModel,
    ):
        self.dataset_crud = dataset_crud
        self.user = user

    async def __call__(
        self, *, file: File, data: OneOfUploadDatasetSchema
    ) -> DatasetModel:
        path = await storage.upload_file(file=file, owner_id=self.user.id)

        file_entity = FileModel(
            type=file.type,
            name=file.name,
            byte_size=file.size,
            path=path,
            owner_id=self.user.id,
        )

        params: OneOfDatasetParams

        if data.type == DatasetType.Tabular:
            params = TabularDatasetParams(
                type=data.type,
                has_header=data.has_header,
                separator=data.separator,
                number_of_columns=0,
                number_of_rows=0,
                column_names=[],
            )
        elif data.type == DatasetType.Transactional:
            params = TransactionalDatasetParams(
                type=data.type,
                has_header=data.has_header,
                separator=data.separator,
                number_of_columns=0,
                number_of_rows=0,
                column_names=[],
                transactional_params=data.transactional_params,
            )
        else:
            params = GraphDatasetParams(type=data.type)

        dataset_entity = DatasetModel(
            type=data.type,
            file=file_entity,
            params=params.serializable_dict(),
        )

        return await self.dataset_crud.create(entity=dataset_entity)
