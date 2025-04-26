from typing import Union
from uuid import UUID


from _app.domain.task.schemas.fd.task import FdTaskConfig, FdTaskResult
from _app.schemas.schemas import BaseSchema

OneOfTaskConfig = Union[FdTaskConfig]

OneOfTaskResult = Union[FdTaskResult]


class TaskCreate(BaseSchema):
    files_ids: list[UUID]
    config: OneOfTaskConfig
