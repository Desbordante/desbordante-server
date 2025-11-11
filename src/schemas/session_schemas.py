from src.schemas.base_schemas import BaseSchema


class UserSessionSchema(BaseSchema):
    """Schema for user session data."""

    user_id: int
    is_admin: bool
