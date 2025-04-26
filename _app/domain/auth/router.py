from typing import Annotated

from fastapi import APIRouter, Depends, Form, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from _app.domain.user.dependencies import UserServiceDep

from .config import settings
from .dependencies import (
    AuthServiceDep,
    RefreshTokenPayloadDep,
)
from .schemas import (
    LoginResponse,
    RefreshResponse,
    RegisterResponse,
    TokenResponse,
    UserLogin,
    UserRegister,
)
from .utils import create_access_token, create_refresh_token, set_auth_cookies

router = APIRouter()


@router.post(
    "/token",
    response_model=TokenResponse,
    summary="Get access token (API docs only)",
    description="Get access token using OAuth2 password flow. This endpoint is for Swagger/OpenAPI documentation testing only.",
)
def get_access_token(
    auth_service: AuthServiceDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> TokenResponse:
    """
    Get access token using OAuth2 password flow.

    Note:
        This endpoint is only for testing in Swagger/OpenAPI documentation.
        Frontend applications should use /login endpoint instead, which:
        - Sets secure HTTP-only cookies
        - Provides proper CSRF protection
        - Handles refresh tokens

    Args:
        user: Authenticated user from OAuth2 password flow

    Returns:
        Access token response with token and type
    """
    user = auth_service.authenticate_user(
        UserLogin(email=form_data.username, password=form_data.password)
    )
    access_token_pair = create_access_token(user=user)
    return TokenResponse(access_token=access_token_pair[0])


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Authenticate user",
    description="Authenticate user with email and password, set auth cookies and return tokens",
    responses={
        401: {
            "description": "Invalid credentials",
            "content": {
                "application/json": {
                    "example": {"detail": "Incorrect email or password"}
                }
            },
        }
    },
)
def login(
    response: Response,
    auth_service: AuthServiceDep,
    form_data: Annotated[UserLogin, Form()],
) -> LoginResponse:
    """
    Authenticate user and return tokens:
    - Validates user credentials
    - Sets HTTP-only cookies with tokens
    - Returns access token and user info

    Returns:
        LoginResponse: Access token and user information

    Raises:
        UnauthorizedException: When credentials are invalid
    """
    user = auth_service.authenticate_user(form_data)
    access_token_pair = create_access_token(user=user)
    refresh_token_pair = create_refresh_token(user=user)
    set_auth_cookies(response, access_token_pair, refresh_token_pair)
    return LoginResponse(access_token=access_token_pair[0], user=user)


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
    description="Create new user account with email and password",
    responses={
        400: {
            "description": "Validation error",
            "content": {
                "application/json": {
                    "example": {"detail": "Password must contain at least 8 characters"}
                }
            },
        },
        409: {
            "description": "User already exists",
            "content": {
                "application/json": {
                    "example": {"detail": "User with this email already exists"}
                }
            },
        },
    },
)
def register(
    response: Response,
    form_data: Annotated[UserRegister, Form()],
    auth_service: AuthServiceDep,
) -> RegisterResponse:
    """
    Register new user:
    - Validates registration data
    - Creates new user account
    - Sets HTTP-only cookies with tokens
    - Returns access token and user info

    Returns:
        RegisterResponse: Access token and user information

    Raises:
        ValidationException: When registration data is invalid
        ResourceAlreadyExistsException: When user with email already exists
    """
    user = auth_service.register_user(form_data)
    access_token_pair = create_access_token(user=user)
    refresh_token_pair = create_refresh_token(user=user)
    set_auth_cookies(response, access_token_pair, refresh_token_pair)
    return RegisterResponse(access_token=access_token_pair[0], user=user)


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Logout user",
    description="Clear authentication cookies",
)
def logout(response: Response):
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
    response_model=RefreshResponse,
    summary="Refresh access token",
    description="Get new access token using refresh token from cookies",
)
def refresh_token(
    response: Response,
    refresh_token_payload: RefreshTokenPayloadDep,
    user_service: UserServiceDep,
) -> RefreshResponse:
    """
    Refresh access token using refresh token:
    - Validates refresh token from cookies
    - Creates new access token
    - Updates cookies with new tokens
    - Returns new access token and user info
    """
    user = user_service.get_by_id(refresh_token_payload.id)

    access_token_pair = create_access_token(user=user)
    refresh_token_pair = create_refresh_token(user=user)
    set_auth_cookies(response, access_token_pair, refresh_token_pair)
    return RefreshResponse(access_token=access_token_pair[0], user=user)
