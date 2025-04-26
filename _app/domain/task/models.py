from uuid import UUID

from sqlmodel import JSON, Column, Field, Relationship, SQLModel

from _app.domain.file.dataset.models import Dataset
from _app.domain.file.graph.models import Graph
from _app.domain.task.schemas.schemas import OneOfTaskConfig, OneOfTaskResult
from _app.domain.task.schemas.types import TaskStatus
from _app.domain.user.models import User
from _app.models.links import DatasetTaskLink, GraphTaskLink
from _app.models.models import BaseUUIDModel


class TaskBase(SQLModel):
    status: TaskStatus = TaskStatus.CREATED
    config: OneOfTaskConfig = Field(sa_column=Column(JSON))
    result: OneOfTaskResult | None = Field(default=None, sa_column=Column(JSON))

    initiator_id: int | None = Field(default=None, foreign_key="users.id")


class Task(BaseUUIDModel, TaskBase, table=True):
    initiator: User | None = Relationship(back_populates="tasks")

    datasets: list["Dataset"] = Relationship(
        back_populates="related_tasks", link_model=DatasetTaskLink
    )
    graphs: list["Graph"] = Relationship(
        back_populates="related_tasks", link_model=GraphTaskLink
    )


class TaskPublic(TaskBase):
    id: UUID
