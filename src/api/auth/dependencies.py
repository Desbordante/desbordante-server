from typing import Annotated

from fastapi import Depends, Request

from src.api.dependencies import AuthAccountCrudDep, SessionManagerDep, UserCrudDep
from src.infrastructure.auth.auth_service import AuthService
from src.usecases.auth.authenticate_via_provider import AuthenticateViaProviderUseCase
from src.usecases.auth.get_or_create_user_via_provider import (
    GetOrCreateUserViaProviderUseCase,
)
from src.usecases.auth.register_user_via_provider import RegisterUserViaProviderUseCase
from src.usecases.session.create_user_session import CreateUserSessionUseCase
from src.usecases.session.destroy_session import DestroySessionUseCase


def get_auth_service(request: Request) -> AuthService:
    """Per-request auth service with request bound in constructor."""
    return AuthService(request=request)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


async def get_register_user_via_provider_use_case(
    user_crud: UserCrudDep,
) -> RegisterUserViaProviderUseCase:
    return RegisterUserViaProviderUseCase(user_crud=user_crud)


RegisterUserViaProviderUseCaseDep = Annotated[
    RegisterUserViaProviderUseCase, Depends(get_register_user_via_provider_use_case)
]


async def get_or_create_user_via_provider_use_case(
    register_user_via_provider: RegisterUserViaProviderUseCaseDep,
    auth_account_crud: AuthAccountCrudDep,
) -> GetOrCreateUserViaProviderUseCase:
    return GetOrCreateUserViaProviderUseCase(
        auth_account_crud=auth_account_crud,
        register_user_via_provider=register_user_via_provider,
    )


GetOrCreateUserViaProviderUseCaseDep = Annotated[
    GetOrCreateUserViaProviderUseCase, Depends(get_or_create_user_via_provider_use_case)
]


async def get_create_user_session_use_case(
    session_manager: SessionManagerDep,
) -> CreateUserSessionUseCase:
    return CreateUserSessionUseCase(session_manager=session_manager)


CreateUserSessionUseCaseDep = Annotated[
    CreateUserSessionUseCase, Depends(get_create_user_session_use_case)
]


async def get_authenticate_via_provider_use_case(
    auth_service: AuthServiceDep,
    get_or_create_user_via_provider: GetOrCreateUserViaProviderUseCaseDep,
    create_session: CreateUserSessionUseCaseDep,
) -> AuthenticateViaProviderUseCase:
    return AuthenticateViaProviderUseCase(
        auth_service=auth_service,
        get_or_create_user_via_provider=get_or_create_user_via_provider,
        create_session=create_session,
    )


AuthenticateViaProviderUseCaseDep = Annotated[
    AuthenticateViaProviderUseCase, Depends(get_authenticate_via_provider_use_case)
]


async def get_destroy_session_use_case(
    session_manager: SessionManagerDep,
) -> DestroySessionUseCase:
    return DestroySessionUseCase(session_manager=session_manager)


DestroySessionUseCaseDep = Annotated[
    DestroySessionUseCase, Depends(get_destroy_session_use_case)
]
