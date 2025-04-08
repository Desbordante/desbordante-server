from typing import Union
from uuid import UUID


from _app.domain.task.schemas.fd.task import FdTaskConfig, FdTaskResult
from _app.domain.task.schemas.dd.task import DdTaskConfig, DdTaskResult
from _app.domain.task.schemas.nar.task import NarTaskConfig, NarTaskResult
from _app.schemas.schemas import BaseSchema

OneOfTaskConfig = Union[FdTaskConfig, NarTaskConfig, DdTaskConfig]

OneOfTaskResult = Union[FdTaskResult, NarTaskResult, DdTaskResult]


class TaskCreate(BaseSchema):
    files_ids: list[UUID]
    config: OneOfTaskConfig
