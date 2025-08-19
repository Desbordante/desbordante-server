from typing import Protocol
from uuid import UUID

from src.models.task_models import TaskResultModel
from src.models.user_models import UserModel


class TaskResultCrud(Protocol):
    async def get_by(self, *, task_id: UUID) -> TaskResultModel: ...


class GetTaskResultUseCase:
    def __init__(
        self,
        *,
        task_result_crud: TaskResultCrud,
        user: UserModel,
    ):
        self.task_result_crud = task_result_crud
        self.user = user

    async def __call__(
        self,
        *,
        task_id: UUID,
    ) -> TaskResultModel:
        return await self.task_result_crud.get_by(
            task_id=task_id,
        )
