from datetime import datetime
from typing import TYPE_CHECKING

from celery import states
from sqlalchemy import BigInteger, DateTime, Enum, ForeignKey, Sequence, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.annotations import str_non_nullable, uuid_pk
from src.models.base_models import BaseModel
from src.models.links import TaskDatasetLink
from src.models.task_models import TaskModel
from src.models.user_models import UserModel
from src.schemas.base_schemas import PydanticType, TaskErrorSchema, TaskStatus
from src.schemas.dataset_schemas import (
    DatasetType,
    OneOfDatasetInfo,
    OneOfDatasetParams,
)

if TYPE_CHECKING:
    from src.models.task_models import TaskModel


class DatasetTask(BaseModel):
    """Celery task result for preprocess_dataset. Result stored as JSONB OneOfDatasetInfo."""

    id: Mapped[int] = mapped_column(
        BigInteger,
        Sequence("task_id_sequence"),
        primary_key=True,
        autoincrement=True,
    )
    task_id: Mapped[str] = mapped_column(String(155), unique=True)
    status: Mapped[str] = mapped_column(String(50), default=states.PENDING)
    result: Mapped[dict | None] = mapped_column(
        JSONB(astext_type=Text()), nullable=True
    )
    date_done: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    traceback: Mapped[str | None] = mapped_column(Text(), nullable=True)

    def __init__(self, task_id: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.task_id = task_id

    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "status": self.status,
            "result": self.result,
            "traceback": self.traceback,
            "date_done": self.date_done,
        }

    @classmethod
    def configure(cls, schema: str | None = None, name: str | None = None) -> None:
        pass


class DatasetModel(BaseModel):
    id: Mapped[uuid_pk]
    type: Mapped[DatasetType]
    name: Mapped[str_non_nullable]
    size: Mapped[int]
    path: Mapped[str_non_nullable]
    params: Mapped[OneOfDatasetParams] = mapped_column(PydanticType(OneOfDatasetParams))
    is_public: Mapped[bool] = mapped_column(default=False, index=True)

    status: Mapped[TaskStatus] = mapped_column(
        Enum(
            TaskStatus,
            native_enum=False,
            values_callable=lambda x: [e.value for e in x],
        ),
        nullable=False,
        default=TaskStatus.PENDING,
    )

    info: Mapped[OneOfDatasetInfo | TaskErrorSchema | None] = mapped_column(
        PydanticType(OneOfDatasetInfo | TaskErrorSchema | None), default=None
    )

    preprocess_task_id: Mapped[str | None] = mapped_column(
        String(155), nullable=True, index=True
    )
    preprocess_task: Mapped[DatasetTask | None] = relationship(
        "DatasetTask",
        primaryjoin="DatasetModel.preprocess_task_id == DatasetTask.task_id",
        lazy="selectin",
        viewonly=True,
    )

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    owner: Mapped["UserModel"] = relationship(back_populates="datasets")

    related_tasks: Mapped[list["TaskModel"]] = relationship(
        secondary=TaskDatasetLink.__table__, back_populates="datasets"
    )
