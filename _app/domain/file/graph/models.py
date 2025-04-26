from typing import TYPE_CHECKING
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel

from _app.domain.file.models import File
from _app.models.links import GraphTaskLink
from _app.models.models import BaseUUIDModel

if TYPE_CHECKING:
    from _app.domain.task.models import Task


class GraphBase(SQLModel):
    pass


class Graph(BaseUUIDModel, GraphBase, table=True):
    related_tasks: list["Task"] = Relationship(
        back_populates="graphs", link_model=GraphTaskLink
    )

    file_id: UUID | None = Field(default=None, foreign_key="files.id")

    file: File = Relationship()


class GraphPublic(GraphBase):
    id: UUID
