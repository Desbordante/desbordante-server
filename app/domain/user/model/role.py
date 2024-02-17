from enum import StrEnum, auto
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from uuid import UUID, uuid4
from app.db import Base


class RoleType(StrEnum):
    ANONYMOUS = auto()
    USER = auto()
    SUPPORT = auto()
    ADMIN = auto()
    DEVELOPER = auto()


class Role(Base):
    __tablename__ = "Role"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("User.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    type: Mapped[RoleType]
    permission_indices: Mapped[str]

    user = relationship("User")
