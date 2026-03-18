import logging
from typing import Protocol, cast
from uuid import UUID

from src.domain.authorization.entities import Actor, Dataset, Task
from src.domain.task.utils import get_primitive_class_by_name
from src.exceptions import BadRequestException, ForbiddenException
from src.models.dataset_models import DatasetModel
from src.models.task_models import ProfilingTaskModel
from src.schemas.base_schemas import TaskStatus
from src.schemas.dataset_schemas import (
    DatasetForTaskSchema,
    DatasetType,
)
from src.schemas.task_schemas.base_schemas import OneOfTaskParams

logger = logging.getLogger(__name__)


class TaskCrud(Protocol):
    async def create(self, entity: ProfilingTaskModel) -> ProfilingTaskModel: ...


class DatasetCrud(Protocol):
    async def get_by_ids(
        self, *, ids: list[UUID], type: DatasetType
    ) -> list[DatasetModel]: ...


class DatasetPolicy(Protocol):
    def can_read(self, actor: Actor, dataset: Dataset) -> bool: ...


class TaskPolicy(Protocol):
    def can_create(self, actor: Actor, task: Task) -> bool: ...


class ProfilingTask(Protocol):
    def run(
        self,
        *,
        params: OneOfTaskParams,
        datasets: list[DatasetForTaskSchema],
        task_id: UUID,
    ) -> None: ...


class CreateTaskUseCase:
    def __init__(
        self,
        *,
        task_crud: TaskCrud,
        dataset_crud: DatasetCrud,
        dataset_policy: DatasetPolicy,
        task_policy: TaskPolicy,
        profiling_task: ProfilingTask,
    ):
        self._task_crud = task_crud
        self._dataset_crud = dataset_crud
        self._dataset_policy = dataset_policy
        self._task_policy = task_policy
        self._profiling_task = profiling_task

    async def __call__(
        self, *, actor: Actor, params: OneOfTaskParams
    ) -> ProfilingTaskModel:
        dataset_ids = list(params.datasets.model_dump().values())

        primitive_class = get_primitive_class_by_name(params.primitive_name)

        datasets = await self._dataset_crud.get_by_ids(
            ids=dataset_ids,
            type=primitive_class.allowed_dataset_type,
        )

        if len(datasets) != len(set(dataset_ids)):
            raise BadRequestException(
                "Some datasets were not found or have invalid type"
            )

        for dataset in datasets:
            if not self._dataset_policy.can_read(
                actor=actor, dataset=cast(Dataset, dataset)
            ):
                raise BadRequestException(
                    "Some datasets were not found or have invalid type"
                )

            if dataset.preprocessing.status != TaskStatus.SUCCESS:
                raise BadRequestException(
                    f"Dataset {dataset.id} preprocessing has inappropriate status"
                )

        task_entity = ProfilingTaskModel(
            owner_id=actor.user_id,
            is_public=actor.user_id is None,
            params=params,
            datasets=datasets,
        )

        if not self._task_policy.can_create(actor, cast(Task, task_entity)):
            raise ForbiddenException("You are not allowed to create this task.")

        created_task = await self._task_crud.create(task_entity)

        self._profiling_task.run(
            params=params,
            datasets=[DatasetForTaskSchema.model_validate(d) for d in datasets],
            task_id=created_task.id,
        )

        return created_task
