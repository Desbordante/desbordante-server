from typing import Annotated

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer

from app.domain.auth.config import settings
from app.domain.auth.exceptions import CredentialsException
from app.domain.auth.schemas import AccessTokenPayload, RefreshTokenPayload
from app.domain.auth.utils import validate_token

oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token", auto_error=False)
TokenDep = Annotated[str, Depends(oauth2)]


def get_access_token_payload(
    token: TokenDep,
    request: Request,
) -> AccessTokenPayload:
    if not token:
        cookiesToken = request.cookies.get(settings.ACCESS_TOKEN_KEY)
        if not cookiesToken:
            raise CredentialsException()

        token = cookiesToken

    return validate_token(token, AccessTokenPayload)


AccessTokenPayloadDep = Annotated[AccessTokenPayload, Depends(get_access_token_payload)]


def get_refresh_token_data(
    request: Request,
) -> RefreshTokenPayload:
    token = request.cookies.get(settings.REFRESH_TOKEN_KEY)
    if not token:
        raise CredentialsException()

    return validate_token(token, RefreshTokenPayload)


RefreshTokenPayloadDep = Annotated[RefreshTokenPayload, Depends(get_refresh_token_data)]


def get_optional_access_token_payload(
    token: TokenDep,
    request: Request,
) -> AccessTokenPayload | None:
    if not token:
        cookiesToken = request.cookies.get(settings.ACCESS_TOKEN_KEY)
        if not cookiesToken:
            return None

        token = cookiesToken

    return validate_token(token, AccessTokenPayload)


OptionalAccessTokenPayloadDep = Annotated[
    AccessTokenPayload | None, Depends(get_optional_access_token_payload)
]
