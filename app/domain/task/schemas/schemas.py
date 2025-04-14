from typing import Union
from uuid import UUID


from app.domain.task.schemas.fd.task import FdTaskConfig, FdTaskResult
from app.domain.task.schemas.dd.task import DdTaskConfig, DdTaskResult
from app.domain.task.schemas.md.task import MdTaskConfig, MdTaskResult
from app.domain.task.schemas.nar.task import NarTaskConfig, NarTaskResult
from app.domain.task.schemas.adc.task import AdcTaskConfig, AdcTaskResult
from app.schemas.schemas import BaseSchema

OneOfTaskConfig = Union[FdTaskConfig, NarTaskConfig, DdTaskConfig, MdTaskConfig, AdcTaskConfig]

OneOfTaskResult = Union[FdTaskResult, NarTaskResult, DdTaskResult, MdTaskResult, AdcTaskResult]


class TaskCreate(BaseSchema):
    files_ids: list[UUID]
    config: OneOfTaskConfig
