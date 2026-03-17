import logging
from typing import Protocol, cast
from uuid import UUID, uuid4

from src.domain.authorization.entities import AuthenticatedActor, Dataset
from src.exceptions import ForbiddenException, PayloadTooLargeException
from src.models.dataset_models import DatasetModel, PreprocessingTaskModel
from src.schemas.base_schemas import TaskStatus
from src.schemas.dataset_schemas import (
    File,
    OneOfUploadDatasetParams,
)

logger = logging.getLogger(__name__)


class DatasetCrud(Protocol):
    async def create(self, entity: DatasetModel) -> DatasetModel: ...
    async def create_with_storage_check(
        self,
        *,
        entity: DatasetModel,
        user_id: int,
        storage_limit: int,
    ) -> DatasetModel: ...
    async def update(
        self,
        *,
        entity: DatasetModel,
        status: TaskStatus,
        preprocess_task_id: str | None = None,
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


class PreprocessDatasetTask(Protocol):
    def run(self, *, task_id: UUID, dataset_id: UUID) -> None: ...


class UploadDatasetUseCase:
    def __init__(
        self,
        *,
        dataset_crud: DatasetCrud,
        storage: Storage,
        dataset_policy: DatasetPolicy,
        settings: Settings,
        preprocess_dataset_task: PreprocessDatasetTask,
    ):
        self._dataset_crud = dataset_crud
        self._storage = storage
        self._dataset_policy = dataset_policy
        self._settings = settings
        self._preprocess_dataset_task = preprocess_dataset_task

    async def __call__(
        self,
        *,
        actor: AuthenticatedActor,
        file: File,
        params: OneOfUploadDatasetParams,
        is_public: bool,
    ) -> DatasetModel:
        storage_limit = self._settings.STORAGE_LIMIT

        if file.size > storage_limit:
            raise PayloadTooLargeException(
                "File size exceeds the maximum allowed size."
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
            preprocessing=PreprocessingTaskModel(),
        )

        if not self._dataset_policy.can_create(
            actor=actor, dataset=cast(Dataset, dataset_entity)
        ):
            raise ForbiddenException(
                "You are not allowed to create this type of datasets."
            )

        created_dataset = await self._dataset_crud.create_with_storage_check(
            entity=dataset_entity,
            user_id=actor.user_id,
            storage_limit=storage_limit,
        )

        try:
            await self._storage.upload(file=file, path=path)
        except Exception as e:
            await self._dataset_crud.delete(entity=created_dataset)
            raise e

        self._preprocess_dataset_task.run(
            task_id=created_dataset.preprocessing.id, dataset_id=created_dataset.id
        )

        return created_dataset
