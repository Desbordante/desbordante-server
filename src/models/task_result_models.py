from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.annotations import uuid_pk
from src.models.base_models import BaseModel
from src.schemas.base_schemas import PydanticType
from src.schemas.task_schemas.base_schemas import OneOfTaskResult

if TYPE_CHECKING:
    from src.models.task_models import TaskModel


class TaskResultModel(BaseModel):
    id: Mapped[uuid_pk]

    result: Mapped[OneOfTaskResult] = mapped_column(PydanticType(OneOfTaskResult))

    task_id: Mapped[UUID] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"))
    task: Mapped["TaskModel"] = relationship(back_populates="results", lazy="joined")
