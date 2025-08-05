# from typing import TYPE_CHECKING
# from uuid import UUID

# from sqlalchemy import JSONB, ForeignKey
# from sqlalchemy.orm import Mapped, mapped_column, relationship

# from src.db.annotations import uuid_pk
# from src.models.base_models import BaseModel
# from src.schemas.dataset_schemas import DatasetType, OneOfDatasetParams

# if TYPE_CHECKING:
#     from src.models.file_models import FileModel


# class DatasetModel(BaseModel):
#     id: Mapped[uuid_pk]

#     type: Mapped[DatasetType]

#     params: Mapped[OneOfDatasetParams] = mapped_column(JSONB)

#     file_id: Mapped[UUID] = mapped_column(ForeignKey("files.id", ondelete="CASCADE"))
#     file: Mapped["FileModel"] = relationship(lazy="joined")
# #
