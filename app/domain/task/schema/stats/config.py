from typing import Annotated
from pydantic import Field
from app.domain.task.schema.base_config import BaseTaskConfig


class StatsTaskConfig(BaseTaskConfig):
    threads_count: Annotated[int, Field(ge=1, le=8)]
