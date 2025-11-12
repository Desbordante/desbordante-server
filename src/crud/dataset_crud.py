from typing import Sequence, TypedDict, Unpack
from uuid import UUID

from sqlalchemy import ColumnExpressionArgument, func, select

from src.crud.base_crud import BaseCrud
from src.models.dataset_models import DatasetModel
from src.schemas.base_schemas import PaginatedResult, PaginationParamsSchema
from src.schemas.dataset_schemas import (
    DatasetFiltersSchema,
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
    is_public: bool


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
        self, filters_params: DatasetFiltersSchema
    ) -> Sequence[ColumnExpressionArgument[bool] | None]:
        return [
            self.model.name.icontains(filters_params.search)
            if filters_params.search
            else None,
            self.model.type == filters_params.type if filters_params.type else None,
            self.model.status == filters_params.status
            if filters_params.status
            else None,
            self.model.is_public == filters_params.is_public
            if filters_params.is_public is not None
            else None,
            self.model.size >= filters_params.min_size
            if filters_params.min_size
            else None,
            self.model.size <= filters_params.max_size
            if filters_params.max_size
            else None,
            self.model.created_at >= filters_params.created_after
            if filters_params.created_after
            else None,
            self.model.created_at <= filters_params.created_before
            if filters_params.created_before
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
            ~self.model.is_public,
        )
        result = await self._session.execute(query)

        row = result.first()

        total_count = row[0] if row and row[0] else 0
        total_size = row[1] if row and row[1] else 0

        return DatasetsStatsSchema(
            total_count=total_count,
            total_size=total_size,
        )

    async def get_public_stats(self) -> DatasetsStatsSchema:
        query = select(
            func.count(self.model.id),
            func.sum(self.model.size),
        ).where(
            self.model.is_public,
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
