from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.annotations import int_pk
from src.models.base_models import BaseModel

if TYPE_CHECKING:
    from src.models.dataset_models import DatasetModel


class UserModel(BaseModel):
    id: Mapped[int_pk]

    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False, nullable=False)

    datasets: Mapped[list["DatasetModel"]] = relationship(back_populates="owner")
