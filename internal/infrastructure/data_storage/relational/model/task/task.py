import typing
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.dialects.postgresql import JSONB

from internal.domain.task.value_objects import (
    TaskStatus,
    OneOfTaskConfig,
    OneOfTaskResult,
    TaskFailureReason,
)
from internal.infrastructure.data_storage.relational.model import ORMBaseModel

if typing.TYPE_CHECKING:
    from internal.infrastructure.data_storage.relational.model.file import DatasetORM


class TaskORM(ORMBaseModel):
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
