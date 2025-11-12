from typing import Protocol
from uuid import UUID

from src.domain.dataset.storage import storage
from src.exceptions import ForbiddenException
from src.models.dataset_models import DatasetModel


class DatasetCrud(Protocol):
    async def get_by(self, *, id: UUID) -> DatasetModel: ...
    async def delete(self, *, entity: DatasetModel) -> None: ...


class DeleteDatasetUseCase:
    def __init__(
        self,
        *,
        dataset_crud: DatasetCrud,
    ):
        self.dataset_crud = dataset_crud

    async def __call__(
        self,
        *,
        id: UUID,
        current_user_id: int,
        is_admin: bool = False,
    ) -> None:
        dataset = await self.dataset_crud.get_by(id=id)

        if dataset.is_public:
            if not is_admin:
                raise ForbiddenException("Only admin can delete public datasets")
        else:
            if dataset.owner_id != current_user_id and not is_admin:
                raise ForbiddenException("Access denied")

        await storage.delete_file(path=dataset.path)

        await self.dataset_crud.delete(entity=dataset)
