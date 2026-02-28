from typing import Literal

from src.schemas.base_schemas import BaseSchema


class AnonymousActorSchema(BaseSchema):
    user_id: None
    is_admin: Literal[False]


class AuthenticatedActorSchema(BaseSchema):
    user_id: int
    is_admin: bool
