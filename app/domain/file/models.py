from typing import Optional
from uuid import UUID

from pydantic import PositiveInt
from sqlmodel import Field, Relationship, SQLModel

from app.domain.file.schemas import FileFormat
from app.domain.user.models import User
from app.models.models import BaseUUIDModel


class FileBase(SQLModel):
    file_format: FileFormat
    name: str
    byte_size: PositiveInt
    owner_id: Optional[int] = Field(default=None, foreign_key="users.id")


class File(BaseUUIDModel, FileBase, table=True):
    path: str

    owner: Optional[User] = Relationship(back_populates="files")


class FilePublic(FileBase):
    id: UUID
