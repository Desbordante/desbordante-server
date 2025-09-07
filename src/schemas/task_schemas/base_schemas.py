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
from src.schemas.task_schemas.adc.task_params import AdcTaskParams
from src.schemas.task_schemas.adc.task_result import (
    AdcSchema,
    AdcTaskResultFiltersSchema,
    AdcTaskResultOrderingField,
)
from src.schemas.task_schemas.afd.task_params import AfdTaskParams
from src.schemas.task_schemas.afd.task_result import (
    AfdSchema,
    AfdTaskResultFiltersSchema,
    AfdTaskResultOrderingField,
)
from src.schemas.task_schemas.afd_verification.task_params import (
    AfdVerificationTaskParams,
)
from src.schemas.task_schemas.afd_verification.task_result import (
    AfdVerificationSchema,
    AfdVerificationTaskResultFiltersSchema,
    AfdVerificationTaskResultOrderingField,
)
from src.schemas.task_schemas.ar.task_params import ArTaskParams
from src.schemas.task_schemas.ar.task_result import (
    ArSchema,
    ArTaskResultFiltersSchema,
    ArTaskResultOrderingField,
)
from src.schemas.task_schemas.dd.task_params import DdTaskParams
from src.schemas.task_schemas.dd.task_result import (
    DdSchema,
    DdTaskResultFiltersSchema,
    DdTaskResultOrderingField,
)
from src.schemas.task_schemas.fd.task_params import FdTaskParams
from src.schemas.task_schemas.fd.task_result import (
    FdSchema,
    FdTaskResultFiltersSchema,
    FdTaskResultOrderingField,
)
from src.schemas.task_schemas.md.task_params import MdTaskParams
from src.schemas.task_schemas.md.task_result import (
    MdSchema,
    MdTaskResultFiltersSchema,
    MdTaskResultOrderingField,
)
from src.schemas.task_schemas.mfd_verification.task_params import (
    MfdVerificationTaskParams,
)
from src.schemas.task_schemas.mfd_verification.task_result import (
    MfdVerificationSchema,
    MfdVerificationTaskResultFiltersSchema,
    MfdVerificationTaskResultOrderingField,
)
from src.schemas.task_schemas.nar.task_params import NarTaskParams
from src.schemas.task_schemas.nar.task_result import (
    NarSchema,
    NarTaskResultFiltersSchema,
    NarTaskResultOrderingField,
)
from src.schemas.task_schemas.pfd.task_params import PfdTaskParams
from src.schemas.task_schemas.pfd.task_result import (
    PfdSchema,
    PfdTaskResultFiltersSchema,
    PfdTaskResultOrderingField,
)
from src.schemas.task_schemas.types import PrimitiveName

OneOfTaskParams = Annotated[
    Union[
        FdTaskParams,
        AfdTaskParams,
        AcTaskParams,
        AdcTaskParams,
        AfdVerificationTaskParams,
        ArTaskParams,
        DdTaskParams,
        MdTaskParams,
        MfdVerificationTaskParams,
        NarTaskParams,
        PfdTaskParams,
    ],
    Field(discriminator="primitive_name"),
]


OneOfTaskResult = Union[
    FdSchema,
    AfdSchema,
    AcSchema,
    AdcSchema,
    AfdVerificationSchema,
    ArSchema,
    DdSchema,
    MdSchema,
    MfdVerificationSchema,
    NarSchema,
    PfdSchema,
]


class PaginatedTaskResponseSchema[T: BaseSchema, P: PrimitiveName](
    PaginatedResponseSchema[T]
):
    primitive_name: P


OneOfPaginatedTaskResponseSchema = Annotated[
    Union[
        PaginatedTaskResponseSchema[FdSchema, Literal[PrimitiveName.FD]],
        PaginatedTaskResponseSchema[AfdSchema, Literal[PrimitiveName.AFD]],
        PaginatedTaskResponseSchema[AcSchema, Literal[PrimitiveName.AC]],
        PaginatedTaskResponseSchema[AdcSchema, Literal[PrimitiveName.ADC]],
        PaginatedTaskResponseSchema[
            AfdVerificationSchema, Literal[PrimitiveName.AFD_VERIFICATION]
        ],
        PaginatedTaskResponseSchema[ArSchema, Literal[PrimitiveName.AR]],
        PaginatedTaskResponseSchema[DdSchema, Literal[PrimitiveName.DD]],
        PaginatedTaskResponseSchema[MdSchema, Literal[PrimitiveName.MD]],
        PaginatedTaskResponseSchema[
            MfdVerificationSchema, Literal[PrimitiveName.MFD_VERIFICATION]
        ],
        PaginatedTaskResponseSchema[NarSchema, Literal[PrimitiveName.NAR]],
        PaginatedTaskResponseSchema[PfdSchema, Literal[PrimitiveName.PFD]],
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


class TaskResultOrderingField(StrEnum):
    _ignore_ = "member cls"
    cls = vars()  # type: ignore
    for member in chain(
        list(AfdTaskResultOrderingField),
        list(FdTaskResultOrderingField),
        list(AcTaskResultOrderingField),
        list(AdcTaskResultOrderingField),
        list(AfdVerificationTaskResultOrderingField),
        list(ArTaskResultOrderingField),
        list(DdTaskResultOrderingField),
        list(MdTaskResultOrderingField),
        list(MfdVerificationTaskResultOrderingField),
        list(NarTaskResultOrderingField),
        list(PfdTaskResultOrderingField),
    ):
        if member.name not in cls:
            cls[member.name] = member.value


OneOfTaskResultFiltersSchema = Union[
    Annotated[AfdTaskResultFiltersSchema, Depends()],
    Annotated[FdTaskResultFiltersSchema, Depends()],
    Annotated[AcTaskResultFiltersSchema, Depends()],
    Annotated[AdcTaskResultFiltersSchema, Depends()],
    Annotated[AfdVerificationTaskResultFiltersSchema, Depends()],
    Annotated[ArTaskResultFiltersSchema, Depends()],
    Annotated[DdTaskResultFiltersSchema, Depends()],
    Annotated[MdTaskResultFiltersSchema, Depends()],
    Annotated[MfdVerificationTaskResultFiltersSchema, Depends()],
    Annotated[NarTaskResultFiltersSchema, Depends()],
    Annotated[PfdTaskResultFiltersSchema, Depends()],
]


class TaskResultQueryParamsSchema[T = OneOfTaskResultFiltersSchema](BaseSchema):
    filters: T

    ordering: Annotated[
        OrderingParamsSchema[TaskResultOrderingField],
        Depends(),
    ]


OneOfTaskResultOrderingField = Union[
    AfdTaskResultOrderingField,
    FdTaskResultOrderingField,
    AcTaskResultOrderingField,
    AdcTaskResultOrderingField,
    AfdVerificationTaskResultOrderingField,
    ArTaskResultOrderingField,
    DdTaskResultOrderingField,
    MdTaskResultOrderingField,
    MfdVerificationTaskResultOrderingField,
    NarTaskResultOrderingField,
    PfdTaskResultOrderingField,
]
