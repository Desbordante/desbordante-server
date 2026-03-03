from datetime import datetime

from src.schemas.base_schemas import BaseSchema


class SessionSchema(BaseSchema):
    user_id: int
    is_admin: bool
    created_at: datetime
