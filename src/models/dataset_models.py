from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    TIMESTAMP,
    Enum,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.annotations import str_non_nullable, uuid_pk
from src.models.base_models import BaseModel
from src.models.links import TaskDatasetLink
from src.models.task_models import TaskModel
from src.models.user_models import UserModel
from src.schemas.base_schemas import (
    CeleryTaskStatus,
    PydanticType,
    TaskErrorSchema,
    TaskStatus,
)
from src.schemas.dataset_schemas import (
    DatasetType,
    OneOfDatasetInfo,
    OneOfDatasetParams,
)

if TYPE_CHECKING:
    from src.models.task_models import TaskModel


class PreprocessingTaskModel(BaseModel):
    id: Mapped[uuid_pk]
    status: Mapped[CeleryTaskStatus] = mapped_column(default=CeleryTaskStatus.PENDING)
    result: Mapped[OneOfDatasetInfo | dict | None] = mapped_column(
        PydanticType(OneOfDatasetInfo | dict | None), default=None
    )
    finished_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True
    )

    dataset_id: Mapped[UUID] = mapped_column(
        ForeignKey("datasets.id", ondelete="CASCADE"), index=True, unique=True
    )
    dataset: Mapped["DatasetModel"] = relationship(back_populates="preprocessing")


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

    preprocessing: Mapped[PreprocessingTaskModel] = relationship(
        back_populates="dataset", lazy="selectin", uselist=False
    )

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    owner: Mapped["UserModel"] = relationship(back_populates="datasets")

    related_tasks: Mapped[list["TaskModel"]] = relationship(
        secondary=TaskDatasetLink.__table__, back_populates="datasets"
    )
