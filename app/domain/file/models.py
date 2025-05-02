from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import PositiveInt
from sqlmodel import Field, Relationship, SQLModel

from app.domain.file.schemas import FileFormat
from app.domain.user.models import User
from app.models.links import FileTaskLink
from app.models.models import BaseUUIDModel

if TYPE_CHECKING:
    from app.domain.task.models import Task


class FileBase(SQLModel):
    file_format: FileFormat
    name: str
    byte_size: PositiveInt
    owner_id: int | None = Field(default=None, foreign_key="users.id")


class File(BaseUUIDModel, FileBase, table=True):
    path: str

    owner: User | None = Relationship(back_populates="files")
    related_tasks: list["Task"] = Relationship(
        back_populates="files", link_model=FileTaskLink
    )


class FilePublic(FileBase):
    id: UUID

class FileFull(FilePublic):
    num_columns: int
    num_rows: int
    with_header: bool
    header: list[str] | None
