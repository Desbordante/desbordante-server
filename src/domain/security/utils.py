import re
from datetime import datetime, timedelta, timezone
from typing import Any, Type

import jwt

from src.domain.security.config import settings
from src.domain.security.constants import pwd_context
from src.domain.security.exceptions import ExpiredTokenException, InvalidTokenException
from src.schemas.security_schemas import TokenPairSchema, TokenPayloadSchema


def create_token[T: TokenPayloadSchema](
    *, schema: Type[T], payload: dict[str, Any], expires_delta: timedelta
) -> TokenPairSchema:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = schema.model_validate({**payload, "exp": expire}).model_dump()
    token = jwt.encode(
        to_encode, settings.SECRET_KEY.get_secret_value(), algorithm=settings.ALGORITHM
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
            algorithms=[settings.ALGORITHM],
        )
        token_data = schema.model_validate(payload)

        if token_data.exp <= datetime.now(timezone.utc):
            raise ExpiredTokenException()

    except jwt.ExpiredSignatureError:
        raise ExpiredTokenException()

    except (jwt.PyJWTError, ValueError):
        raise InvalidTokenException()

    return token_data


def validate_password_strength(password: str) -> str:
    """
    Validates password strength requirements.

    Args:
        password: The password to validate

    Returns:
        The validated password

    Raises:
        ValueError: If password doesn't meet strength requirements
    """
    # if not re.search(r"[A-Z]", password):
    #     raise ValueError("Password must contain at least one uppercase letter")
    if not re.search(r"[a-zA-Z]", password):
        raise ValueError("Password must contain at least one letter")
    if not re.search(r"[0-9]", password):
        raise ValueError("Password must contain at least one digit")
    # if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
    #     raise ValueError("Password must contain at least one special character")
    return password


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
