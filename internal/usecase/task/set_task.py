from typing import Protocol
from uuid import UUID

from internal.domain.task.value_objects import OneOfTaskConfig, TaskStatus
from internal.dto.repository.file import DatasetResponseSchema, DatasetFindSchema
from internal.dto.repository.task import TaskCreateSchema, TaskResponseSchema
from internal.dto.worker.task import ProfilingTaskCreateSchema
from internal.uow import DataStorageContext, UnitOfWork
from internal.usecase.file.exception import DatasetNotFoundException


class DatasetRepo(Protocol):

    def find(
        self, dataset_info: DatasetFindSchema, context: DataStorageContext
    ) -> DatasetResponseSchema | None: ...


class TaskRepo(Protocol):

    def create(
        self, task_info: TaskCreateSchema, context: DataStorageContext
    ) -> TaskResponseSchema: ...


class ProfilingTaskWorker(Protocol):

    def set(self, task_info: ProfilingTaskCreateSchema) -> None: ...


class SetTask:

    def __init__(
        self,
        unit_of_work: UnitOfWork,
        dataset_repo: DatasetRepo,
        task_repo: TaskRepo,
        profiling_task_worker: ProfilingTaskWorker,
    ):

        self.unit_of_work = unit_of_work
        self.dataset_repo = dataset_repo
        self.task_repo = task_repo
        self.profiling_task_worker = profiling_task_worker

    def __call__(
        self,
        *,
        dataset_id: UUID,
        config: OneOfTaskConfig,
    ) -> UUID:

        dataset_find_schema = DatasetFindSchema(id=dataset_id)
        task_create_schema = TaskCreateSchema(
            status=TaskStatus.CREATED,
            config=config,
            dataset_id=dataset_id,
        )

        with self.unit_of_work as context:
            dataset = self.dataset_repo.find(dataset_find_schema, context)
            if not dataset:
                raise DatasetNotFoundException()
            task = self.task_repo.create(task_create_schema, context)

        profiling_task_create_schema = ProfilingTaskCreateSchema(
            task_id=task.id, dataset_id=dataset_id, config=config
        )
        self.profiling_task_worker.set(profiling_task_create_schema)

        return task.id
