from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db import Base


class FileInfo(Base):
    __tablename__ = "FileInfo"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=text("now()")
    )
    user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("User.id", ondelete="SET NULL", onupdate="CASCADE"), default=None
    )
    is_built_in: Mapped[bool] = mapped_column(default=False)
    is_valid: Mapped[bool] = mapped_column(default=True)
    mime_type: Mapped[str | None] = mapped_column(default=None)
    encoding: Mapped[str | None] = mapped_column(default=None)
    file_name: Mapped[str]
    original_file_name: Mapped[str]
    has_header: Mapped[bool]
    delimiter: Mapped[str]
    renamed_header: Mapped[str]
    rows_count: Mapped[int]
    count_of_columns: Mapped[int]
    path: Mapped[str] = mapped_column(unique=True)
    deleted_at: Mapped[datetime | None] = mapped_column(default=None)

    user = relationship("User")
    file_format = relationship("FileFormat")
    task = relationship("Task")
