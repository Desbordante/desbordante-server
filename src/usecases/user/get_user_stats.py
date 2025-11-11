from typing import Protocol

from src.domain.user.config import settings
from src.schemas.dataset_schemas import DatasetsStatsSchema
from src.schemas.user_schemas import UserStatsSchema


class DatasetCrud(Protocol):
    async def get_stats(self, *, user_id: int) -> DatasetsStatsSchema: ...


class GetUserStatsUseCase:
    def __init__(
        self,
        *,
        dataset_crud: DatasetCrud,
    ):
        self.dataset_crud = dataset_crud

    async def __call__(self, *, user_id: int) -> UserStatsSchema:
        datasets_stats = await self.dataset_crud.get_stats(user_id=user_id)

        return UserStatsSchema(
            datasets=datasets_stats,
            storage_limit=settings.STORAGE_LIMIT,
        )
