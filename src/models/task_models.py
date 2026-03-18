from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.annotations import uuid_pk
from src.models.base_models import BaseModel, BaseTaskModel
from src.models.user_models import UserModel
from src.schemas.base_schemas import PydanticType
from src.schemas.task_schemas.base_schemas import (
    OneOfTaskParams,
    OneOfTaskResultItemSchema,
    OneOfTaskResultSchema,
)

if TYPE_CHECKING:
    from src.models.dataset_models import DatasetModel


class ProfilingDepModel(BaseModel):
    __tablename__ = "profiling_deps"

    id: Mapped[uuid_pk]

    result: Mapped[OneOfTaskResultItemSchema] = mapped_column(
        PydanticType(OneOfTaskResultItemSchema)
    )

    task_id: Mapped[UUID] = mapped_column(
        ForeignKey("profiling_tasks.id", ondelete="CASCADE")
    )
    task: Mapped["ProfilingTaskModel"] = relationship(back_populates="profiling_deps")


class ProfilingTaskDatasetLink(BaseModel):
    __tablename__ = "profiling_task_dataset_links"

    task_id: Mapped[uuid_pk] = mapped_column(
        ForeignKey("profiling_tasks.id", ondelete="CASCADE"), primary_key=True
    )
    dataset_id: Mapped[uuid_pk] = mapped_column(
        ForeignKey("datasets.id", ondelete="CASCADE"), primary_key=True
    )


class ProfilingTaskModel(BaseTaskModel[OneOfTaskResultSchema]):
    __tablename__ = "profiling_tasks"

    is_public: Mapped[bool] = mapped_column(default=False)

    owner_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=True
    )
    owner: Mapped["UserModel | None"] = relationship(back_populates="tasks")

    params: Mapped[OneOfTaskParams] = mapped_column(PydanticType(OneOfTaskParams))

    profiling_deps: Mapped[list["ProfilingDepModel"]] = relationship(
        back_populates="task"
    )

    datasets: Mapped[list["DatasetModel"]] = relationship(
        secondary=ProfilingTaskDatasetLink.__table__,
        back_populates="related_tasks",
        lazy="selectin",
    )
