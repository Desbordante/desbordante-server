from typing import Annotated
from pydantic import Field
from app.tasks.schema.base_task_config import BaseTaskConfig


class CFDTaskConfig(BaseTaskConfig):
    max_lhs: Annotated[int, Field(ge=1, le=10)]
    min_support_cfd: Annotated[int, Field(ge=1, le=16)]
    min_confidence: Annotated[float, Field(ge=0, le=1)]
