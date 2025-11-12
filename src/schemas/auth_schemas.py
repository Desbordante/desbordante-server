from enum import StrEnum

from src.schemas.base_schemas import BaseSchema


class OAuthProvider(StrEnum):
    GITHUB = "github"
    GOOGLE = "google"


class OAuthUserInfoSchema(BaseSchema):
    id: str


class OAuthCredsSchema(BaseSchema):
    provider: OAuthProvider
    oauth_id: str
