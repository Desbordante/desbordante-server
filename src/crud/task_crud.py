from typing import TypedDict, Unpack
from uuid import UUID

from src.crud.base_crud import BaseCrud
from src.domain.task.value_objects import OneOfTaskResult
from src.domain.task.value_objects.task_failure_reason import TaskFailureReason
from src.domain.task.value_objects.task_status import TaskStatus
from src.models.task_models import TaskModel


class TaskFindProps(TypedDict, total=False):
    id: UUID
    owner_id: int


class TaskUpdateProps(TypedDict, total=False):
    status: TaskStatus
    result: OneOfTaskResult
    raised_exception_name: str
    failure_reason: TaskFailureReason
    traceback: str


class TaskCrud(BaseCrud[TaskModel]):
    model = TaskModel

    async def get_by(self, **kwargs: Unpack[TaskFindProps]) -> TaskModel:  # type: ignore
        return await super().get_by(**kwargs)

    async def update(
        self, *, entity: TaskModel, **kwargs: Unpack[TaskUpdateProps]
    ) -> TaskModel:  # type: ignore
        return await super().update(entity=entity, **kwargs)
