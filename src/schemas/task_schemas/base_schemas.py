from datetime import datetime
from enum import StrEnum
from typing import Annotated, Literal, Union
from uuid import UUID

from pydantic import Field

from src.schemas.base_schemas import (
    BaseSchema,
    QueryParamsSchema,
    TaskStatus,
)
from src.schemas.dataset_schemas import DatasetSchema
from src.schemas.task_schemas.afd.task_params import AFdTaskParams
from src.schemas.task_schemas.afd.task_result import (
    AfdSchema,
    AfdTaskResultFiltersSchema,
    AfdTaskResultOrderingField,
)
from src.schemas.task_schemas.fd.task_params import FdTaskParams
from src.schemas.task_schemas.fd.task_result import (
    FdSchema,
    FdTaskResultFiltersSchema,
    FdTaskResultOrderingField,
)

OneOfTaskParams = Annotated[
    Union[FdTaskParams, AFdTaskParams],
    Field(discriminator="primitive_name"),
]


OneOfTaskResult = FdSchema | AfdSchema


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


class TaskResultFiltersSchema(AfdTaskResultFiltersSchema, FdTaskResultFiltersSchema):
    pass


TaskResultOrderingField = StrEnum(
    "TaskResultOrderingField",
    {
        **{item.name: item.value for item in AfdTaskResultOrderingField},
        **{item.name: item.value for item in FdTaskResultOrderingField},
    },
)


TaskResultQueryParamsSchema = QueryParamsSchema[
    TaskResultFiltersSchema,
    TaskResultOrderingField,
]

OneOfTaskResultFilter = AfdTaskResultFiltersSchema | FdTaskResultFiltersSchema
OneOfTaskResultOrderingField = AfdTaskResultOrderingField | FdTaskResultOrderingField
