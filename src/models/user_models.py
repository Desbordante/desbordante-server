from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.annotations import int_pk, str_non_nullable, str_uniq
from src.models.base_models import BaseModel

if TYPE_CHECKING:
    from src.models.dataset_models import DatasetModel


class UserModel(BaseModel):
    id: Mapped[int_pk]
    email: Mapped[str_uniq]
    full_name: Mapped[str_non_nullable]

    hashed_password: Mapped[str_non_nullable]

    country: Mapped[str_non_nullable]
    company: Mapped[str_non_nullable]
    occupation: Mapped[str_non_nullable]

    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)

    datasets: Mapped[list["DatasetModel"]] = relationship(
        back_populates="owner", lazy="selectin"
    )
