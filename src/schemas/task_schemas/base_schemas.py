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
    TaskErrorSchema,
    TaskStatus,
)
from src.schemas.dataset_schemas import DatasetSchema
from src.schemas.task_schemas.primitives.ac.task_params import AcTaskParams
from src.schemas.task_schemas.primitives.ac.task_result import (
    AcTaskResultFiltersSchema,
    AcTaskResultItemSchema,
    AcTaskResultOrderingField,
    AcTaskResultSchema,
)
from src.schemas.task_schemas.primitives.adc.task_params import AdcTaskParams
from src.schemas.task_schemas.primitives.adc.task_result import (
    AdcTaskResultFiltersSchema,
    AdcTaskResultItemSchema,
    AdcTaskResultOrderingField,
    AdcTaskResultSchema,
)
from src.schemas.task_schemas.primitives.afd.task_params import AfdTaskParams
from src.schemas.task_schemas.primitives.afd.task_result import (
    AfdTaskResultFiltersSchema,
    AfdTaskResultItemSchema,
    AfdTaskResultOrderingField,
    AfdTaskResultSchema,
)
from src.schemas.task_schemas.primitives.afd_verification.task_params import (
    AfdVerificationTaskParams,
)
from src.schemas.task_schemas.primitives.afd_verification.task_result import (
    AfdVerificationTaskResultFiltersSchema,
    AfdVerificationTaskResultItemSchema,
    AfdVerificationTaskResultOrderingField,
    AfdVerificationTaskResultSchema,
)
from src.schemas.task_schemas.primitives.ar.task_params import ArTaskParams
from src.schemas.task_schemas.primitives.ar.task_result import (
    ArTaskResultFiltersSchema,
    ArTaskResultItemSchema,
    ArTaskResultOrderingField,
    ArTaskResultSchema,
)
from src.schemas.task_schemas.primitives.base_schemas import BaseTaskResultSchema
from src.schemas.task_schemas.primitives.dd.task_params import DdTaskParams
from src.schemas.task_schemas.primitives.dd.task_result import (
    DdTaskResultFiltersSchema,
    DdTaskResultItemSchema,
    DdTaskResultOrderingField,
    DdTaskResultSchema,
)
from src.schemas.task_schemas.primitives.fd.task_params import FdTaskParams
from src.schemas.task_schemas.primitives.fd.task_result import (
    FdTaskResultFiltersSchema,
    FdTaskResultItemSchema,
    FdTaskResultOrderingField,
    FdTaskResultSchema,
)
from src.schemas.task_schemas.primitives.fd_verification.task_params import (
    FdVerificationTaskParams,
)
from src.schemas.task_schemas.primitives.fd_verification.task_result import (
    FdVerificationTaskResultFiltersSchema,
    FdVerificationTaskResultItemSchema,
    FdVerificationTaskResultOrderingField,
    FdVerificationTaskResultSchema,
)
from src.schemas.task_schemas.primitives.md.task_params import MdTaskParams
from src.schemas.task_schemas.primitives.md.task_result import (
    MdTaskResultFiltersSchema,
    MdTaskResultItemSchema,
    MdTaskResultOrderingField,
    MdTaskResultSchema,
)
from src.schemas.task_schemas.primitives.mfd_verification.task_params import (
    MfdVerificationTaskParams,
)
from src.schemas.task_schemas.primitives.mfd_verification.task_result import (
    MfdVerificationTaskResultFiltersSchema,
    MfdVerificationTaskResultItemSchema,
    MfdVerificationTaskResultOrderingField,
    MfdVerificationTaskResultSchema,
)
from src.schemas.task_schemas.primitives.nar.task_params import NarTaskParams
from src.schemas.task_schemas.primitives.nar.task_result import (
    NarTaskResultFiltersSchema,
    NarTaskResultItemSchema,
    NarTaskResultOrderingField,
    NarTaskResultSchema,
)
from src.schemas.task_schemas.primitives.pfd.task_params import PfdTaskParams
from src.schemas.task_schemas.primitives.pfd.task_result import (
    PfdTaskResultFiltersSchema,
    PfdTaskResultItemSchema,
    PfdTaskResultOrderingField,
    PfdTaskResultSchema,
)
from src.schemas.task_schemas.types import PrimitiveName

OneOfTaskParams = Annotated[
    Union[
        FdTaskParams,
        AfdTaskParams,
        AcTaskParams,
        AdcTaskParams,
        AfdVerificationTaskParams,
        FdVerificationTaskParams,
        ArTaskParams,
        DdTaskParams,
        MdTaskParams,
        MfdVerificationTaskParams,
        NarTaskParams,
        PfdTaskParams,
    ],
    Field(discriminator="primitive_name"),
]


