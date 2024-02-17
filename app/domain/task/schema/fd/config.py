from typing import Annotated
from pydantic import Field
from app.domain.task.schema.base_config import BaseTaskConfig


class FDTaskConfig(BaseTaskConfig):
    error_threshold: Annotated[float, Field(ge=0, le=1)]
    max_lhs: Annotated[int, Field(ge=1, le=10)]
    threads_count: Annotated[int, Field(ge=1, le=8)]
