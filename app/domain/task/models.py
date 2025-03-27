from uuid import UUID

from sqlmodel import JSON, Column, Field, Relationship, SQLModel

from app.domain.file.models import File
from app.domain.task.schemas.schemas import OneOfTaskConfig, OneOfTaskResult
from app.domain.task.schemas.types import TaskStatus
from app.domain.user.models import User
from app.models.links import FileTaskLink
from app.models.models import BaseUUIDModel


class TaskBase(SQLModel):
    status: TaskStatus = TaskStatus.CREATED
    config: OneOfTaskConfig = Field(sa_column=Column(JSON))
    result: OneOfTaskResult | None = Field(default=None, sa_column=Column(JSON))

    initiator_id: int | None = Field(default=None, foreign_key="users.id")


class Task(BaseUUIDModel, TaskBase, table=True):
    initiator: User | None = Relationship(back_populates="tasks")
    files: list[File] = Relationship(
        back_populates="related_tasks", link_model=FileTaskLink
    )


class TaskPublic(TaskBase):
    id: UUID
