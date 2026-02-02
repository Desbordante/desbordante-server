from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.annotations import uuid_pk
from src.models.base_models import BaseModel
from src.models.user_models import UserModel
from src.schemas.base_schemas import PydanticType, TaskErrorSchema
from src.schemas.dataset_schemas import TaskStatus
from src.schemas.task_schemas.base_schemas import OneOfTaskConfig, OneOfTaskResult

if TYPE_CHECKING:
    from src.models.dataset_models import DatasetModel


class TaskModel(BaseModel):
    id: Mapped[uuid_pk]

    config: Mapped[OneOfTaskConfig] = mapped_column(PydanticType(OneOfTaskConfig))

    status: Mapped[TaskStatus] = mapped_column(default=TaskStatus.PENDING)
    result: Mapped[OneOfTaskResult | TaskErrorSchema | None] = mapped_column(
        JSONB, default=None
    )

    dataset_id: Mapped[UUID] = mapped_column(
        ForeignKey("datasets.id", ondelete="CASCADE")
    )
    dataset: Mapped["DatasetModel"] = relationship(
        back_populates="related_tasks", lazy="joined"
    )

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    owner: Mapped["UserModel"] = relationship(back_populates="tasks")
