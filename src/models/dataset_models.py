from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.annotations import str_non_nullable, uuid_pk
from src.models.base_models import BaseModel
from src.models.links import TaskDatasetLink
from src.models.user_models import UserModel
from src.schemas.dataset_schemas import (
    DatasetType,
    OneOfDatasetInfo,
    OneOfDatasetParams,
    TaskStatus,
)

if TYPE_CHECKING:
    from src.models.task_models import TaskModel


class DatasetModel(BaseModel):
    id: Mapped[uuid_pk]
    type: Mapped[DatasetType]
    name: Mapped[str_non_nullable]
    size: Mapped[int]
    path: Mapped[str_non_nullable]
    params: Mapped[OneOfDatasetParams] = mapped_column(JSONB)

    status: Mapped[TaskStatus] = mapped_column(default=TaskStatus.Pending)
    info: Mapped[OneOfDatasetInfo | None] = mapped_column(JSONB, default=None)

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    owner: Mapped["UserModel"] = relationship(back_populates="datasets")

    related_tasks: Mapped[list["TaskModel"]] = relationship(
        secondary=TaskDatasetLink.__table__, back_populates="datasets"
    )
