from typing import Union
from uuid import UUID


from _app.domain.task.schemas.fd.task import FdTaskConfig, FdTaskResult
from _app.domain.task.schemas.pfd.task import PfdTaskConfig, PfdTaskResult
from _app.domain.task.schemas.afd.task import AfdTaskConfig, AfdTaskResult
from _app.domain.task.schemas.afd_verification.task import (
    AfdVerificationTaskConfig,
    AfdVerificationTaskResult,
)
from _app.domain.task.schemas.dd.task import DdTaskConfig, DdTaskResult
from _app.domain.task.schemas.md.task import MdTaskConfig, MdTaskResult
from _app.domain.task.schemas.nar.task import NarTaskConfig, NarTaskResult
from _app.domain.task.schemas.adc.task import AdcTaskConfig, AdcTaskResult
from _app.domain.task.schemas.ac.task import AcTaskConfig, AcTaskResult

from _app.schemas.schemas import BaseSchema

OneOfTaskConfig = Union[
    FdTaskConfig,
    PfdTaskConfig,
    AfdTaskConfig,
    AfdVerificationTaskConfig,
    NarTaskConfig,
    DdTaskConfig,
    MdTaskConfig,
    AdcTaskConfig,
    AcTaskConfig,
]

OneOfTaskResult = Union[
    FdTaskResult,
    PfdTaskResult,
    AfdTaskResult,
    AfdVerificationTaskResult,
    NarTaskResult,
    DdTaskResult,
    MdTaskResult,
    AdcTaskResult,
    AcTaskResult,
]


class TaskCreate(BaseSchema):
    files_ids: list[UUID]
    config: OneOfTaskConfig
