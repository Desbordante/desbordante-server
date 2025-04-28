from datetime import datetime

from pydantic import ConfigDict

from src.schemas.base_schemas import BaseSchema


class UserSchema(BaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    full_name: str

    country: str
    company: str
    occupation: str

    created_at: datetime
