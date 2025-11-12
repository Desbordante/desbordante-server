from typing import TYPE_CHECKING

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.annotations import int_pk, str_non_nullable
from src.models.base_models import BaseModel
from src.schemas.auth_schemas import OAuthProvider

if TYPE_CHECKING:
    from src.models.dataset_models import DatasetModel


class UserModel(BaseModel):
    id: Mapped[int_pk]

    is_banned: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False, nullable=False)

    oauth_provider: Mapped[OAuthProvider] = mapped_column(nullable=False)
    oauth_id: Mapped[str_non_nullable]

    datasets: Mapped[list["DatasetModel"]] = relationship(back_populates="owner")

    __table_args__ = (
        UniqueConstraint("oauth_provider", "oauth_id", name="uq_user_oauth"),
    )
