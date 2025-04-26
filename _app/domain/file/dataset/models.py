from typing import TYPE_CHECKING
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel

from _app.domain.file.dataset.schemas import DatasetSeparator
from _app.domain.file.models import File
from _app.models.models import BaseUUIDModel

if TYPE_CHECKING:
    pass


class DatasetBase(SQLModel):
    separator: DatasetSeparator
    has_header: bool
    columns_count: int
    rows_count: int


class Dataset(BaseUUIDModel, DatasetBase, table=True):
    # related_tasks: list["Task"] = Relationship(
    #     back_populates="datasets", link_model=DatasetTaskLink
    # )

    file_id: UUID | None = Field(default=None, foreign_key="files.id")

    file: File = Relationship()


class DatasetPublic(DatasetBase):
    id: UUID
