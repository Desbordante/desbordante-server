from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from app.models import Base
from app.db.annotations import int_pk, str_uniq, str_null_false


class User(Base):
    id: Mapped[int_pk]
    email: Mapped[str_uniq]
    hashed_password: Mapped[str_null_false]
    first_name: Mapped[str_null_false]
    last_name: Mapped[str_null_false]
    is_admin: Mapped[bool] = mapped_column(default=False)

    files: Mapped[List["File"]] = relationship("File", back_populates="owner")  # noqa: F821
