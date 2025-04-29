from fastapi import Response

from src.api.constants import ACCESS_TOKEN_KEY, REFRESH_TOKEN_KEY
from src.schemas.security_schemas import TokenPairSchema


def set_auth_cookies(
    response: Response,
    access_token_pair: TokenPairSchema,
    refresh_token_pair: TokenPairSchema,
):
    """Set authentication cookies with tokens and their expiration times.

    Args:
        response: FastAPI response object
        access_token_pair: TokenPairSchema
        refresh_token_pair: TokenPairSchema
    """
    response.set_cookie(
        key=ACCESS_TOKEN_KEY,
        value=access_token_pair.token,
        expires=access_token_pair.expires,
        httponly=False,
        secure=True,
        samesite="lax",
        path="/",
    )

    response.set_cookie(
        key=REFRESH_TOKEN_KEY,
        value=refresh_token_pair.token,
        expires=refresh_token_pair.expires,
        httponly=True,
        secure=True,
        samesite="strict",
        path="/",
    )
