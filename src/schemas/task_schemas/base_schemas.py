from datetime import datetime
from typing import Annotated, Union
from uuid import UUID

from pydantic import Field

from src.schemas.base_schemas import BaseSchema, TaskStatus
from src.schemas.dataset_schemas import DatasetSchema
from src.schemas.task_schemas.afd.task_params import AFdTaskParams
from src.schemas.task_schemas.fd.task_params import FdTaskParams

OneOfTaskParams = Annotated[
    Union[FdTaskParams, AFdTaskParams],
    Field(discriminator="primitive_name"),
]


class TaskSchema(BaseSchema):
    id: UUID

    params: OneOfTaskParams

    status: TaskStatus

    datasets: list[DatasetSchema]

    created_at: datetime
    updated_at: datetime
