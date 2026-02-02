from datetime import datetime
from typing import Annotated, Literal, Union
from uuid import UUID

from pydantic import Field

from src.schemas.base_schemas import BaseSchema, TaskErrorSchema, TaskStatus
from src.schemas.dataset_schemas import DatasetSchema
from src.schemas.task_schemas.primitives.afd import AfdTaskConfig, AfdTaskResult
from src.schemas.task_schemas.primitives.fd import FdTaskConfig, FdTaskResult

OneOfTaskConfig = Annotated[
    Union[
        FdTaskConfig,
        AfdTaskConfig,
    ],
    Field(discriminator="primitive_name"),
]

OneOfTaskResult = Annotated[
    Union[
        FdTaskResult,
        AfdTaskResult,
    ],
    Field(discriminator="primitive_name"),
]


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
    result: TaskErrorSchema


class SuccessTaskSchema(BaseTaskSchema):
    status: Literal[TaskStatus.SUCCESS]
    result: OneOfTaskResult


TaskSchema = Annotated[
    Union[ProcessingTaskSchema, FailedTaskSchema, SuccessTaskSchema],
    Field(discriminator="status"),
]
