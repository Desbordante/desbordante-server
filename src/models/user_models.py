from sqlalchemy.orm import Mapped

from src.db.annotations import int_pk, str_non_nullable, str_uniq
from src.models.base_models import BaseModel


class UserModel(BaseModel):
    id: Mapped[int_pk]
    email: Mapped[str_uniq]
    full_name: Mapped[str_non_nullable]

    hashed_password: Mapped[str_non_nullable]

    country: Mapped[str_non_nullable]
    company: Mapped[str_non_nullable]
    occupation: Mapped[str_non_nullable]
