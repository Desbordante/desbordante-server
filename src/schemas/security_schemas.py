from datetime import datetime

from src.schemas.base_schemas import BaseSchema


class TokenPairSchema(BaseSchema):
    token: str
    expires: datetime


class TokenPayloadSchema(BaseSchema):
    exp: datetime
    type: str
