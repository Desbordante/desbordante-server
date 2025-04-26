from uuid import UUID

from sqlmodel import Field

from _app.models.models import BaseModel


class DatasetTaskLink(BaseModel, table=True):
    dataset_id: UUID | None = Field(
        default=None, foreign_key="datasets.id", primary_key=True
    )
    task_id: UUID | None = Field(default=None, foreign_key="tasks.id", primary_key=True)


class GraphTaskLink(BaseModel, table=True):
    graph_id: UUID | None = Field(
        default=None, foreign_key="graphs.id", primary_key=True
    )
    task_id: UUID | None = Field(default=None, foreign_key="tasks.id", primary_key=True)
