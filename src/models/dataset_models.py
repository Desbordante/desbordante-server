from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.annotations import str_non_nullable, uuid_pk
from src.models.base_models import BaseModel, BaseTaskModel
from src.models.task_models import ProfilingTaskDatasetLink, ProfilingTaskModel
from src.models.user_models import UserModel
from src.schemas.base_schemas import PydanticType
from src.schemas.dataset_schemas import (
    DatasetType,
    OneOfDatasetInfo,
    OneOfDatasetParams,
)


class PreprocessingTaskModel(BaseTaskModel[OneOfDatasetInfo]):
    __tablename__ = "preprocessing_tasks"

    dataset_id: Mapped[UUID] = mapped_column(
        ForeignKey("datasets.id", ondelete="CASCADE"), index=True, unique=True
    )
    dataset: Mapped["DatasetModel"] = relationship(back_populates="preprocessing")


class DatasetModel(BaseModel):
    __tablename__ = "datasets"

    id: Mapped[uuid_pk]
    type: Mapped[DatasetType]
    name: Mapped[str_non_nullable]
    size: Mapped[int]
    path: Mapped[str_non_nullable]
    params: Mapped[OneOfDatasetParams] = mapped_column(PydanticType(OneOfDatasetParams))
    is_public: Mapped[bool] = mapped_column(default=False, index=True)

    preprocessing: Mapped[PreprocessingTaskModel] = relationship(
        back_populates="dataset", lazy="selectin", uselist=False
    )

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    owner: Mapped["UserModel"] = relationship(back_populates="datasets")

    related_tasks: Mapped[list["ProfilingTaskModel"]] = relationship(
        secondary=ProfilingTaskDatasetLink.__table__, back_populates="datasets"
    )
