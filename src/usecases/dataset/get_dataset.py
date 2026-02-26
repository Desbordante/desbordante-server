from typing import Protocol
from uuid import UUID

from src.domain.authorization.entities import Actor
from src.exceptions import ForbiddenException
from src.models.dataset_models import DatasetModel


class DatasetCrud(Protocol):
    async def get_by(self, *, id: UUID) -> DatasetModel: ...


class DatasetPolicy(Protocol):
    def can_read(self, actor: Actor, dataset: DatasetModel) -> bool: ...


class GetDatasetUseCase:
    def __init__(
        self,
        *,
        dataset_crud: DatasetCrud,
        dataset_policy: DatasetPolicy,
    ):
        self.dataset_crud = dataset_crud
        self.dataset_policy = dataset_policy

    async def __call__(
        self,
        *,
        id: UUID,
        actor: Actor,
    ) -> DatasetModel:
        dataset = await self.dataset_crud.get_by(id=id)

        if not self.dataset_policy.can_read(actor, dataset):
            raise ForbiddenException("Access denied")

        return dataset
