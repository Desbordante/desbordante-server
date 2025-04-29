from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, declared_attr, mapped_column, relationship

from src.db.annotations import str_non_nullable, uuid_pk
from src.models.base_models import BaseModel
from src.schemas.file_schemas import DatasetType, FileType, OneOfDatasetParams

if TYPE_CHECKING:
    from src.models.user_models import UserModel


class FileModel(BaseModel):
    id: Mapped[uuid_pk]

    type: Mapped[FileType]

    name: Mapped[str_non_nullable]
    byte_size: Mapped[int]
    path: Mapped[str_non_nullable]

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    owner: Mapped["UserModel"] = relationship(back_populates="files", lazy="joined")


class DatasetModel(BaseModel):
    id: Mapped[uuid_pk]

    type: Mapped[DatasetType]

    params: Mapped[OneOfDatasetParams] = mapped_column(JSONB)

    file_id: Mapped[UUID] = mapped_column(ForeignKey("files.id", ondelete="CASCADE"))
    file: Mapped["FileModel"] = relationship(lazy="joined")


class MediaModel(BaseModel):
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return "media"

    id: Mapped[uuid_pk]

    width: Mapped[int]
    height: Mapped[int]

    file_id: Mapped[UUID] = mapped_column(ForeignKey("files.id", ondelete="CASCADE"))
    file: Mapped["FileModel"] = relationship(lazy="joined")
