from typing import Protocol

from src.models.dataset_models import DatasetModel
from src.models.user_models import UserModel
from src.schemas.base_schemas import PaginatedResult, PaginationParamsSchema
from src.schemas.dataset_schemas import DatasetQueryParamsSchema


class DatasetCrud(Protocol):
    async def get_many(
        self,
        *,
        pagination: PaginationParamsSchema,
        query_params: DatasetQueryParamsSchema,
        owner_id: int,
    ) -> PaginatedResult[DatasetModel]: ...


class GetDatasetsUseCase:
    def __init__(
        self,
        *,
        dataset_crud: DatasetCrud,
        user: UserModel,
    ):
        self.dataset_crud = dataset_crud
        self.user = user

    async def __call__(
        self,
        *,
        pagination: PaginationParamsSchema,
        query_params: DatasetQueryParamsSchema,
    ) -> PaginatedResult[DatasetModel]:
        return await self.dataset_crud.get_many(
            pagination=pagination,
            query_params=query_params,
            owner_id=self.user.id,
        )
