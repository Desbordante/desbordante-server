from typing import Protocol
from uuid import UUID

from src.models.task_models import TaskModel
from src.models.user_models import UserModel


class TaskCrud(Protocol):
    async def get_by(self, *, id: UUID, owner_id: int) -> TaskModel: ...


class GetTaskUseCase:
    def __init__(
        self,
        *,
        task_crud: TaskCrud,
        user: UserModel,
    ):
        self.task_crud = task_crud
        self.user = user

    async def __call__(
        self,
        *,
        id: UUID,
    ) -> TaskModel:
        return await self.task_crud.get_by(
            owner_id=self.user.id,
            id=id,
        )
