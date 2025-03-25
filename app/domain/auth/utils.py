from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple

import jwt
from fastapi import Response

from app.domain.user.schemas import UserPublic

from .config import settings
from .schemas import AccessTokenPayload, RefreshTokenPayload


def create_access_token(
    user: UserPublic, expires_delta: Optional[timedelta] = None
) -> Tuple[str, datetime]:
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode = AccessTokenPayload(
        id=user.id, exp=expire, is_admin=user.is_admin
    ).model_dump()
    token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token, expire


def create_refresh_token(
    user: UserPublic, expires_delta: Optional[timedelta] = None
) -> Tuple[str, datetime]:
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    to_encode = RefreshTokenPayload(id=user.id, exp=expire).model_dump()
    token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token, expire


def set_auth_cookies(
    response: Response,
    access_token_pair: Tuple[str, datetime],
    refresh_token_pair: Tuple[str, datetime],
):
    """Set authentication cookies with tokens and their expiration times.

    Args:
        response: FastAPI response object
        access_token_pair: Tuple of (access_token, expiration)
        refresh_token_pair: Tuple of (refresh_token, expiration)
    """
    access_token, access_expires = access_token_pair
    refresh_token, refresh_expires = refresh_token_pair

    response.set_cookie(
        key=settings.ACCESS_TOKEN_KEY,
        value=access_token,
        expires=access_expires,
        httponly=False,
        secure=True,
        samesite="lax",
        path="/",
    )

    response.set_cookie(
        key=settings.REFRESH_TOKEN_KEY,
        value=refresh_token,
        expires=refresh_expires,
        httponly=True,
        secure=True,
        samesite="strict",
        path="/",
    )
