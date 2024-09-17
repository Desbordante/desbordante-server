from uuid import UUID

from internal.domain.task.value_objects import TaskStatus, OneOfTaskConfig, OneOfTaskResult, TaskFailureReason
from internal.dto.repository.base_schema import BaseSchema, BaseCreateSchema, BaseUpdateSchema, \
    BaseResponseSchema, BaseFindSchema


class TaskBaseSchema(BaseSchema):
    status: TaskStatus
    config: OneOfTaskConfig
    dataset_id: UUID


class TaskCreateSchema(TaskBaseSchema, BaseCreateSchema): ...


class TaskUpdateSchema(TaskBaseSchema, BaseUpdateSchema[UUID]):
    result: OneOfTaskResult | None
    raised_exception_name: str | None
    failure_reason: TaskFailureReason | None
    traceback: str | None


class TaskFindSchema(BaseFindSchema[UUID]): ...


class TaskResponseSchema(TaskBaseSchema, BaseResponseSchema[UUID]):
    result: OneOfTaskResult | None = None
    raised_exception_name: str | None = None
    failure_reason: TaskFailureReason | None = None
    traceback: str | None = None
