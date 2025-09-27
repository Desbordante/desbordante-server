from datetime import datetime
from typing import Any

from pydantic import Field

from src.schemas.base_schemas import BaseSchema


class TokenPairSchema(BaseSchema):
    token: str
    expires: datetime


class TokenPayloadSchema(BaseSchema):
    exp: datetime
    type: str


def password_field(
    description: str = "The password of the user. Must contain at least one letter, one digit",
) -> Any:
    """
    Creates a password field with standard validation requirements.

    Args:
        description: Custom description for the field

    Returns:
        A Field with password validation settings
    """
    return Field(
        min_length=8,
        max_length=50,
        description=description,
    )
