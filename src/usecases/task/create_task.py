from typing import Protocol
from uuid import UUID

from src.domain.task.tasks import data_profiling_task
from src.models.dataset_models import DatasetModel
from src.models.task_models import TaskModel
from src.schemas.task_schemas.base_schemas import OneOfTaskConfig


class TaskCrud(Protocol):
    async def create(self, *, entity: TaskModel) -> TaskModel: ...


class DatasetCrud(Protocol):
    async def get_by(self, *, id: UUID, owner_id: int) -> DatasetModel: ...


class User(Protocol):
    id: int


class CreateTaskUseCase:
    def __init__(
        self,
        *,
        task_crud: TaskCrud,
        dataset_crud: DatasetCrud,
        user: User,
    ):
        self.task_crud = task_crud
        self.dataset_crud = dataset_crud
        self.user = user

    async def __call__(self, *, dataset_id: UUID, config: OneOfTaskConfig) -> TaskModel:
        dataset = await self.dataset_crud.get_by(
            id=dataset_id,
            owner_id=self.user.id,
        )

        task_entity = TaskModel(
            owner_id=self.user.id,
            dataset_id=dataset.id,
            config=config,
        )

        created_task = await self.task_crud.create(entity=task_entity)

        data_profiling_task.delay(
            task_id=created_task.id,
            dataset_id=dataset_id,
            config=config,
        )

        return created_task
