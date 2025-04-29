from pydantic import ValidationInfo, field_validator

from src.domain.security.utils import validate_password_strength
from src.schemas.base_schemas import BaseSchema, OptionalSchema
from src.schemas.security_schemas import TokenPayloadSchema, password_field
from src.schemas.user_schemas import UserInfoSchema


class EmailTokenPayloadSchema(TokenPayloadSchema):
    email: str


class ConfirmationTokenPayloadSchema(EmailTokenPayloadSchema):
    type: str = "confirmation"


class ChangePasswordSchema(BaseSchema):
    current_password: str

    new_password: str = password_field(
        "The new password of the user. Must contain at least one uppercase letter, one lowercase letter, one digit, and one special character"
    )

    @field_validator("new_password")
    def validate_password(cls, value: str) -> str:
        return validate_password_strength(value)

    @field_validator("new_password")
    def passwords_match(cls, value: str, info: ValidationInfo) -> str:
        if "current_password" in info.data and value == info.data["current_password"]:
            raise ValueError("New password cannot be the same as the current password")
        return value


class UpdateUserInfoSchema(UserInfoSchema, OptionalSchema):
    pass
