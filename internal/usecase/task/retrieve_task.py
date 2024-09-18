import datetime
from typing import Protocol
from uuid import UUID

from pydantic import BaseModel

from internal.domain.task.value_objects import TaskStatus, OneOfTaskConfig, OneOfTaskResult, TaskFailureReason
from internal.dto.repository.task import TaskResponseSchema, TaskFindSchema
from internal.uow import DataStorageContext, UnitOfWork
from internal.usecase.task.exception import TaskNotFoundException


class TaskRepo(Protocol):

    def find(self, task_info: TaskFindSchema, context: DataStorageContext) -> TaskResponseSchema | None: ...


class RetrieveTaskUseCaseResult(BaseModel):
    task_id: UUID
    status: TaskStatus
    config: OneOfTaskConfig
    result: OneOfTaskResult | None
    dataset_id: UUID

    raised_exception_name: str | None
    failure_reason: TaskFailureReason | None
    traceback: str | None

    created_at: datetime.datetime | None
    updated_at: datetime.datetime | None


class RetrieveTask:

    def __init__(self, unit_of_work: UnitOfWork, task_repo: TaskRepo):
        self.unit_of_work = unit_of_work
        self.task_repo = task_repo

    def __call__(self, task_id: UUID) -> RetrieveTaskUseCaseResult:
        task_find_schema = TaskFindSchema(id=task_id)

        with self.unit_of_work as context:
            task = self.task_repo.find(task_find_schema, context)

        if not task:
            raise TaskNotFoundException()

        return RetrieveTaskUseCaseResult(
            task_id=task.id,
            status=task.status,
            config=task.config,
            result=task.result,
            dataset_id=task.dataset_id,
            raised_exception_name=task.raised_exception_name,
            failure_reason=task.failure_reason,
            traceback=task.traceback,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
