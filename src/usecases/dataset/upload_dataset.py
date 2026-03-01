import logging
from typing import Protocol, cast
from uuid import uuid4

from src.domain.authorization.entities import AuthenticatedActor, Dataset
from src.exceptions import (
    ConflictException,
    ForbiddenException,
    PayloadTooLargeException,
)
from src.models.dataset_models import DatasetModel
from src.schemas.dataset_schemas import (
    DatasetsStatsSchema,
    DatasetStatus,
    File,
    OneOfUploadDatasetParams,
)

logger = logging.getLogger(__name__)


class DatasetCrud(Protocol):
    async def create(self, entity: DatasetModel) -> DatasetModel: ...
    async def get_stats(self, *, user_id: int) -> DatasetsStatsSchema: ...
    async def update(
        self, *, entity: DatasetModel, status: DatasetStatus
    ) -> DatasetModel: ...
    async def delete(self, *, entity: DatasetModel) -> None: ...


class Storage(Protocol):
    async def upload(self, *, file: File, path: str) -> str: ...
    async def delete(self, *, path: str) -> None: ...


class DatasetPolicy(Protocol):
    def can_create(self, actor: AuthenticatedActor, dataset: Dataset) -> bool: ...


class User(Protocol):
    id: int


class Settings(Protocol):
    STORAGE_LIMIT: int


class UploadDatasetUseCase:
    def __init__(
        self,
        *,
        dataset_crud: DatasetCrud,
        storage: Storage,
        dataset_policy: DatasetPolicy,
        settings: Settings,
    ):
        self._dataset_crud = dataset_crud
        self._storage = storage
        self._dataset_policy = dataset_policy
        self._settings = settings

    async def __call__(
        self,
        *,
        actor: AuthenticatedActor,
        file: File,
        params: OneOfUploadDatasetParams,
        is_public: bool,
    ) -> DatasetModel:
        user_stats = await self._dataset_crud.get_stats(user_id=actor.user_id)

        storage_limit = self._settings.STORAGE_LIMIT

        total_size = user_stats.total_size

        if file.size > storage_limit:
            raise PayloadTooLargeException(
                "File size exceeds the maximum allowed size."
            )

        if total_size + file.size > storage_limit:
            raise ConflictException(
                "Storage limit reached. Delete some datasets to upload a new one."
            )

        path = f"{actor.user_id}/{uuid4()}"

        dataset_entity = DatasetModel(
            type=params.type,
            name=file.name,
            size=file.size,
            path=path,
            params=params.model_dump(exclude={"type"}),
            owner_id=actor.user_id,
            is_public=is_public,
        )

        if not self._dataset_policy.can_create(
            actor=actor, dataset=cast(Dataset, dataset_entity)
        ):
            raise ForbiddenException(
                "You are not allowed to create this type of datasets."
            )

        created_dataset = await self._dataset_crud.create(entity=dataset_entity)

        try:
            await self._storage.upload(file=file, path=path)
        except Exception as e:
            await self._dataset_crud.delete(entity=created_dataset)
            raise e

        await self._dataset_crud.update(
            entity=created_dataset, status=DatasetStatus.READY
        )

        return created_dataset
