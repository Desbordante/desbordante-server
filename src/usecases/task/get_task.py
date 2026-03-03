from typing import Protocol, cast
from uuid import UUID

from src.domain.authorization.entities import Actor, Task
from src.exceptions import ResourceNotFoundException
from src.models.task_models import TaskModel


class TaskCrud(Protocol):
    async def get_by(self, *, id: UUID) -> TaskModel: ...


class TaskPolicy(Protocol):
    def can_read(self, actor: Actor, task: Task) -> bool: ...


class GetTaskUseCase:
    def __init__(
        self,
        *,
        task_crud: TaskCrud,
        task_policy: TaskPolicy,
    ):
        self._task_crud = task_crud
        self._task_policy = task_policy

    async def __call__(
        self,
        *,
        id: UUID,
        actor: Actor,
    ) -> TaskModel:
        task = await self._task_crud.get_by(id=id)

        if not self._task_policy.can_read(actor, cast(Task, task)):
            raise ResourceNotFoundException("Task not found")

        return task
