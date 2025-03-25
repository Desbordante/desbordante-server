from datetime import datetime, timezone
from typing import Annotated

import jwt
from fastapi import Depends, Form, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.dependencies import SessionDep
from app.domain.auth.exceptions import CredentialsException
from app.domain.auth.schemas import (
    AccessTokenPayload,
    RefreshTokenPayload,
    UserLogin,
)
from app.domain.auth.service import AuthService
from app.domain.user.models import User
from app.domain.user.schemas import UserPublic
from app.repository import BaseRepository

from .config import settings

oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token", auto_error=False)
TokenDep = Annotated[str, Depends(oauth2)]


def get_auth_service(session: SessionDep) -> AuthService:
    return AuthService(repository=BaseRepository(model=User, session=session))


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


def get_authorized_user(
    form_data: Annotated[UserLogin, Form()],
    auth_service: AuthServiceDep,
) -> UserPublic:
    return auth_service.authenticate_user(form_data)


AuthorizedUserDep = Annotated[UserPublic, Depends(get_authorized_user)]


def get_oauth2_authorized_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: AuthServiceDep,
) -> UserPublic:
    return auth_service.authenticate_user(
        UserLogin(email=form_data.username, password=form_data.password)
    )


OAuth2uthorizedUserDep = Annotated[UserPublic, Depends(get_oauth2_authorized_user)]


def get_access_token_payload(
    token: TokenDep,
    request: Request,
) -> AccessTokenPayload:
    if not token:
        cookiesToken = request.cookies.get(settings.ACCESS_TOKEN_KEY)
        if not cookiesToken:
            raise CredentialsException()

        token = cookiesToken

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = AccessTokenPayload.model_validate(payload)

        # Check if token has expired
        if token_data.exp <= datetime.now(timezone.utc):
            raise CredentialsException()

    except (jwt.PyJWTError, ValueError):
        raise CredentialsException()

    return token_data


AccessTokenPayloadDep = Annotated[AccessTokenPayload, Depends(get_access_token_payload)]


def get_refresh_token_data(
    request: Request,
) -> RefreshTokenPayload:
    token = request.cookies.get(settings.REFRESH_TOKEN_KEY)
    if not token:
        raise CredentialsException()

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = RefreshTokenPayload.model_validate(payload)

        # Check if token has expired
        if token_data.exp <= datetime.now(timezone.utc):
            raise CredentialsException()

    except (jwt.PyJWTError, ValueError):
        raise CredentialsException()

    return token_data


RefreshTokenPayloadDep = Annotated[RefreshTokenPayload, Depends(get_refresh_token_data)]
