import os
from typing import Protocol
from uuid import uuid4

from src.domain.dataset.storage import storage
from src.models.dataset_models import DatasetModel
from src.models.user_models import UserModel
from src.schemas.dataset_schemas import File, OneOfUploadDatasetParams


class DatasetCrud(Protocol):
    async def create(self, entity: DatasetModel) -> DatasetModel: ...
    async def get_user_datasets_size(self, *, owner_id: int) -> int: ...


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
        self, *, file: File, params: OneOfUploadDatasetParams
    ) -> DatasetModel:
        _, file_extension = os.path.splitext(file.name)
        path = f"{self.user.id}/{uuid4()}{file_extension}"

        await storage.upload_file(file=file, path=path)

        dataset_entity = DatasetModel(
            type=params.type,
            name=file.name,
            size=file.size,
            path=path,
            params=params.model_dump(exclude={"type"}),
            owner_id=self.user.id,
        )

        try:
            return await self.dataset_crud.create(entity=dataset_entity)
        except Exception as e:
            await storage.delete_file(path=path)
            raise e
