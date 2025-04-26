from sqlmodel import Field, Relationship

from _app.domain.user.models import User
from _app.models.models import BaseUUIDModel


class File(BaseUUIDModel, table=True):
    name: str
    byte_size: int
    path: str

    owner_id: int | None = Field(default=None, foreign_key="users.id")

    owner: User = Relationship(back_populates="files")
