from typing import Protocol
from uuid import UUID

from src.exceptions import ForbiddenException
from src.models.task_models import TaskModel


class TaskCrud(Protocol):
    async def get_by(self, *, id: UUID, owner_id: int | None = None) -> TaskModel: ...


class User(Protocol):
    id: int
    is_admin: bool


class GetTaskUseCase:
    def __init__(
        self,
        *,
        task_crud: TaskCrud,
        user: User,
    ):
        self.task_crud = task_crud
        self.user = user

    async def __call__(
        self,
        *,
        id: UUID,
    ) -> TaskModel:
        task = await self.task_crud.get_by(id=id)

        if task.owner_id != self.user.id and not self.user.is_admin:
            raise ForbiddenException("Access denied")

        return task
