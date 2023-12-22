from datetime import datetime
from pydantic import BaseModel


class BaseTaskResult(BaseModel):
    created_at: datetime
    deleted_at: datetime | None = None
