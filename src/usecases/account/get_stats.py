from typing import Protocol

from src.domain.account.config import settings
from src.schemas.account_schemas import AccountStatsSchema
from src.schemas.dataset_schemas import DatasetsStatsSchema
from src.schemas.session_schemas import UserSessionSchema


class DatasetCrud(Protocol):
    async def get_stats(self, *, user_id: int) -> DatasetsStatsSchema: ...


class GetStatsUseCase:
    def __init__(
        self,
        *,
        dataset_crud: DatasetCrud,
        user_session: UserSessionSchema,
    ):
        self.dataset_crud = dataset_crud
        self.user_session = user_session

    async def __call__(self) -> AccountStatsSchema:
        datasets_stats = await self.dataset_crud.get_stats(user_id=self.user_session.id)

        return AccountStatsSchema(
            datasets=datasets_stats,
            storage_limit=settings.STORAGE_LIMIT,
        )
