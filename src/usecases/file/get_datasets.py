from typing import Protocol

from sqlalchemy import Select, select

from src.models.file_models import DatasetModel, FileModel
from src.models.user_models import UserModel


class DatasetCrud(Protocol):
    async def get_many(
        self, *, limit: int, offset: int, query: Select[tuple[DatasetModel]]
    ) -> list[DatasetModel]: ...


class GetDatasetsUseCase:
    def __init__(
        self,
        *,
        dataset_crud: DatasetCrud,
        user: UserModel,
    ):
        self.dataset_crud = dataset_crud
        self.user = user

    async def __call__(self, *, limit: int, offset: int) -> list[DatasetModel]:
        query: Select[tuple[DatasetModel]] = (
            select(DatasetModel)
            .join(FileModel, DatasetModel.file_id == FileModel.id)
            .where(FileModel.owner_id == self.user.id)
            .limit(limit)
            .offset(offset)
        )

        return await self.dataset_crud.get_many(limit=limit, offset=offset, query=query)
