import re
from datetime import datetime

from pydantic import EmailStr, Field, field_validator

from src.schemas.base_schemas import BaseSchema
from src.schemas.user_schemas import UserSchema


class AuthResponseSchema(BaseSchema):
    access_token: str
    user: UserSchema


class RegisterUserSchema(BaseSchema):
    email: EmailStr = Field(max_length=255, description="The email address of the user")
    full_name: str = Field(
        min_length=1, max_length=50, description="The full name of the user"
    )

    password: str = Field(
        min_length=8,
        description="The password of the user. Must contain at least one uppercase letter, one lowercase letter, one digit, and one special character",
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

    @field_validator("password")
    def validate_password(cls, value: str) -> str:
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[0-9]", value):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password must contain at least one special character")
        return value


class AuthenticateUserSchema(BaseSchema):
    email: EmailStr = Field(max_length=255, description="The email address of the user")
    password: str = Field(
        min_length=8,
        description="The password of the user.",
    )


class TokenPairSchema(BaseSchema):
    token: str
    expires: datetime


class TokenPayloadSchema(BaseSchema):
    id: int
    exp: datetime
    type: str


class AccessTokenPayloadSchema(TokenPayloadSchema):
    type: str = "access"


class RefreshTokenPayloadSchema(TokenPayloadSchema):
    type: str = "refresh"
