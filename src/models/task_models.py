from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.annotations import uuid_pk
from src.models.base_models import BaseModel
from src.models.user_models import UserModel
from src.schemas.base_schemas import PydanticType
from src.domain.task.value_objects import (
    OneOfTaskConfig,
    OneOfTaskResult,
    TaskStatus,
    TaskFailureReason,
)

if TYPE_CHECKING:
    from src.models.dataset_models import DatasetModel


class TaskModel(BaseModel):
    id: Mapped[uuid_pk]

    config: Mapped[OneOfTaskConfig] = mapped_column(PydanticType(OneOfTaskConfig))

    status: Mapped[TaskStatus] = mapped_column(default=TaskStatus.PENDING)
    result: Mapped[OneOfTaskResult | None] = mapped_column(JSONB, default=None)

    is_public: Mapped[bool] = mapped_column(default=False)

    dataset_id: Mapped[UUID] = mapped_column(
        ForeignKey("datasets.id", ondelete="CASCADE")
    )
    dataset: Mapped["DatasetModel"] = relationship(
        back_populates="related_tasks", lazy="joined"
    )

    owner_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=True
    )
    owner: Mapped["UserModel | None"] = relationship(back_populates="tasks")

    # Only if task failed
    raised_exception_name: Mapped[str | None] = mapped_column(default=None)
    failure_reason: Mapped[TaskFailureReason | None] = mapped_column(default=None)
    traceback: Mapped[str | None] = mapped_column(default=None)
