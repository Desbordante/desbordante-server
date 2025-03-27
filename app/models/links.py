from uuid import UUID

from sqlmodel import Field

from app.models.models import BaseModel


class FileTaskLink(BaseModel, table=True):
    file_id: UUID | None = Field(default=None, foreign_key="files.id", primary_key=True)
    task_id: UUID | None = Field(default=None, foreign_key="tasks.id", primary_key=True)
