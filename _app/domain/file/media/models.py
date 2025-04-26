from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel

from _app.domain.file.models import File
from _app.models.models import BaseUUIDModel


class MediaBase(SQLModel):
    width: int
    height: int


class Media(BaseUUIDModel, MediaBase, table=True):
    file_id: UUID | None = Field(default=None, foreign_key="files.id")

    file: File = Relationship()


class MediaPublic(MediaBase):
    id: UUID
