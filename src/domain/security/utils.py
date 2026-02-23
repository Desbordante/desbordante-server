from datetime import datetime, timedelta, timezone
from typing import Any, Type

import jwt

from src.domain.security.config import settings
from src.domain.security.exceptions import ExpiredTokenException, InvalidTokenException
from src.schemas.security_schemas import TokenPairSchema, TokenPayloadSchema


def create_token[T: TokenPayloadSchema](
    *, schema: Type[T], payload: dict[str, Any], expires_delta: timedelta
) -> TokenPairSchema:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = schema.model_validate({**payload, "exp": expire}).model_dump()
    token = jwt.encode(
        to_encode,
        settings.SECRET_KEY.get_secret_value(),
        algorithm=settings.JWT_ALGORITHM,
    )
    return TokenPairSchema(
        token=token,
        expires=expire,
    )


def decode_token[T: TokenPayloadSchema](*, schema: Type[T], token: str) -> T:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY.get_secret_value(),
            algorithms=[settings.JWT_ALGORITHM],
        )
        token_data = schema.model_validate(payload)

        if token_data.exp <= datetime.now(timezone.utc):
            raise ExpiredTokenException()

    except jwt.ExpiredSignatureError:
        raise ExpiredTokenException()

    except (jwt.PyJWTError, ValueError):
        raise InvalidTokenException()

    return token_data
