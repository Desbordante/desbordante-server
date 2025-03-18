from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.domain.user.schemas import UserSchema


class FileBase(BaseModel):
    name: str


class FileCreate(FileBase):
    pass


class FileSchema(FileBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    owner_id: int
    owner: UserSchema
    created_at: datetime
    download_url: str | None = None  # This will be computed
