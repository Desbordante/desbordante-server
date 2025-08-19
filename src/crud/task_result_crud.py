from typing import TypedDict, Unpack
from uuid import UUID

from src.crud.base_crud import BaseCrud
from src.models.task_models import TaskResultModel


class TaskResultFindProps(TypedDict, total=False):
    id: UUID
    task_id: UUID


class TaskResultUpdateProps(TypedDict, total=False):
    pass


class TaskResultCrud(BaseCrud[TaskResultModel, UUID]):
    model = TaskResultModel

    async def get_by(self, **kwargs: Unpack[TaskResultFindProps]) -> TaskResultModel:
        return await super().get_by(**kwargs)

    async def update(
        self, *, entity: TaskResultModel, **kwargs: Unpack[TaskResultUpdateProps]
    ) -> TaskResultModel:
        return await super().update(entity=entity, **kwargs)
