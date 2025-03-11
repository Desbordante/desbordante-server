from datetime import datetime
import re

from pydantic import EmailStr, Field, field_validator
from app.schemas import BaseSchema

from app.domain.user.schemas import UserSchema


class AccessTokenSchema(BaseSchema):
    id: int
    exp: datetime
    is_admin: bool


class RefreshTokenSchema(BaseSchema):
    id: int
    exp: datetime


class LoginResponseSchema(BaseSchema):
    access_token: str
    user: UserSchema


class RegisterResponseSchema(LoginResponseSchema):
    pass


class RefreshResponseSchema(LoginResponseSchema):
    pass


class RegisterUserSchema(BaseSchema):
    email: str
    password: str
    first_name: str
    last_name: str


class RegisterFormDataSchema(BaseSchema):
    email: EmailStr = Field(..., description="The email address of the user")
    password: str = Field(
        ...,
        min_length=8,
        description="The password of the user. Must contain at least one uppercase letter, one lowercase letter, one digit, and one special character",
    )
    first_name: str = Field(
        ..., min_length=1, max_length=50, description="The first name of the user"
    )
    last_name: str = Field(
        ..., min_length=1, max_length=50, description="The last name of the user"
    )

    @field_validator("password")
    def validate_password(cls, value):
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[0-9]", value):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password must contain at least one special character")
        return value


class LoginFormDataSchema(BaseSchema):
    email: EmailStr = Field(..., description="The email address of the user")
    password: str = Field(..., min_length=8, description="The password of the user")
