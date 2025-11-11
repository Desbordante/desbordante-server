import logging
import os
from typing import Protocol
from uuid import uuid4

from aioredlock import LockError

from src.domain.dataset.storage import storage
from src.domain.dataset.tasks import preprocess_dataset
from src.domain.user.config import settings
from src.exceptions import (
    ConflictException,
    PayloadTooLargeException,
    TooManyRequestsException,
)
from src.models.dataset_models import DatasetModel
from src.redis.lock import lock_manager
from src.schemas.dataset_schemas import (
    DatasetsStatsSchema,
    File,
    OneOfUploadDatasetParams,
)

logger = logging.getLogger(__name__)


class DatasetCrud(Protocol):
    async def create(self, entity: DatasetModel) -> DatasetModel: ...
    async def get_stats(self, *, user_id: int) -> DatasetsStatsSchema: ...


class User(Protocol):
    id: int


class UploadDatasetUseCase:
    def __init__(
        self,
        *,
        dataset_crud: DatasetCrud,
        user: User,
    ):
        self.dataset_crud = dataset_crud
        self.user = user

    async def __call__(
        self, *, file: File, params: OneOfUploadDatasetParams
    ) -> DatasetModel:
        try:
            async with await lock_manager.lock(f"user_upload_lock:{self.user.id}"):
                if file.size > settings.STORAGE_LIMIT:
                    raise PayloadTooLargeException(
                        "File size exceeds the maximum allowed size."
                    )

                datasets_stats = await self.dataset_crud.get_stats(user_id=self.user.id)

                if datasets_stats.total_size + file.size > settings.STORAGE_LIMIT:
                    raise ConflictException(
                        "You have reached your storage limit. Delete some datasets to upload a new one."
                    )

                _, file_extension = os.path.splitext(file.name)
                path = f"{self.user.id}/{uuid4()}{file_extension}"

                await storage.upload_file(file=file, path=path)

                dataset_entity = DatasetModel(
                    type=params.type,
                    name=file.name,
                    size=file.size,
                    path=path,
                    params=params.model_dump(exclude={"type"}),
                    owner_id=self.user.id,
                )

                try:
                    created_dataset = await self.dataset_crud.create(
                        entity=dataset_entity
                    )

                    preprocess_dataset.delay(created_dataset.id)

                    return created_dataset
                except Exception as e:
                    await storage.delete_file(path=path)
                    raise e
        except LockError as e:
            logger.exception(e)
            raise TooManyRequestsException(
                "Upload in progress, try again later."
            ) from e
