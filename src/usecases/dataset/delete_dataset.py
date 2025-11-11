from typing import Protocol
from uuid import UUID

from src.domain.dataset.storage import storage
from src.models.dataset_models import DatasetModel


class DatasetCrud(Protocol):
    async def get_by(self, *, id: UUID, owner_id: int) -> DatasetModel: ...
    async def delete(self, *, entity: DatasetModel) -> None: ...


class User(Protocol):
    id: int


class DeleteDatasetUseCase:
    def __init__(
        self,
        *,
        dataset_crud: DatasetCrud,
        user: User,
    ):
        self.dataset_crud = dataset_crud
        self.user = user

    async def __call__(
        self,
        *,
        id: UUID,
    ) -> None:
        dataset = await self.dataset_crud.get_by(id=id, owner_id=self.user.id)

        await storage.delete_file(path=dataset.path)

        await self.dataset_crud.delete(entity=dataset)
