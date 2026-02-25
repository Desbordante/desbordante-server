from datetime import datetime

from pydantic import ConfigDict

from src.schemas.base_schemas import BaseSchema
from src.schemas.dataset_schemas import DatasetsStatsSchema


class UserSchema(BaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int

    is_banned: bool
    is_admin: bool

    created_at: datetime


class UpdateUserStatusSchema(BaseSchema):
    is_banned: bool


class UserStatsSchema(BaseSchema):
    datasets: DatasetsStatsSchema
    storage_limit: int
