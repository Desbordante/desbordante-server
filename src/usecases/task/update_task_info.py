from typing import Protocol, TypedDict, Unpack
from uuid import UUID

from src.domain.task.value_objects import OneOfTaskResult, TaskStatus
from src.domain.task.value_objects.task_failure_reason import TaskFailureReason
from src.models.task_models import TaskModel


class TaskUpdateProps(TypedDict, total=False):
    status: TaskStatus
    result: OneOfTaskResult
    raised_exception_name: str
    failure_reason: TaskFailureReason
    traceback: str


class TaskCrud(Protocol):
    async def get_by(self, *, id: UUID) -> TaskModel: ...
    async def update(
        self,
        *,
        entity: TaskModel,
        **kwargs: Unpack[TaskUpdateProps],
    ) -> TaskModel: ...


class UpdateTaskInfoUseCase:
    def __init__(
        self,
        task_crud: TaskCrud,
    ):
        self._task_crud = task_crud

    async def __call__(
        self,
        *,
        task_id: UUID,
        **kwargs: Unpack[TaskUpdateProps],
    ) -> TaskModel:
        task = await self._task_crud.get_by(id=task_id)

        return await self._task_crud.update(entity=task, **kwargs)
