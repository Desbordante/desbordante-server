from typing import Protocol

from src.domain.account.config import settings
from src.models.user_models import UserModel
from src.schemas.account_schemas import AccountStatsSchema
from src.schemas.dataset_schemas import DatasetsStatsSchema


class DatasetCrud(Protocol):
    async def get_stats(self, *, user_id: int) -> DatasetsStatsSchema: ...


class GetStatsUseCase:
    def __init__(
        self,
        *,
        dataset_crud: DatasetCrud,
        user: UserModel,
    ):
        self.dataset_crud = dataset_crud
        self.user = user

    async def __call__(self) -> AccountStatsSchema:
        datasets_stats = await self.dataset_crud.get_stats(user_id=self.user.id)

        return AccountStatsSchema(
            datasets=datasets_stats,
            storage_limit=settings.STORAGE_LIMIT,
        )
