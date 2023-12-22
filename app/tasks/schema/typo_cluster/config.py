from dataclasses import Field
from typing import Annotated

from pydantic import UUID4, BaseModel

from app.tasks.schema.base_task_config import BaseTaskConfig


class TypoFD(BaseModel):
    left: list[int]
    right: int


class TypoClusterTaskConfig(BaseTaskConfig):
    parent_task_id: UUID4
    typo_fd: TypoFD
    radius: Annotated[float, Field(ge=1, le=10)]
    ratio: Annotated[float, Field(ge=0, le=1)]
