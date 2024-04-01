from pathlib import Path
from uuid import UUID, uuid4
from sqlalchemy.orm import Mapped, mapped_column
from app.db import ORMBase
from app.db.session import ORMBaseModel
from sqlalchemy.ext.hybrid import hybrid_property

from app.settings import settings


class FileORM(ORMBase):
    __tablename__ = "file"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    mime_type: Mapped[str]
    file_name: Mapped[UUID]
    original_file_name: Mapped[str]

    @hybrid_property
    def path_to_file(self) -> Path:
        return Path(settings.uploaded_files_dir_path, str(self.file_name))


class FileModel(ORMBaseModel):
    id: UUID

    mime_type: str
    file_name: UUID
    original_file_name: str
