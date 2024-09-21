from uuid import UUID
from pydantic import BaseModel

from internal.domain.task.value_objects import OneOfTaskConfig


class ProfilingTaskBaseSchema(BaseModel):
    task_id: UUID
    dataset_id: UUID
    config: OneOfTaskConfig


class ProfilingTaskCreateSchema(ProfilingTaskBaseSchema): ...


ProfilingTaskResponseSchema = None
