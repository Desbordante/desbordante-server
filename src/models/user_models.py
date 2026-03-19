from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.annotations import int_pk
from src.models.auth_models import AuthAccountModel
from src.models.base_models import BaseModel

if TYPE_CHECKING:
    from src.models.dataset_models import DatasetModel
    from src.models.task_models import TaskModel


class UserModel(BaseModel):
    id: Mapped[int_pk]
    email: Mapped[str] = mapped_column(
        String(length=255), unique=True, index=True, nullable=False
    )

    is_banned: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False, nullable=False)

    datasets: Mapped[list["DatasetModel"]] = relationship(back_populates="owner")
    tasks: Mapped[list["TaskModel"]] = relationship(back_populates="owner")

    auth_accounts: Mapped[list[AuthAccountModel]] = relationship(back_populates="owner")
