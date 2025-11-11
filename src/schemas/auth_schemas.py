from enum import StrEnum

from pydantic import EmailStr, Field, field_validator

from src.domain.security.utils import validate_password_strength
from src.schemas.base_schemas import BaseSchema
from src.schemas.security_schemas import TokenPayloadSchema, password_field
from src.schemas.user_schemas import UserInfoSchema, UserSchema


class OAuthProvider(StrEnum):
    GITHUB = "github"
    GOOGLE = "google"


class OAuthUserInfoSchema(BaseSchema):
    id: str


class OAuthCredentialsSchema(BaseSchema):
    provider: OAuthProvider
    oauth_id: str


class AuthResponseSchema(BaseSchema):
    access_token: str
    user: UserSchema


class RegisterUserSchema(UserInfoSchema):
    email: EmailStr = Field(max_length=255, description="The email address of the user")

    password: str = password_field()

    @field_validator("password")
    def validate_password(cls, value: str) -> str:
        return validate_password_strength(value)


class AuthenticateUserSchema(BaseSchema):
    email: EmailStr = Field(max_length=255, description="The email address of the user")
    password: str = Field(
        min_length=8,
        description="The password of the user.",
    )


class ResetPasswordSchema(BaseSchema):
    new_password: str = password_field()

    @field_validator("new_password")
    def validate_password(cls, value: str) -> str:
        return validate_password_strength(value)


class AuthTokenPayloadSchema(TokenPayloadSchema):
    id: int


class AccessTokenPayloadSchema(AuthTokenPayloadSchema):
    type: str = "access"


class RefreshTokenPayloadSchema(AuthTokenPayloadSchema):
    type: str = "refresh"
