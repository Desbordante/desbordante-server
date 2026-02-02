from typing import TypedDict, Unpack
from uuid import UUID


from src.crud.base_crud import BaseCrud
from src.models.task_models import TaskModel


class TaskFindProps(TypedDict, total=False):
    id: UUID
    owner_id: int


class TaskCrud(BaseCrud[TaskModel, UUID]):
    model = TaskModel

    async def get_by(self, **kwargs: Unpack[TaskFindProps]) -> TaskModel:
        return await super().get_by(**kwargs)
