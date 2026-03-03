from typing import Protocol, cast
from uuid import UUID

from src.domain.authorization.entities import AuthenticatedActor, Dataset
from src.exceptions import ForbiddenException
from src.models.dataset_models import DatasetModel


class DatasetCrud(Protocol):
    async def get_by(self, *, id: UUID) -> DatasetModel: ...
    async def delete(self, *, entity: DatasetModel) -> None: ...


class Storage(Protocol):
    async def delete(self, *, path: str) -> None: ...


class DatasetPolicy(Protocol):
    def can_delete(self, actor: AuthenticatedActor, dataset: Dataset) -> bool: ...


class DeleteDatasetUseCase:
    def __init__(
        self,
        *,
        dataset_crud: DatasetCrud,
        storage: Storage,
        dataset_policy: DatasetPolicy,
    ):
        self._dataset_crud = dataset_crud
        self._storage = storage
        self._dataset_policy = dataset_policy

    async def __call__(
        self,
        *,
        id: UUID,
        actor: AuthenticatedActor,
    ) -> None:
        dataset = await self._dataset_crud.get_by(id=id)

        if not self._dataset_policy.can_delete(
            actor=actor, dataset=cast(Dataset, dataset)
        ):
            raise ForbiddenException("Access denied")

        await self._storage.delete(path=dataset.path)
        await self._dataset_crud.delete(entity=dataset)
