from datetime import datetime
from enum import auto
from enum import StrEnum
from uuid import UUID, uuid4
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db import Base


class SessionStatusType(StrEnum):
    INVALID = auto()
    VALID = auto()


class Session(Base):
    __tablename__ = "Session"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("User.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    device_id: Mapped[str] = mapped_column(
        ForeignKey("Device.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    status: Mapped[SessionStatusType]
    access_token_iat: Mapped[int | None] = mapped_column(default=None)
    refresh_token_iat: Mapped[int | None] = mapped_column(default=None)
    created_at: Mapped[datetime]

    device = relationship("Device")
    user = relationship("User")
