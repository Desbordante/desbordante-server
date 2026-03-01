from datetime import datetime
from typing import Annotated, Literal, Union
from uuid import UUID

from pydantic import Field

from src.domain.task.value_objects import (
    OneOfTaskConfig,
    OneOfTaskResult,
    TaskStatus,
)
from src.domain.task.value_objects.task_failure_reason import TaskFailureReason
from src.schemas.base_schemas import BaseSchema
from src.schemas.dataset_schemas import DatasetSchema


class BaseTaskSchema(BaseSchema):
    id: UUID
    config: OneOfTaskConfig
    dataset: DatasetSchema
    created_at: datetime
    updated_at: datetime


class ProcessingTaskSchema(BaseTaskSchema):
    status: Literal[TaskStatus.PENDING] | Literal[TaskStatus.PROCESSING]
    result: None


class FailedTaskSchema(BaseTaskSchema):
    status: Literal[TaskStatus.FAILED]
    result: None
    raised_exception_name: str
    failure_reason: TaskFailureReason
    traceback: str


class SuccessTaskSchema(BaseTaskSchema):
    status: Literal[TaskStatus.SUCCESS]
    result: OneOfTaskResult


TaskSchema = Annotated[
    Union[ProcessingTaskSchema, FailedTaskSchema, SuccessTaskSchema],
    Field(discriminator="status"),
]
