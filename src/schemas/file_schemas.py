from enum import StrEnum, auto
from typing import BinaryIO, Protocol
from uuid import UUID

from src.schemas.base_schemas import BaseSchema


class File(Protocol):
    name: str
    data: BinaryIO
    size: int
    content_type: str


class FileStatus(StrEnum):
    Temporary = auto()
    Permanent = auto()


class FileSchema(BaseSchema):
    id: UUID
    name: str
    size: int
