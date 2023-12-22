from typing import Annotated
from pydantic import Field
from app.tasks.schema.base_task_config import BaseTaskConfig


class StatsTaskConfig(BaseTaskConfig):
    threads_count: Annotated[int, Field(ge=1, le=8)]
