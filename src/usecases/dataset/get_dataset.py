from typing import Protocol, cast
from uuid import UUID

from src.domain.authorization.entities import Actor, Dataset
from src.exceptions import ResourceNotFoundException
from src.models.dataset_models import DatasetModel


class DatasetCrud(Protocol):
    async def get_by(self, *, id: UUID) -> DatasetModel: ...


class DatasetPolicy(Protocol):
    def can_read(self, actor: Actor, dataset: Dataset) -> bool: ...


class GetDatasetUseCase:
    def __init__(
        self,
        *,
        dataset_crud: DatasetCrud,
        dataset_policy: DatasetPolicy,
    ):
        self._dataset_crud = dataset_crud
        self._dataset_policy = dataset_policy

    async def __call__(
        self,
        *,
        id: UUID,
        actor: Actor,
    ) -> DatasetModel:
        dataset = await self._dataset_crud.get_by(id=id)

        if not self._dataset_policy.can_read(actor, cast(Dataset, dataset)):
            raise ResourceNotFoundException("Dataset not found")

        return dataset
