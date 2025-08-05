from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.annotations import str_non_nullable, uuid_pk
from src.models.base_models import BaseModel
from src.schemas.file_schemas import FileStatus

if TYPE_CHECKING:
    from src.models.user_models import UserModel


class FileModel(BaseModel):
    id: Mapped[uuid_pk]

    name: Mapped[str_non_nullable]
    size: Mapped[int]
    path: Mapped[str_non_nullable]

    status: Mapped[FileStatus] = mapped_column(default=FileStatus.Temporary)

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    owner: Mapped["UserModel"] = relationship(back_populates="files", lazy="joined")
