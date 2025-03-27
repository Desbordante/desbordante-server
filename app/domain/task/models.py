from uuid import UUID

from sqlmodel import JSON, Column, Field, Relationship, SQLModel

from app.domain.task.schemas.schemas import OneOfTaskConfig, OneOfTaskResult, TaskStatus
from app.domain.user.models import User
from app.models.models import BaseUUIDModel


class TaskBase(SQLModel):
    status: TaskStatus = TaskStatus.CREATED
    config: OneOfTaskConfig = Field(sa_column=Column(JSON))
    result: OneOfTaskResult | None = Field(default=None, sa_column=Column(JSON))

    owner_id: int | None = Field(default=None, foreign_key="users.id")


class Task(BaseUUIDModel, TaskBase, table=True):
    owner: User | None = Relationship(back_populates="tasks")


class TaskPublic(TaskBase):
    id: UUID
