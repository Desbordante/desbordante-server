from enum import StrEnum

from src.schemas.base_schemas import BaseSchema


class AuthProvider(StrEnum):
    GITHUB = "github"
    GOOGLE = "google"


class AuthCredsSchema(BaseSchema):
    provider: AuthProvider
    account_id: str
    email: str


class AuthUserInfoSchema(BaseSchema):
    account_id: str
    email: str
    is_verified: bool


class AuthAccountSchema(BaseSchema):
    provider: AuthProvider
    account_id: str
