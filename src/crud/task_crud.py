from typing import TypedDict, Unpack
from uuid import UUID

from sqlalchemy import ColumnExpressionArgument

from src.crud.base_crud import BaseCrud
from src.models.dataset_models import DatasetModel
from src.models.task_models import TaskModel
from src.schemas.base_schemas import PaginatedResult, PaginationParamsSchema
from src.schemas.task_schemas.base_schemas import TaskQueryParamsSchema


class TaskFindProps(TypedDict, total=False):
    id: UUID
    owner_id: int


class TaskUpdateProps(TypedDict, total=False):
    pass


class TaskCrud(BaseCrud[TaskModel, UUID]):
    model = TaskModel

    async def get_by(self, **kwargs: Unpack[TaskFindProps]) -> TaskModel:
        return await super().get_by(**kwargs)

    async def update(
        self, *, entity: TaskModel, **kwargs: Unpack[TaskUpdateProps]
    ) -> TaskModel:
        return await super().update(entity=entity, **kwargs)

    def _make_filters(
        self, query_params: TaskQueryParamsSchema
    ) -> list[ColumnExpressionArgument[bool] | None]:
        return [
            self.model.datasets.any(DatasetModel.name.icontains(query_params.search))
            if query_params.search
            else None,
            self.model.status == query_params.filters.status
            if query_params.filters.status
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
        query_params: TaskQueryParamsSchema,
        **kwargs: Unpack[TaskFindProps],
    ) -> PaginatedResult[TaskModel]:
        return await super().get_many(
            pagination=pagination,
            query_params=query_params,
            **kwargs,
        )
