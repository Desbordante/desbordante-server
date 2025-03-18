from uuid import UUID, uuid4
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.domain.user.models import User
from app.models import Base
from app.db.annotations import str_null_false


class File(Base):
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str_null_false]
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    owner: Mapped["User"] = relationship("User", back_populates="files")
