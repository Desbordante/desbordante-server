import logging
import os
from typing import Protocol
from uuid import uuid4

from aioredlock import LockError

from src.domain.user.config import settings as user_settings
from src.exceptions import (
    ConflictException,
    PayloadTooLargeException,
    TooManyRequestsException,
)
from src.infrastructure.lock import lock_manager
from src.models.dataset_models import DatasetModel
from src.schemas.dataset_schemas import (
    DatasetsStatsSchema,
    File,
    OneOfUploadDatasetParams,
)

logger = logging.getLogger(__name__)


class DatasetCrud(Protocol):
    async def create(self, entity: DatasetModel) -> DatasetModel: ...
    async def get_stats(self, *, user_id: int) -> DatasetsStatsSchema: ...
    async def get_public_stats(self) -> DatasetsStatsSchema: ...


class Storage(Protocol):
    async def upload(self, *, file: File, path: str) -> str: ...
    async def delete(self, *, path: str) -> None: ...


class User(Protocol):
    id: int


class UploadDatasetUseCase:
    def __init__(
        self,
        *,
        dataset_crud: DatasetCrud,
        storage: Storage,
        user: User,
    ):
        self.dataset_crud = dataset_crud
        self.storage = storage
        self.user = user

    async def __call__(
        self, *, file: File, params: OneOfUploadDatasetParams, is_public: bool = False
    ) -> DatasetModel:
        try:
            async with await lock_manager.lock(f"user_upload_lock:{self.user.id}"):
                user_stats = await self.dataset_crud.get_stats(user_id=self.user.id)
                storage_limit = user_settings.STORAGE_LIMIT
                total_size = user_stats.total_size

                if file.size > storage_limit:
                    raise PayloadTooLargeException(
                        "File size exceeds the maximum allowed size."
                    )

                if total_size + file.size > storage_limit:
                    raise ConflictException(
                        "Storage limit reached. Delete some datasets to upload a new one."
                    )

                _, file_extension = os.path.splitext(file.name)
                path = f"{'public' if is_public else self.user.id}/{uuid4()}{file_extension}"

                await self.storage.upload(file=file, path=path)

                dataset_entity = DatasetModel(
                    type=params.type,
                    name=file.name,
                    size=file.size,
                    path=path,
                    params=params.model_dump(exclude={"type"}),
                    owner_id=self.user.id,
                    is_public=is_public,
                )

                try:
                    created_dataset = await self.dataset_crud.create(
                        entity=dataset_entity
                    )

                    return created_dataset
                except Exception as e:
                    await self.storage.delete(path=path)
                    raise e
        except LockError as e:
            logger.exception(e)
            raise TooManyRequestsException(
                "Upload in progress, try again later."
            ) from e
