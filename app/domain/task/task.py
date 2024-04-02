from enum import StrEnum, auto
import typing
from uuid import UUID, uuid4
from sqlalchemy.orm import Mapped, mapped_column
from app.db import ORMBase
from app.db.session import ORMBaseModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from app.domain.file.dataset import DatasetModel
from app.domain.task import OneOfTaskConfig, OneOfTaskResult

from sqlalchemy.dialects.postgresql import JSONB

if typing.TYPE_CHECKING:
    from app.domain.file.dataset import DatasetORM


class TaskStatus(StrEnum):
    FAILED = auto()
    CREATED = auto()
    RUNNING = auto()
    COMPLETED = auto()


class TaskFailureReason(StrEnum):
    MEMORY_LIMIT_EXCEEDED = auto()
    TIME_LIMIT_EXCEEDED = auto()
    WORKER_KILLED_BY_SIGNAL = auto()
    OTHER = auto()


class TaskORM(ORMBase):
    __tablename__ = "task"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    status: Mapped[TaskStatus]
    config: Mapped[OneOfTaskConfig] = mapped_column(JSONB)
    result: Mapped[OneOfTaskResult | None] = mapped_column(JSONB, default=None)

    dataset_id: Mapped[UUID] = mapped_column(ForeignKey("dataset.id"), nullable=False)
    dataset: Mapped["DatasetORM"] = relationship(
        "DatasetORM", back_populates="related_tasks"
    )

    # Only if task failed
    raised_exception_name: Mapped[str | None] = mapped_column(default=None)
    failure_reason: Mapped[TaskFailureReason | None] = mapped_column(default=None)
    traceback: Mapped[str | None] = mapped_column(default=None)


class TaskModel(ORMBaseModel):
    id: UUID
    status: TaskStatus
    config: OneOfTaskConfig
    result: OneOfTaskResult | None
    dataset: DatasetModel

    raised_exception_name: str | None
    failure_reason: TaskFailureReason | None
    traceback: str | None
