from typing import TYPE_CHECKING

from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.annotations import str_non_nullable, uuid_pk
from src.models.base_models import BaseModel
from src.schemas.dataset_schemas import (
    DatasetStatus,
    DatasetType,
    OneOfDatasetInfo,
    OneOfDatasetParams,
)

if TYPE_CHECKING:
    from src.models.user_models import UserModel


class DatasetModel(BaseModel):
    id: Mapped[uuid_pk]
    type: Mapped[DatasetType]
    name: Mapped[str_non_nullable]
    size: Mapped[int]
    path: Mapped[str_non_nullable]
    params: Mapped[OneOfDatasetParams] = mapped_column(JSON)

    status: Mapped[DatasetStatus] = mapped_column(default=DatasetStatus.Queued)
    info: Mapped[OneOfDatasetInfo] = mapped_column(JSON, default=None)

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    owner: Mapped["UserModel"] = relationship(back_populates="datasets", lazy="joined")
