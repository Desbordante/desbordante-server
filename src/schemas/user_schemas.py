from datetime import datetime

from pydantic import ConfigDict

from src.schemas.auth_schemas import OAuthProvider
from src.schemas.base_schemas import BaseSchema
from src.schemas.dataset_schemas import DatasetsStatsSchema


class UserSchema(BaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int

    is_active: bool
    is_admin: bool

    oauth_provider: OAuthProvider
    oauth_id: str

    created_at: datetime


class UserStatsSchema(BaseSchema):
    datasets: DatasetsStatsSchema
    storage_limit: int
