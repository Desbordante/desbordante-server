from datetime import datetime, timezone
from typing import Annotated
from fastapi import Depends, Form, Request
import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.domain.auth.exceptions import CredentialsException
from app.domain.auth.schemas import (
    AccessTokenSchema,
    LoginFormDataSchema,
    RefreshTokenSchema,
)
from app.domain.auth.service import AuthService
from app.domain.user.repository import UserRepository
from app.domain.user.schemas import UserSchema
from .config import settings


async def get_auth_service(session: AsyncSession = Depends(get_session)) -> AuthService:
    return AuthService(repository=UserRepository(session=session))


async def get_authorized_user(
    form_data: Annotated[LoginFormDataSchema, Form()],
    auth_service: AuthService = Depends(get_auth_service),
) -> UserSchema:
    return await auth_service.authenticate_user(
        email=form_data.email, password=form_data.password
    )


async def get_access_token_data(
    request: Request,
) -> AccessTokenSchema:
    # Try to get token from cookies first
    token = request.cookies.get(settings.ACCESS_TOKEN_KEY)

    # If not in cookies, try to get from headers
    if not token:
        authorization = request.headers.get("Authorization")
        if not authorization:
            raise CredentialsException()

        scheme, _, token = authorization.partition(" ")
        if scheme.lower() != "bearer":
            raise CredentialsException()

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = AccessTokenSchema.model_validate(payload)

        # Check if token has expired
        if token_data.exp <= datetime.now(timezone.utc):
            raise CredentialsException()

    except (jwt.PyJWTError, ValueError):
        raise CredentialsException()

    return token_data


async def get_refresh_token_data(
    request: Request,
) -> RefreshTokenSchema:
    token = request.cookies.get(settings.REFRESH_TOKEN_KEY)
    if not token:
        raise CredentialsException()

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = RefreshTokenSchema.model_validate(payload)

        # Check if token has expired
        if token_data.exp <= datetime.now(timezone.utc):
            raise CredentialsException()

    except (jwt.PyJWTError, ValueError):
        raise CredentialsException()

    return token_data
