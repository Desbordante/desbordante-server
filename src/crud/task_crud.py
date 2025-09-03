from typing import Sequence, TypedDict, Unpack
from uuid import UUID

from sqlalchemy import ColumnExpressionArgument

from src.crud.base_crud import BaseCrud
from src.models.dataset_models import DatasetModel
from src.models.task_models import TaskModel
from src.models.task_result_models import TaskResultModel
from src.schemas.base_schemas import PaginatedResult, PaginationParamsSchema
from src.schemas.task_schemas.base_schemas import (
    TaskFiltersSchema,
    TaskQueryParamsSchema,
)


class TaskFindProps(TypedDict, total=False):
    id: UUID
    owner_id: int


class TaskUpdateProps(TypedDict, total=False):
    results: list[TaskResultModel]


class TaskCrud(BaseCrud[TaskModel, UUID]):
    model = TaskModel

    async def get_by(self, **kwargs: Unpack[TaskFindProps]) -> TaskModel:
        return await super().get_by(**kwargs)

    async def update(
        self, *, entity: TaskModel, **kwargs: Unpack[TaskUpdateProps]
    ) -> TaskModel:
        return await super().update(entity=entity, **kwargs)

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

    async def get_many(
        self,
        *,
        pagination: PaginationParamsSchema,
        query_params: TaskQueryParamsSchema,
        **kwargs: Unpack[TaskFindProps],
    ) -> PaginatedResult[TaskModel]:
        return await super().get_many(
            pagination=pagination,
            query_params=query_params,
            **kwargs,
        )
