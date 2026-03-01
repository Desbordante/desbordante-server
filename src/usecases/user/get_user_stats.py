from typing import Protocol

from src.schemas.dataset_schemas import DatasetsStatsSchema
from src.schemas.user_schemas import UserStatsSchema


class DatasetCrud(Protocol):
    async def get_stats(self, *, user_id: int) -> DatasetsStatsSchema: ...


class Settings(Protocol):
    STORAGE_LIMIT: int


class GetUserStatsUseCase:
    def __init__(
        self,
        *,
        dataset_crud: DatasetCrud,
        settings: Settings,
    ):
        self._dataset_crud = dataset_crud
        self._settings = settings

    async def __call__(self, *, user_id: int) -> UserStatsSchema:
        datasets_stats = await self._dataset_crud.get_stats(user_id=user_id)

        return UserStatsSchema(
            datasets=datasets_stats,
            storage_limit=self._settings.STORAGE_LIMIT,
        )
