from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.annotations import uuid_pk
from src.models.base_models import BaseModel
from src.models.links import TaskDatasetLink
from src.models.user_models import UserModel
from src.schemas.base_schemas import PydanticType, TaskErrorSchema, TaskStatus
from src.schemas.task_schemas.base_schemas import OneOfTaskParams, OneOfTaskResultSchema

if TYPE_CHECKING:
    from src.models.dataset_models import DatasetModel
    from src.models.task_result_models import TaskResultModel


class TaskModel(BaseModel):
    id: Mapped[uuid_pk]

    params: Mapped[OneOfTaskParams] = mapped_column(PydanticType(OneOfTaskParams))

    status: Mapped[TaskStatus] = mapped_column(default=TaskStatus.Pending)
    result: Mapped[OneOfTaskResultSchema | TaskErrorSchema | None] = mapped_column(
        PydanticType(OneOfTaskResultSchema | TaskErrorSchema | None), default=None
    )

    results: Mapped[list["TaskResultModel"]] = relationship(back_populates="task")

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    owner: Mapped["UserModel"] = relationship(back_populates="tasks")

    datasets: Mapped[list["DatasetModel"]] = relationship(
        secondary=TaskDatasetLink.__table__,
        back_populates="related_tasks",
        lazy="selectin",
    )
