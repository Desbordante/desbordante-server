from typing import TypedDict, Unpack
from uuid import UUID

from sqlalchemy import ColumnExpressionArgument, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.base_crud import BaseCrud
from src.models.dataset_models import DatasetModel
from src.schemas.base_schemas import PaginationParamsSchema
from src.schemas.dataset_schemas import DatasetQueryParamsSchema


class DatasetFindProps(TypedDict, total=False):
    id: UUID
    owner_id: int


class DatasetUpdateProps(TypedDict, total=False):
    pass


class DatasetCrud(BaseCrud[DatasetModel, UUID]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=DatasetModel, session=session)

    async def get_by(self, **kwargs: Unpack[DatasetFindProps]) -> DatasetModel:
        return await super().get_by(**kwargs)

    async def update(
        self, *, entity: DatasetModel, **kwargs: Unpack[DatasetUpdateProps]
    ) -> DatasetModel:
        return await super().update(entity=entity, **kwargs)

    async def get_user_datasets_size(self, *, owner_id: int) -> int:
        query = select(func.sum(self.model.size)).where(
            self.model.owner_id == owner_id,
        )
        result = await self._session.execute(query)
        return result.scalar() or 0

    def _make_filters(
        self, query_params: DatasetQueryParamsSchema
    ) -> list[ColumnExpressionArgument[bool] | None]:
        return [
            self.model.name.icontains(query_params.search)
            if query_params.search
            else None,
            self.model.type == query_params.filters.type
            if query_params.filters.type
            else None,
            self.model.size >= query_params.filters.min_size
            if query_params.filters.min_size
            else None,
            self.model.size <= query_params.filters.max_size
            if query_params.filters.max_size
            else None,
            self.model.created_at >= query_params.filters.created_after
            if query_params.filters.created_after
            else None,
            self.model.created_at <= query_params.filters.created_before
            if query_params.filters.created_before
            else None,
        ]

    async def get_many(
        self,
        *,
        pagination: PaginationParamsSchema,
        query_params: DatasetQueryParamsSchema,
        **kwargs: Unpack[DatasetFindProps],
    ) -> list[DatasetModel]:
        return await super().get_many(
            pagination=pagination,
            query_params=query_params,
            **kwargs,
        )

    async def delete(self, *, entity: DatasetModel) -> None:
        return await super().delete(entity=entity)
