import re
from datetime import datetime

from pydantic import EmailStr, Field, field_validator

from _app.domain.user.schemas import UserPublic
from _app.schemas.schemas import BaseSchema


class UserLogin(BaseSchema):
    email: EmailStr = Field(description="The email address of the user")
    password: str = Field(min_length=8, description="The password of the user")


class UserRegister(BaseSchema):
    first_name: str = Field(
        min_length=1, max_length=50, description="The first name of the user"
    )
    last_name: str = Field(
        min_length=1, max_length=50, description="The last name of the user"
    )
    email: EmailStr = Field(max_length=255, description="The email address of the user")

    password: str = Field(
        min_length=8,
        description="The password of the user. Must contain at least one uppercase letter, one lowercase letter, one digit, and one special character",
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


class TokenResponse(BaseSchema):
    access_token: str
    token_type: str = "bearer"


class AuthResponse(BaseSchema):
    access_token: str
    user: UserPublic


class LoginResponse(AuthResponse):
    token_type: str = "bearer"


class RegisterResponse(AuthResponse):
    pass


class RefreshResponse(AuthResponse):
    pass


class TokenPayload(BaseSchema):
    id: int
    exp: datetime
    type: str


class AccessTokenPayload(TokenPayload):
    type: str = "access"
    is_admin: bool


class RefreshTokenPayload(TokenPayload):
    type: str = "refresh"
