from typing import Protocol
from uuid import UUID


from internal.uow import DataStorageContext, UnitOfWork
from internal.domain.task.value_objects import TaskStatus, OneOfTaskResult
from internal.dto.repository.task import (
    TaskUpdateSchema,
    TaskResponseSchema,
    TaskFindSchema,
)
from internal.dto.repository.task.task import TaskNotFoundException
from internal.usecase.task.exception import (
    TaskNotFoundException as TaskNotFoundUseCaseException,
)


class TaskRepo(Protocol):

    def update(
        self,
        find_schema: TaskFindSchema,
        update_schema: TaskUpdateSchema,
        fields_to_update_if_none: set[str] | None,
        context: DataStorageContext,
    ) -> TaskResponseSchema: ...


class UpdateTaskInfo:

    def __init__(
        self,
        unit_of_work: UnitOfWork,
        task_repo: TaskRepo,
    ):

        self.unit_of_work = unit_of_work
        self.task_repo = task_repo

    def __call__(
        self,
        *,
        task_id: UUID,
        fields_to_update_if_none: set[str] | None = None,
        task_status: TaskStatus | None = None,
        result: OneOfTaskResult | None = None,
        raised_exception_name: str | None = None,
        failure_reason: str | None = None,
        traceback: str | None = None,
    ) -> None:

        task_find_schema = TaskFindSchema(id=task_id)
        data_to_update = TaskUpdateSchema(
            status=task_status,
            result=result,
            raised_exception_name=raised_exception_name,
            failure_reason=failure_reason,
            traceback=traceback,
        )  # type: ignore

        with self.unit_of_work as context:
            try:
                self.task_repo.update(
                    task_find_schema, data_to_update, fields_to_update_if_none, context
                )
            except TaskNotFoundException:
                raise TaskNotFoundUseCaseException()
