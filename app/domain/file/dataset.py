from uuid import UUID, uuid4
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ARRAY
from app.db import ORMBase
from app.db.session import ORMBaseModel
from app.domain.file.file import FileModel, FileORM


class DatasetORM(ORMBase):
    __tablename__ = "dataset"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    is_built_in: Mapped[bool] = mapped_column(default=False)
    header: Mapped[list[int]] = mapped_column(ARRAY(Integer), default=[])
    separator: Mapped[str]
    file_id: Mapped[UUID] = mapped_column(ForeignKey("file.id"), nullable=False)
    file: Mapped[FileORM] = relationship("FileORM")

    # user = relationship("UserORM")
    # task = relationship("TaskORM")


class DatasetModel(ORMBaseModel):
    id: UUID
    is_built_in: bool
    separator: str
    header: list[int]
    file: FileModel
