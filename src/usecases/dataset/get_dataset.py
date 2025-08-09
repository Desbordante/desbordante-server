from typing import Protocol
from uuid import UUID

from src.models.dataset_models import DatasetModel
from src.models.user_models import UserModel


class DatasetCrud(Protocol):
    async def get_by(self, *, id: UUID, owner_id: int) -> DatasetModel: ...


class GetDatasetUseCase:
    def __init__(
        self,
        *,
        dataset_crud: DatasetCrud,
        user: UserModel,
    ):
        self.dataset_crud = dataset_crud
        self.user = user

    async def __call__(
        self,
        *,
        id: UUID,
    ) -> DatasetModel:
        return await self.dataset_crud.get_by(
            owner_id=self.user.id,
            id=id,
        )
