from datetime import datetime
from typing import Annotated, Literal, Union
from uuid import UUID

from pydantic import Field

from src.schemas.base_schemas import (
    BaseSchema,
    QueryParamsSchema,
    TaskErrorSchema,
    TaskStatus,
)
from src.schemas.dataset_schemas import DatasetSchema
from src.schemas.task_schemas.afd.task_params import AFdTaskParams
from src.schemas.task_schemas.fd.task_params import FdTaskParams

OneOfTaskParams = Annotated[
    Union[FdTaskParams, AFdTaskParams],
    Field(discriminator="primitive_name"),
]


class FdTaskResult(BaseSchema):
    primitive_name: str


class AfdTaskResult(BaseSchema):
    primitive_name: str


OneOfTaskResult = FdTaskResult | AfdTaskResult | TaskErrorSchema


class TaskSchema(BaseSchema):
    id: UUID

    params: OneOfTaskParams

    status: TaskStatus

    datasets: list[DatasetSchema]

    created_at: datetime
    updated_at: datetime


class TaskFiltersSchema(BaseSchema):
    status: TaskStatus | None = None
    created_after: datetime | None = None
    created_before: datetime | None = None


TaskQueryParamsSchema = QueryParamsSchema[
    TaskFiltersSchema, Literal["status", "created_at"]
]


class TaskResultSchema(BaseSchema):
    task: TaskSchema

    result: OneOfTaskResult
