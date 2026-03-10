from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, declared_attr, mapped_column

from src.db.annotations import uuid_pk
from src.models.base_models import BaseModel


class TaskDatasetLink(BaseModel):
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return "task_dataset_links"

    task_id: Mapped[uuid_pk] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True
    )
    dataset_id: Mapped[uuid_pk] = mapped_column(
        ForeignKey("datasets.id", ondelete="CASCADE"), primary_key=True
    )
