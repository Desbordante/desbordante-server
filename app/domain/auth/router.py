from typing import Annotated

from fastapi import APIRouter, Depends, Form, Response, status
from fastapi.security import OAuth2PasswordBearer

from app.domain.user.dependencies import get_user_service
from app.domain.user.schemas import UserSchema
from app.domain.user.service import UserService

from .config import settings

from .schemas import (
    LoginResponseSchema,
    RefreshResponseSchema,
    RefreshTokenSchema,
    RegisterFormDataSchema,
    RegisterResponseSchema,
)

from .dependencies import get_auth_service, get_authorized_user, get_refresh_token_data
from .service import AuthService
from .utils import set_auth_cookies, create_access_token, create_refresh_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter()


@router.post(
    "/login",
    response_model=LoginResponseSchema,
    responses={
        401: {
            "description": "Authentication failed",
            "content": {
                "application/json": {
                    "examples": {
                        "incorrect_credentials": {
                            "summary": "Incorrect credentials",
                            "value": {"detail": "Incorrect username or password"},
                        },
                    }
                }
            },
        }
    },
    summary="Authenticate user",
    description="Login with email and password to get access and refresh tokens",
)
async def login(
    response: Response,
    user: UserSchema = Depends(get_authorized_user),
    auth_service: AuthService = Depends(get_auth_service),
) -> LoginResponseSchema:
    """
    Authenticate user and return tokens:
    - Validates user credentials
    - Sets HTTP-only cookies with tokens
    - Returns access token and user info

    Raises:
        IncorrectCredentialsException: When email or password is incorrect
        CredentialsException: When token validation fails
    """
    access_token_pair = create_access_token(user=user)
    refresh_token_pair = create_refresh_token(user=user)
    set_auth_cookies(response, access_token_pair, refresh_token_pair)
    return LoginResponseSchema(access_token=access_token_pair[0], user=user)


@router.post(
    "/register",
    response_model=RegisterResponseSchema,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {
            "description": "Registration failed",
            "content": {
                "application/json": {
                    "examples": {
                        "user_exists": {
                            "summary": "User already exists",
                            "value": {
                                "detail": "User with email example@email.com already exists"
                            },
                        }
                    }
                }
            },
        },
        422: {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "password"],
                                "msg": "Password must contain at least one uppercase letter",
                                "type": "value_error",
                            }
                        ]
                    }
                }
            },
        },
    },
    summary="Register new user",
    description="Create new user account with email and password",
)
async def register(
    response: Response,
    form_data: Annotated[RegisterFormDataSchema, Form()],
    auth_service: AuthService = Depends(get_auth_service),
) -> RegisterResponseSchema:
    """
    Register new user:
    - Validates registration data
    - Creates new user account
    - Sets HTTP-only cookies with tokens
    - Returns access token and user info

    Raises:
        UserAlreadyExistsException: When email is already registered
        ValidationError: When form data validation fails
    """
    user = await auth_service.register_user(form_data)
    access_token_pair = create_access_token(user=user)
    refresh_token_pair = create_refresh_token(user=user)
    set_auth_cookies(response, access_token_pair, refresh_token_pair)
    return RegisterResponseSchema(access_token=access_token_pair[0], user=user)


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={204: {"description": "Successfully logged out"}},
    summary="Logout user",
    description="Clear authentication cookies",
)
async def logout(response: Response):
    """
    Logout current user:
    - Clears authentication cookies
    - Returns no content
    """
    response.delete_cookie(key=settings.ACCESS_TOKEN_KEY)
    response.delete_cookie(key=settings.REFRESH_TOKEN_KEY)
    return None


@router.post(
    "/refresh",
    response_model=LoginResponseSchema,
    responses={
        401: {
            "description": "Refresh token is invalid or expired",
            "content": {
                "application/json": {
                    "examples": {
                        "invalid_token": {
                            "summary": "Invalid token",
                            "value": {"detail": "Could not validate credentials"},
                        },
                    }
                }
            },
        },
        404: {
            "description": "User not found",
            "content": {"application/json": {"example": {"detail": "User not found"}}},
        },
    },
    summary="Refresh access token",
    description="Get new access token using refresh token from cookies",
)
async def refresh_token(
    response: Response,
    token_data: RefreshTokenSchema = Depends(get_refresh_token_data),
    user_service: UserService = Depends(get_user_service),
) -> RefreshResponseSchema:
    """
    Refresh access token using refresh token:
    - Validates refresh token from cookies
    - Creates new access token
    - Updates cookies with new tokens
    - Returns new access token and user info

    Raises:
        CredentialsException: When refresh token is missing or invalid
        UserNotFoundException: When user from token not found
    """
    user = await user_service.get_by_id(token_data.id)

    access_token_pair = create_access_token(user=user)
    refresh_token_pair = create_refresh_token(user=user)
    set_auth_cookies(response, access_token_pair, refresh_token_pair)
    return RefreshResponseSchema(access_token=access_token_pair[0], user=user)
