from pydantic import EmailStr, Field, field_validator

from src.domain.security.utils import validate_password_strength
from src.schemas.base_schemas import BaseSchema
from src.schemas.security_schemas import TokenPayloadSchema, password_field
from src.schemas.user_schemas import UserSchema


class AuthResponseSchema(BaseSchema):
    access_token: str
    user: UserSchema


class RegisterUserSchema(BaseSchema):
    email: EmailStr = Field(max_length=255, description="The email address of the user")
    full_name: str = Field(
        min_length=1, max_length=50, description="The full name of the user"
    )

    password: str = password_field(
        "The password of the user. Must contain at least one uppercase letter, one lowercase letter, one digit, and one special character"
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
        return validate_password_strength(value)


class AuthenticateUserSchema(BaseSchema):
    email: EmailStr = Field(max_length=255, description="The email address of the user")
    password: str = Field(
        min_length=8,
        description="The password of the user.",
    )


class AuthTokenPayloadSchema(TokenPayloadSchema):
    id: int


class AccessTokenPayloadSchema(AuthTokenPayloadSchema):
    type: str = "access"


class RefreshTokenPayloadSchema(AuthTokenPayloadSchema):
    type: str = "refresh"
