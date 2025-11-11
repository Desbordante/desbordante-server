from datetime import datetime

from pydantic import ConfigDict

from src.schemas.auth_schemas import OAuthProvider
from src.schemas.base_schemas import BaseSchema


class UserSchema(BaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int

    oauth_provider: OAuthProvider
    oauth_id: str

    created_at: datetime
