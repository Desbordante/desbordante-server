from typing import Protocol, cast
from uuid import UUID

from src.domain.authorization.entities import Actor, Dataset, Task
from src.domain.task.value_objects import OneOfTaskConfig
from src.exceptions import ForbiddenException, ResourceNotFoundException
from src.models.dataset_models import DatasetModel
from src.models.task_models import TaskModel


class TaskCrud(Protocol):
    async def create(self, *, entity: TaskModel) -> TaskModel: ...


class DatasetCrud(Protocol):
    async def get_by(self, *, id: UUID) -> DatasetModel: ...


class ProfilingTaskWorker(Protocol):
    def set(
        self, *, task_id: UUID, dataset_id: UUID, config: OneOfTaskConfig
    ) -> None: ...


class DatasetPolicy(Protocol):
    def can_read(self, actor: Actor, dataset: Dataset) -> bool: ...


class TaskPolicy(Protocol):
    def can_create(self, actor: Actor, task: Task) -> bool: ...


class CreateTaskUseCase:
    def __init__(
        self,
        *,
        task_crud: TaskCrud,
        dataset_crud: DatasetCrud,
        profiling_task_worker: ProfilingTaskWorker,
        dataset_policy: DatasetPolicy,
        task_policy: TaskPolicy,
    ):
        self._task_crud = task_crud
        self._dataset_crud = dataset_crud
        self._profiling_task_worker = profiling_task_worker
        self._dataset_policy = dataset_policy
        self._task_policy = task_policy

    async def __call__(
        self, *, actor: Actor, dataset_id: UUID, config: OneOfTaskConfig
    ) -> TaskModel:
        dataset = await self._dataset_crud.get_by(id=dataset_id)

        if not self._dataset_policy.can_read(actor, cast(Dataset, dataset)):
            raise ResourceNotFoundException("Dataset not found")

        task_entity = TaskModel(
            owner_id=actor.user_id,
            is_public=actor.user_id is None,
            dataset_id=dataset.id,
            config=config,
        )

        if not self._task_policy.can_create(actor, cast(Task, task_entity)):
            raise ForbiddenException("You are not allowed to create this task.")

        created_task = await self._task_crud.create(entity=task_entity)

        self._profiling_task_worker.set(
            task_id=created_task.id,
            dataset_id=dataset_id,
            config=config,
        )

        return created_task
