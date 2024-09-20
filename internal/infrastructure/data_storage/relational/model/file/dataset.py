import typing
from uuid import uuid4, UUID

from sqlalchemy import ForeignKey, Integer, ARRAY
from sqlalchemy.orm import mapped_column, Mapped, relationship

from internal.infrastructure.data_storage.relational.model import ORMBaseModel
from internal.infrastructure.data_storage.relational.model.file.file_metadata import FileMetadataORM

if typing.TYPE_CHECKING:
    from internal.infrastructure.data_storage.relational.model.task import TaskORM


class DatasetORM(ORMBaseModel):
    __tablename__ = "dataset"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    is_built_in: Mapped[bool] = mapped_column(default=False)
    header: Mapped[list[int]] = mapped_column(ARRAY(Integer), default=[])
    separator: Mapped[str]
    file_id: Mapped[UUID] = mapped_column(ForeignKey("file_metadata.id"), nullable=False)
    file_metadata: Mapped[FileMetadataORM] = relationship("FileMetadataORM")

    related_tasks: Mapped[list["TaskORM"]] = relationship(
        "TaskORM", back_populates="dataset"
    )

    # owner = relationship("UserORM")
