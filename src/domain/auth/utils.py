from datetime import datetime, timedelta, timezone
from typing import Any, Type

import jwt

from src.domain.auth.config import settings
from src.schemas.auth_schemas import TokenPairSchema, TokenPayloadSchema


def create_token[T: TokenPayloadSchema](
    *, schema: Type[T], payload: dict[str, Any], expires_delta: timedelta
) -> TokenPairSchema:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = schema.model_validate({**payload, "exp": expire}).model_dump()
    token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return TokenPairSchema(
        token=token,
        expires=expire,
    )


def decode_token[T: TokenPayloadSchema](*, schema: Type[T], token: str) -> T:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    return schema.model_validate(payload)
