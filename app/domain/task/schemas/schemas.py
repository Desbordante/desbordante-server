from typing import Union
from uuid import UUID


from app.domain.task.schemas.fd.task import FdTaskConfig, FdTaskResult
from app.domain.task.schemas.dd.task import DdTaskConfig, DdTaskResult
from app.domain.task.schemas.md.task import MdTaskConfig, MdTaskResult
from app.domain.task.schemas.nar.task import NarTaskConfig, NarTaskResult
from app.schemas.schemas import BaseSchema

OneOfTaskConfig = Union[FdTaskConfig, NarTaskConfig, DdTaskConfig, MdTaskConfig]

OneOfTaskResult = Union[FdTaskResult, NarTaskResult, DdTaskResult, MdTaskResult]


class TaskCreate(BaseSchema):
    files_ids: list[UUID]
    config: OneOfTaskConfig
