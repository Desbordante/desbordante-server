from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.annotations import uuid_pk
from src.models.base_models import BaseModel
from src.models.links import TaskDatasetLink
from src.models.user_models import UserModel
from src.schemas.base_schemas import TaskStatus
from src.schemas.task_schemas.base_schemas import OneOfTaskParams, OneOfTaskResult

if TYPE_CHECKING:
    from src.models.dataset_models import DatasetModel


class TaskModel(BaseModel):
    id: Mapped[uuid_pk]

    params: Mapped[OneOfTaskParams] = mapped_column(JSONB)

    status: Mapped[TaskStatus] = mapped_column(default=TaskStatus.Pending)
    result: Mapped["TaskResultModel"] = relationship(
        back_populates="task", uselist=False
    )

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    owner: Mapped["UserModel"] = relationship(back_populates="tasks")

    datasets: Mapped[list["DatasetModel"]] = relationship(
        secondary=TaskDatasetLink.__table__,
        back_populates="related_tasks",
        lazy="selectin",
    )


class TaskResultModel(BaseModel):
    id: Mapped[uuid_pk]

    result: Mapped[OneOfTaskResult] = mapped_column(JSONB)

    task_id: Mapped[UUID] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"), unique=True
    )
    task: Mapped["TaskModel"] = relationship(back_populates="result", lazy="joined")
