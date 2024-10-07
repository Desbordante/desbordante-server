from pathlib import Path
from uuid import UUID, uuid4

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import mapped_column, Mapped

from internal.infrastructure.data_storage import settings
from internal.infrastructure.data_storage.relational.model import ORMBaseModel


class FileMetadataORM(ORMBaseModel):
    __tablename__ = "file_metadata"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    mime_type: Mapped[str]
    file_name: Mapped[UUID]
    original_file_name: Mapped[str]

    @hybrid_property
    def path_to_file(self) -> Path:
        return Path(settings.uploaded_files_dir_path, str(self.file_name))
