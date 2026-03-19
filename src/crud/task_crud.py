from typing import Sequence, TypedDict, Unpack
from uuid import UUID

from sqlalchemy import ColumnExpressionArgument

from src.crud.base_crud import BaseCrud
from src.models.dataset_models import DatasetModel
from src.models.task_models import ProfilingTaskModel
from src.schemas.base_schemas import PaginatedResult, PaginationParamsSchema
from src.schemas.task_schemas.base_schemas import (
    TaskFiltersSchema,
    TaskQueryParamsSchema,
)


class TaskFindProps(TypedDict, total=False):
    id: UUID
    owner_id: int


class TaskCrud(BaseCrud[ProfilingTaskModel]):
    model = ProfilingTaskModel

    async def get_by(self, **kwargs: Unpack[TaskFindProps]) -> ProfilingTaskModel:  # type: ignore
        return await super().get_by(**kwargs)

    def _make_filters(
        self, filters_params: TaskFiltersSchema
    ) -> Sequence[ColumnExpressionArgument[bool] | None]:
        return [
            self.model.datasets.any(DatasetModel.name.icontains(filters_params.search))
            if filters_params.search
            else None,
            self.model.status == filters_params.status
            if filters_params.status
            else None,
            self.model.created_at >= filters_params.created_after
            if filters_params.created_after
            else None,
            self.model.created_at <= filters_params.created_before
            if filters_params.created_before
            else None,
        ]

    async def get_many(  # type: ignore
        self,
        *,
        pagination: PaginationParamsSchema,
        query_params: TaskQueryParamsSchema,
        **kwargs: Unpack[TaskFindProps],
    ) -> PaginatedResult[ProfilingTaskModel]:
        return await super().get_many(
            pagination=pagination,
            query_params=query_params,
            **kwargs,
        )
