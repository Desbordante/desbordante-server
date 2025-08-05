from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.annotations import uuid_pk
from src.models.base_models import BaseModel

if TYPE_CHECKING:
    from src.models.file_models import FileModel


class MediaModel(BaseModel):
    id: Mapped[uuid_pk]

    width: Mapped[int]
    height: Mapped[int]

    file_id: Mapped[UUID] = mapped_column(ForeignKey("files.id", ondelete="CASCADE"))
    file: Mapped["FileModel"] = relationship(lazy="joined")
