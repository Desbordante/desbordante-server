from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.annotations import uuid_pk
from src.models.base_models import BaseModel
from src.models.links import TaskDatasetLink
from src.models.task_result_models import TaskResultModel
from src.models.user_models import UserModel
from src.schemas.base_schemas import PydanticType, TaskErrorSchema, TaskStatus
from src.schemas.task_schemas.base_schemas import OneOfTaskParams, OneOfTaskResultSchema

if TYPE_CHECKING:
    from src.models.dataset_models import DatasetModel


class TaskModel(BaseModel):
    id: Mapped[uuid_pk]

    is_public: Mapped[bool] = mapped_column(default=False)

    owner_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=True
    )
    owner: Mapped["UserModel | None"] = relationship(back_populates="tasks")

    params: Mapped[OneOfTaskParams] = mapped_column(PydanticType(OneOfTaskParams))

    status: Mapped[TaskStatus] = mapped_column(default=TaskStatus.PENDING)

    result: Mapped[OneOfTaskResultSchema | TaskErrorSchema | None] = mapped_column(
        PydanticType(OneOfTaskResultSchema | TaskErrorSchema | None), default=None
    )

    results: Mapped[list["TaskResultModel"]] = relationship(back_populates="task")

    datasets: Mapped[list["DatasetModel"]] = relationship(
        secondary=TaskDatasetLink.__table__,
        back_populates="related_tasks",
        lazy="selectin",
    )
