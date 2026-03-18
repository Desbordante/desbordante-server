from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_models import BaseModel
from src.schemas.auth_schemas import AuthProvider

if TYPE_CHECKING:
    from src.models.user_models import UserModel


class AuthAccountModel(BaseModel):
    __tablename__ = "auth_accounts"

    provider: Mapped[AuthProvider] = mapped_column(
        Enum(
            AuthProvider,
            native_enum=False,
            values_callable=lambda x: [e.value for e in x],
        ),
        nullable=False,
        primary_key=True,
    )
    account_id: Mapped[str] = mapped_column(nullable=False, primary_key=True)

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    owner: Mapped["UserModel"] = relationship(
        back_populates="auth_accounts", lazy="joined"
    )
