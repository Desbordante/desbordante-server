from typing import Protocol

from src.models.dataset_models import DatasetModel
from src.schemas.base_schemas import PaginatedResult, PaginationParamsSchema
from src.schemas.dataset_schemas import DatasetQueryParamsSchema


class DatasetCrud(Protocol):
    async def get_many(
        self,
        *,
        pagination: PaginationParamsSchema,
        query_params: DatasetQueryParamsSchema,
        is_public: bool,
    ) -> PaginatedResult[DatasetModel]: ...


class GetPublicDatasetsUseCase:
    def __init__(
        self,
        *,
        dataset_crud: DatasetCrud,
    ):
        self.dataset_crud = dataset_crud

    async def __call__(
        self,
        *,
        pagination: PaginationParamsSchema,
        query_params: DatasetQueryParamsSchema,
    ) -> PaginatedResult[DatasetModel]:
        return await self.dataset_crud.get_many(
            pagination=pagination,
            query_params=query_params,
            is_public=True,
        )
