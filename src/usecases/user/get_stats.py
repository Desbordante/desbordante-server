from typing import Protocol

from src.domain.user.config import settings
from src.schemas.dataset_schemas import DatasetsStatsSchema
from src.schemas.user_schemas import UserStatsSchema


class DatasetCrud(Protocol):
    async def get_stats(self, *, user_id: int) -> DatasetsStatsSchema: ...


class User(Protocol):
    id: int


class GetStatsUseCase:
    def __init__(
        self,
        *,
        dataset_crud: DatasetCrud,
        user: User,
    ):
        self.dataset_crud = dataset_crud
        self.user = user

    async def __call__(self) -> UserStatsSchema:
        datasets_stats = await self.dataset_crud.get_stats(user_id=self.user.id)

        return UserStatsSchema(
            datasets=datasets_stats,
            storage_limit=settings.STORAGE_LIMIT,
        )
