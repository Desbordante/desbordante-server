from typing import Annotated

from fastapi import Depends, Request

from src.api.dependencies import SessionManagerDep, UserCrudDep
from src.infrastructure.auth.oauth_service import AuthlibOAuthService
from src.usecases.auth.authenticate_via_oauth import AuthenticateViaOAuthUseCase
from src.usecases.auth.get_or_create_user_via_oauth import (
    GetOrCreateUserViaOAuthUseCase,
)
from src.usecases.auth.get_user_by_oauth import GetUserByOAuthUseCase
from src.usecases.auth.register_user_via_oauth import RegisterUserViaOAuthUseCase
from src.usecases.session.create_user_session import CreateUserSessionUseCase
from src.usecases.session.destroy_session import DestroySessionUseCase


def get_oauth_service(request: Request) -> AuthlibOAuthService:
    """Per-request OAuth service with request bound in constructor."""
    return AuthlibOAuthService(request=request)


OAuthServiceDep = Annotated[AuthlibOAuthService, Depends(get_oauth_service)]


async def get_get_user_by_oauth_use_case(
    user_crud: UserCrudDep,
) -> GetUserByOAuthUseCase:
    return GetUserByOAuthUseCase(user_crud=user_crud)


GetUserByOAuthUseCaseDep = Annotated[
    GetUserByOAuthUseCase, Depends(get_get_user_by_oauth_use_case)
]


async def get_register_user_via_oauth_use_case(
    user_crud: UserCrudDep,
) -> RegisterUserViaOAuthUseCase:
    return RegisterUserViaOAuthUseCase(user_crud=user_crud)


RegisterUserViaOAuthUseCaseDep = Annotated[
    RegisterUserViaOAuthUseCase, Depends(get_register_user_via_oauth_use_case)
]


async def get_or_create_user_via_oauth_use_case(
    get_user_by_oauth: GetUserByOAuthUseCaseDep,
    register_user_via_oauth: RegisterUserViaOAuthUseCaseDep,
) -> GetOrCreateUserViaOAuthUseCase:
    return GetOrCreateUserViaOAuthUseCase(
        get_user_by_oauth=get_user_by_oauth,
        register_user_via_oauth=register_user_via_oauth,
    )


GetOrCreateUserViaOAuthUseCaseDep = Annotated[
    GetOrCreateUserViaOAuthUseCase, Depends(get_or_create_user_via_oauth_use_case)
]


async def get_create_user_session_use_case(
    session_manager: SessionManagerDep,
) -> CreateUserSessionUseCase:
    return CreateUserSessionUseCase(session_manager=session_manager)


CreateUserSessionUseCaseDep = Annotated[
    CreateUserSessionUseCase, Depends(get_create_user_session_use_case)
]


async def get_authenticate_via_oauth_use_case(
    oauth_service: OAuthServiceDep,
    get_or_create_user_via_oauth: GetOrCreateUserViaOAuthUseCaseDep,
    create_session: CreateUserSessionUseCaseDep,
) -> AuthenticateViaOAuthUseCase:
    return AuthenticateViaOAuthUseCase(
        oauth_service=oauth_service,
        get_or_create_user_via_oauth=get_or_create_user_via_oauth,
        create_session=create_session,
    )


AuthenticateViaOAuthUseCaseDep = Annotated[
    AuthenticateViaOAuthUseCase, Depends(get_authenticate_via_oauth_use_case)
]


async def get_destroy_session_use_case(
    session_manager: SessionManagerDep,
) -> DestroySessionUseCase:
    return DestroySessionUseCase(session_manager=session_manager)


DestroySessionUseCaseDep = Annotated[
    DestroySessionUseCase, Depends(get_destroy_session_use_case)
]
