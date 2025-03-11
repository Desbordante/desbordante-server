from app.schemas import BaseSchema
from pydantic import ConfigDict


class UserSchema(BaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    is_admin: bool
    first_name: str
    last_name: str
