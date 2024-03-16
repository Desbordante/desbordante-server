from datetime import datetime
from enum import auto
from enum import StrEnum
from uuid import UUID, uuid4
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db import Base


class CodeType(StrEnum):
    EMAIL_VERIFICATION_REQUIRED = auto()
    PASSWORD_RECOVERY_PENDING = auto()
    PASSWORD_RECOVERY_APPROVED = auto()


class Code(Base):
    __tablename__ = "Code"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    type: Mapped[CodeType]
    value: Mapped[int]
    expiring_date: Mapped[datetime]
    user_id: Mapped[UUID] = mapped_column(ForeignKey("User.id", onupdate="CASCADE"))
    device_id: Mapped[str | None] = mapped_column(
        ForeignKey("Device.id", ondelete="SET NULL", onupdate="CASCADE"), default=None
    )

    device = relationship("Device")
    user = relationship("User")
