from datetime import datetime
from enum import StrEnum
from itertools import chain
from typing import Annotated, Literal, Union
from uuid import UUID

from fastapi import Depends
from pydantic import Field

from src.schemas.base_schemas import (
    BaseSchema,
    FiltersParamsSchema,
    OrderingParamsSchema,
    PaginatedResponseSchema,
    QueryParamsSchema,
    TaskStatus,
)
from src.schemas.dataset_schemas import DatasetSchema
from src.schemas.task_schemas.ac.task_params import AcTaskParams
from src.schemas.task_schemas.ac.task_result import (
    AcSchema,
    AcTaskResultFiltersSchema,
    AcTaskResultOrderingField,
)
from src.schemas.task_schemas.afd.task_params import AfdTaskParams
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
from src.schemas.task_schemas.types import PrimitiveName

OneOfTaskParams = Annotated[
    Union[FdTaskParams, AfdTaskParams, AcTaskParams],
    Field(discriminator="primitive_name"),
]


OneOfTaskResult = FdSchema | AfdSchema | AcSchema


class PaginatedTaskResponseSchema[T: BaseSchema, P: PrimitiveName](
    PaginatedResponseSchema[T]
):
    primitive_name: P


OneOfPaginatedTaskResponseSchema = Annotated[
    Union[
        PaginatedTaskResponseSchema[FdSchema, Literal[PrimitiveName.FD]],
        PaginatedTaskResponseSchema[AfdSchema, Literal[PrimitiveName.AFD]],
        PaginatedTaskResponseSchema[AcSchema, Literal[PrimitiveName.AC]],
    ],
    Field(discriminator="primitive_name"),
]


class TaskSchema(BaseSchema):
    id: UUID

    params: OneOfTaskParams

    status: TaskStatus

    datasets: list[DatasetSchema]

    created_at: datetime
    updated_at: datetime


class TaskFiltersSchema(FiltersParamsSchema):
    status: TaskStatus | None = None
    created_after: datetime | None = None
    created_before: datetime | None = None


TaskQueryParamsSchema = QueryParamsSchema[
    TaskFiltersSchema, Literal["status", "created_at"]
]


class TaskResultFiltersSchema(
    AfdTaskResultFiltersSchema, FdTaskResultFiltersSchema, AcTaskResultFiltersSchema
): ...


class TaskResultOrderingField(StrEnum):
    _ignore_ = "member cls"
    cls = vars()  # type: ignore
    for member in chain(
        list(AfdTaskResultOrderingField),
        list(FdTaskResultOrderingField),
        list(AcTaskResultOrderingField),
    ):
        if member.name not in cls:
            cls[member.name] = member.value


OneOfTaskResultFiltersSchema = Union[
    Annotated[AfdTaskResultFiltersSchema, Depends()],
    Annotated[FdTaskResultFiltersSchema, Depends()],
    Annotated[AcTaskResultFiltersSchema, Depends()],
]


class TaskResultQueryParamsSchema[T = OneOfTaskResultFiltersSchema](BaseSchema):
    filters: T

    ordering: Annotated[
        OrderingParamsSchema[TaskResultOrderingField],
        Depends(),
    ]


OneOfTaskResultOrderingField = Union[
    AfdTaskResultOrderingField, FdTaskResultOrderingField, AcTaskResultOrderingField
]
