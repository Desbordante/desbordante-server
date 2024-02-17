from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from uuid import UUID, uuid4
from app.db import Base


class Feedback(Base):
    __tablename__ = "Feedback"

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True, default=uuid4)
    user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("User.id", ondelete="SET NULL", onupdate="CASCADE")
    )
    rating: Mapped[int]
    subject: Mapped[str | None] = mapped_column(default=None)
    text: Mapped[str]
    created_at: Mapped[datetime]

    user = relationship("User")
