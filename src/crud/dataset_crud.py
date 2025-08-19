from typing import TypedDict, Unpack
from uuid import UUID

from sqlalchemy import ColumnExpressionArgument, func, select

from src.crud.base_crud import BaseCrud
from src.models.dataset_models import DatasetModel
from src.schemas.base_schemas import PaginatedResult, PaginationParamsSchema
from src.schemas.dataset_schemas import (
    DatasetQueryParamsSchema,
    DatasetsStatsSchema,
    DatasetType,
    TaskStatus,
)


class DatasetFindProps(TypedDict, total=False):
    id: UUID
    owner_id: int
    type: DatasetType
    status: TaskStatus


class DatasetUpdateProps(TypedDict, total=False):
    pass


class DatasetCrud(BaseCrud[DatasetModel, UUID]):
    model = DatasetModel

    async def get_by(self, **kwargs: Unpack[DatasetFindProps]) -> DatasetModel:
        return await super().get_by(**kwargs)

    async def update(
        self, *, entity: DatasetModel, **kwargs: Unpack[DatasetUpdateProps]
    ) -> DatasetModel:
        return await super().update(entity=entity, **kwargs)

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
            self.model.status == query_params.filters.status
            if query_params.filters.status
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
    ) -> PaginatedResult[DatasetModel]:
        return await super().get_many(
            pagination=pagination,
            query_params=query_params,
            **kwargs,
        )

    async def delete(self, *, entity: DatasetModel) -> None:
        return await super().delete(entity=entity)

    async def get_stats(self, *, user_id: int) -> DatasetsStatsSchema:
        query = select(
            func.count(self.model.id),
            func.sum(self.model.size),
        ).where(
            self.model.owner_id == user_id,
        )
        result = await self._session.execute(query)

        row = result.first()

        total_count = row[0] if row and row[0] else 0
        total_size = row[1] if row and row[1] else 0

        return DatasetsStatsSchema(
            total_count=total_count,
            total_size=total_size,
        )

    async def get_by_ids(
        self, *, ids: list[UUID], **kwargs: Unpack[DatasetFindProps]
    ) -> list[DatasetModel]:
        query = select(self.model).filter_by(**kwargs).where(self.model.id.in_(ids))

        result = await self._session.execute(query)

        return list(result.scalars().all())
