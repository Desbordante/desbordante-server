from typing import Protocol
from uuid import UUID

from src.exceptions import ForbiddenException
from src.models.dataset_models import DatasetModel


class DatasetCrud(Protocol):
    async def get_by(self, *, id: UUID) -> DatasetModel: ...


class GetDatasetUseCase:
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
        current_user_id: int | None = None,
        is_admin: bool = False,
    ) -> DatasetModel:
        dataset = await self.dataset_crud.get_by(id=id)

        if dataset.is_public:
            return dataset

        if current_user_id is None:
            raise ForbiddenException("Authentication required")

        if dataset.owner_id != current_user_id and not is_admin:
            raise ForbiddenException("Access denied")

        return dataset
