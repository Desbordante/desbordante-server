from datetime import datetime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db import Base


class Device(Base):
    __tablename__ = "Device"

    id: Mapped[str] = mapped_column(primary_key=True, index=True)
    user_agent: Mapped[str | None] = mapped_column(default=None)
    browser: Mapped[str | None] = mapped_column(default=None)
    engine: Mapped[str | None] = mapped_column(default=None)
    os: Mapped[str | None] = mapped_column(default=None)
    os_version: Mapped[str | None] = mapped_column(default=None)
    device: Mapped[str | None] = mapped_column(default=None)
    cpu: Mapped[str | None] = mapped_column(default=None)
    screen: Mapped[str | None] = mapped_column(default=None)
    plugins: Mapped[str | None] = mapped_column(default=None)
    time_zone: Mapped[str | None] = mapped_column(default=None)
    language: Mapped[str | None] = mapped_column(default=None)
    created_at: Mapped[datetime]

    session = relationship("Session", back_populates="device")
