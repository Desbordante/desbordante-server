from enum import StrEnum, auto
from uuid import UUID, uuid4
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base


class InputFormat(StrEnum):
    SINGULAR = auto()
    TABULAR = auto()


class FileFormat(Base):
    __tablename__ = "FileFormat"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    file_id: Mapped[UUID] = mapped_column(
        ForeignKey("FileInfo.id", onupdate="CASCADE", ondelete="CASCADE")
    )
    input_format: Mapped[InputFormat]
    singular_tid_column_index: Mapped[int | None] = mapped_column(default=None)
    singular_item_column_index: Mapped[int | None] = mapped_column(default=None)
    tabular_has_tid: Mapped[bool | None] = mapped_column(default=None)
