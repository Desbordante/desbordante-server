from datetime import datetime

from pydantic import ConfigDict, Field

from src.schemas.base_schemas import BaseSchema


class UserInfoSchema(BaseSchema):
    full_name: str = Field(
        min_length=1, max_length=50, description="The full name of the user"
    )

    country: str = Field(
        min_length=1, max_length=50, description="The country of the user"
    )

    company: str = Field(
        min_length=1, max_length=50, description="The company of the user"
    )

    occupation: str = Field(
        min_length=1, max_length=50, description="The occupation of the user"
    )


class UserSchema(UserInfoSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str

    created_at: datetime

    is_verified: bool
