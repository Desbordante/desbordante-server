from datetime import datetime
from enum import auto
from enum import StrEnum
from uuid import UUID, uuid4
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base
from typing import Any


class TaskStatus(StrEnum):
    IN_PROCESS = auto()
    COMPLETED = auto()
    INTERNAL_SERVER_ERROR = auto()
    RESOURCE_LIMIT_IS_REACHED = auto()
    ADDED_TO_THE_TASK_QUEUE = auto()
    ADDING_TO_DB = auto()


class Task(Base):
    __tablename__ = "Task"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("User.id", ondelete="SET NULL", onupdate="CASCADE")
    )
    file_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("FileInfo.id", ondelete="SET NULL", onupdate="CASCADE")
    )
    is_private: Mapped[bool] = mapped_column(default=False)
    attempt_number: Mapped[int] = mapped_column(default=0)
    status: Mapped[TaskStatus]
    phase_name: Mapped[str | None] = mapped_column(default=None)
    current_phase: Mapped[int | None] = mapped_column(default=None)
    progres: Mapped[float] = mapped_column(default=0)
    max_phase: Mapped[int | None] = mapped_column(default=None)
    error_msg: Mapped[int | None] = mapped_column(default=None)
    id_executed: Mapped[bool] = mapped_column(default=False)
    elapsed_time: Mapped[float | None] = mapped_column(default=None)
    config: Mapped[dict[Any, Any]] = mapped_column(JSONB)
    result: Mapped[dict[Any, Any]] = mapped_column(JSONB)
    created_at: Mapped[datetime]
    deleted_at: Mapped[datetime | None] = mapped_column(default=None)

    user = relationship("User")
    file_info = relationship("FileInfo")
