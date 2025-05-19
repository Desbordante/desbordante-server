from typing import Union
from uuid import UUID


from app.domain.task.schemas.fd.task import FdTaskConfig, FdTaskResult
from app.domain.task.schemas.pfd.task import PfdTaskConfig, PfdTaskResult
from app.domain.task.schemas.afd.task import AfdTaskConfig, AfdTaskResult
from app.domain.task.schemas.afd_verification.task import (
    AfdVerificationTaskConfig,
    AfdVerificationTaskResult,
)
from app.domain.task.schemas.ar.task import (
    ARTaskConfig,
    ARTaskResult,
)
from app.domain.task.schemas.dd.task import DdTaskConfig, DdTaskResult
from app.domain.task.schemas.md.task import MdTaskConfig, MdTaskResult
from app.domain.task.schemas.mfd_verification.task import (
    MfdVerificationTaskConfig,
    MfdVerificationTaskResult,
)
from app.domain.task.schemas.nar.task import NarTaskConfig, NarTaskResult
from app.domain.task.schemas.adc.task import AdcTaskConfig, AdcTaskResult
from app.domain.task.schemas.ac.task import AcTaskConfig, AcTaskResult
from app.schemas.schemas import BaseSchema

from app.domain.task.schemas.dd.filter import DdFilterOptions
from app.domain.task.schemas.mfd_verification.filter import MfdVerificationFilterOptions
from app.domain.task.schemas.md.filter import MdFilterOptions
from app.domain.task.schemas.fd.filter import FdFilterOptions
from app.domain.task.schemas.afd.filter import AfdFilterOptions
from app.domain.task.schemas.afd_verification.filter import AfdVerificationFilterOptions
from app.domain.task.schemas.pfd.filter import PfdFilterOptions
from app.domain.task.schemas.nar.filter import NarFilterOptions
from app.domain.task.schemas.ac.filter import AcFilterOptions
from app.domain.task.schemas.adc.filter import AdcFilterOptions

from app.domain.task.schemas.dd.sort import DdSortOptions
from app.domain.task.schemas.mfd_verification.sort import MfdVerificationSortOptions
from app.domain.task.schemas.md.sort import MdSortOptions
from app.domain.task.schemas.fd.sort import FdSortOptions
from app.domain.task.schemas.afd.sort import AfdSortOptions
from app.domain.task.schemas.afd_verification.sort import AfdVerificationSortOptions
from app.domain.task.schemas.pfd.sort import PfdSortOptions
from app.domain.task.schemas.nar.sort import NarSortOptions
from app.domain.task.schemas.ac.sort import AcSortOptions
from app.domain.task.schemas.adc.sort import AdcSortOptions
from app.domain.task.schemas.ar.sort import ARSortOptions

OneOfTaskConfig = Union[
    FdTaskConfig,
    PfdTaskConfig,
    AfdTaskConfig,
    AfdVerificationTaskConfig,
    ARTaskConfig,
    NarTaskConfig,
    DdTaskConfig,
    MdTaskConfig,
    MfdVerificationTaskConfig,
    AdcTaskConfig,
    AcTaskConfig,
]

OneOfTaskResult = Union[
    FdTaskResult,
    PfdTaskResult,
    AfdTaskResult,
    AfdVerificationTaskResult,
    ARTaskResult,
    NarTaskResult,
    DdTaskResult,
    MdTaskResult,
    MfdVerificationTaskResult,
    AdcTaskResult,
    AcTaskResult,
]

OneOfFilterOption = Union[
    NarFilterOptions,
    DdFilterOptions,
    MdFilterOptions,
    MfdVerificationFilterOptions,
    FdFilterOptions,
    PfdFilterOptions,
    AfdFilterOptions,
    AdcFilterOptions,
    AcFilterOptions,
    AfdVerificationFilterOptions,
]

OneOfSortOption = Union[
    FdSortOptions,
    PfdSortOptions,
    AfdSortOptions,
    DdSortOptions,
    NarSortOptions,
    MdSortOptions,
    MfdVerificationSortOptions,
    AcSortOptions,
    AdcSortOptions,
    AfdVerificationSortOptions,
    ARSortOptions,
]


class TaskCreate(BaseSchema):
    files_ids: list[UUID]
    config: OneOfTaskConfig
