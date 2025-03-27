from uuid import UUID

from sqlmodel import JSON, Column, Field, SQLModel

from app.domain.task.schemas.schemas import OneOfTaskConfig, OneOfTaskResult, TaskStatus
from app.models.models import BaseUUIDModel


class TaskBase(SQLModel):
    status: TaskStatus = TaskStatus.CREATED
    config: OneOfTaskConfig = Field(sa_column=Column(JSON))
    result: OneOfTaskResult | None = Field(default=None, sa_column=Column(JSON))


class Task(BaseUUIDModel, TaskBase, table=True):
    pass


class TaskPublic(TaskBase):
    id: UUID
