from typing import TYPE_CHECKING

from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.annotations import uuid_pk
from src.models.base_models import BaseModel
from src.models.links import TaskDatasetLink
from src.models.user_models import UserModel
from src.schemas.base_schemas import TaskStatus
from src.schemas.task_schemas.base_schemas import OneOfTaskParams

if TYPE_CHECKING:
    from src.models.dataset_models import DatasetModel


class TaskModel(BaseModel):
    id: Mapped[uuid_pk]

    params: Mapped[OneOfTaskParams] = mapped_column(JSON)

    status: Mapped[TaskStatus] = mapped_column(default=TaskStatus.Pending)
    result: Mapped[None] = mapped_column(JSON, default=None)

    initiator_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    initiator: Mapped["UserModel"] = relationship(back_populates="tasks")

    datasets: Mapped[list["DatasetModel"]] = relationship(
        secondary=TaskDatasetLink.__table__,
        back_populates="related_tasks",
        lazy="selectin",
    )