OneOfTaskResultItemSchema = Union[
    FdTaskResultItemSchema,
    AfdTaskResultItemSchema,
    AcTaskResultItemSchema,
    AdcTaskResultItemSchema,
    AfdVerificationTaskResultItemSchema,
    FdVerificationTaskResultItemSchema,
    ArTaskResultItemSchema,
    DdTaskResultItemSchema,
    MdTaskResultItemSchema,
    MfdVerificationTaskResultItemSchema,
    NarTaskResultItemSchema,
    PfdTaskResultItemSchema,
]

OneOfTaskResultSchema = Union[
    FdTaskResultSchema,
    AfdTaskResultSchema,
    AcTaskResultSchema,
    AdcTaskResultSchema,
    AfdVerificationTaskResultSchema,
    FdVerificationTaskResultSchema,
    ArTaskResultSchema,
    DdTaskResultSchema,
    MdTaskResultSchema,
    MfdVerificationTaskResultSchema,
    NarTaskResultSchema,
    PfdTaskResultSchema,
]


class PaginatedTaskResponseSchema[
    I: BaseSchema,
    R: BaseTaskResultSchema,
    P: PrimitiveName,
](PaginatedResponseSchema[I]):
    primitive_name: P
    result: R | TaskErrorSchema | None


OneOfPaginatedTaskResponseSchema = Annotated[
    Union[
        PaginatedTaskResponseSchema[
            FdTaskResultItemSchema,
            FdTaskResultSchema,
            Literal[PrimitiveName.FD],
        ],
        PaginatedTaskResponseSchema[
            AfdTaskResultItemSchema,
            AfdTaskResultSchema,
            Literal[PrimitiveName.AFD],
        ],
        PaginatedTaskResponseSchema[
            AcTaskResultItemSchema,
            AcTaskResultSchema,
            Literal[PrimitiveName.AC],
        ],
        PaginatedTaskResponseSchema[
            AdcTaskResultItemSchema,
            AdcTaskResultSchema,
            Literal[PrimitiveName.ADC],
        ],
        PaginatedTaskResponseSchema[
            AfdVerificationTaskResultItemSchema,
            AfdVerificationTaskResultSchema,
            Literal[PrimitiveName.AFD_VERIFICATION],
        ],
        PaginatedTaskResponseSchema[
            FdVerificationTaskResultItemSchema,
            FdVerificationTaskResultSchema,
            Literal[PrimitiveName.FD_VERIFICATION],
        ],
        PaginatedTaskResponseSchema[
            ArTaskResultItemSchema,
            ArTaskResultSchema,
            Literal[PrimitiveName.AR],
        ],
        PaginatedTaskResponseSchema[
            DdTaskResultItemSchema,
            DdTaskResultSchema,
            Literal[PrimitiveName.DD],
        ],
        PaginatedTaskResponseSchema[
            MdTaskResultItemSchema,
            MdTaskResultSchema,
            Literal[PrimitiveName.MD],
        ],
        PaginatedTaskResponseSchema[
            MfdVerificationTaskResultItemSchema,
            MfdVerificationTaskResultSchema,
            Literal[PrimitiveName.MFD_VERIFICATION],
        ],
        PaginatedTaskResponseSchema[
            NarTaskResultItemSchema,
            NarTaskResultSchema,
            Literal[PrimitiveName.NAR],
        ],
        PaginatedTaskResponseSchema[
            PfdTaskResultItemSchema,
            PfdTaskResultSchema,
            Literal[PrimitiveName.PFD],
        ],
    ],
    Field(discriminator="primitive_name"),
]


class BaseTaskSchema(BaseSchema):
    id: UUID
    params: OneOfTaskParams
    datasets: list[DatasetSchema]
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
    result: OneOfTaskResultSchema


TaskSchema = Annotated[
    Union[ProcessingTaskSchema, FailedTaskSchema, SuccessTaskSchema],
    Field(discriminator="status"),
]


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
        list(FdVerificationTaskResultOrderingField),
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
    Annotated[FdVerificationTaskResultFiltersSchema, Depends()],
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
    FdVerificationTaskResultOrderingField,
    ArTaskResultOrderingField,
    DdTaskResultOrderingField,
    MdTaskResultOrderingField,
    MfdVerificationTaskResultOrderingField,
    NarTaskResultOrderingField,
    PfdTaskResultOrderingField,
]
