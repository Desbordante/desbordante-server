from datetime import datetime
from enum import auto
from enum import StrEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from app.db import Base


class AccountStatusType(StrEnum):
    EMAIL_VERIFICATION = auto()
    EMAIl_VERIFIED = auto()


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "User"
    full_name: Mapped[str]
    country: Mapped[str]
    company_or_affiliation: Mapped[str]
    occupation: Mapped[str]
    account_status: Mapped[AccountStatusType]
    created_at: Mapped[datetime]
    deleted_at: Mapped[datetime | None] = mapped_column(default=None)

    sessions = relationship("Session", back_populates="user")
    roles = relationship("Role", back_populates="user")
    feedbacks = relationship("Feedback", back_populates="user")
    tasks = relationship("Task", back_populates="user")
    files = relationship("FileInfo", back_populates="user")
