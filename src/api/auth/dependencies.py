from typing import Annotated

from fastapi import Depends

from src.api.dependencies import SessionManagerDep, UserCrudDep
from src.domain.auth.factory import OAuthClientFactory
from src.usecases.auth.get_oauth_authorization_redirect import (
    GetOAuthAuthorizationRedirectUseCase,
)
from src.usecases.auth.get_oauth_user_info import GetOAuthUserInfoUseCase
from src.usecases.auth.get_or_create_user_via_oauth import (
    GetOrCreateUserViaOAuthUseCase,
)
from src.usecases.auth.get_user_by_oauth import GetUserByOAuthUseCase
from src.usecases.auth.register_user_via_oauth import RegisterUserViaOAuthUseCase
from src.usecases.session.create_user_session import CreateUserSessionUseCase
from src.usecases.session.destroy_session import DestroySessionUseCase


async def get_oauth_client_factory() -> OAuthClientFactory:
    return OAuthClientFactory()


OAuthClientFactoryDep = Annotated[OAuthClientFactory, Depends(get_oauth_client_factory)]


async def get_oauth_authorization_redirect_use_case(
    oauth_factory: OAuthClientFactoryDep,
) -> GetOAuthAuthorizationRedirectUseCase:
    return GetOAuthAuthorizationRedirectUseCase(oauth_factory=oauth_factory)


GetOAuthAuthorizationRedirectUseCaseDep = Annotated[
    GetOAuthAuthorizationRedirectUseCase,
    Depends(get_oauth_authorization_redirect_use_case),
]


async def get_oauth_user_info_use_case(
    oauth_factory: OAuthClientFactoryDep,
) -> GetOAuthUserInfoUseCase:
    return GetOAuthUserInfoUseCase(oauth_factory=oauth_factory)


GetOAuthUserInfoUseCaseDep = Annotated[
    GetOAuthUserInfoUseCase, Depends(get_oauth_user_info_use_case)
]


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


async def get_destroy_session_use_case(
    session_manager: SessionManagerDep,
) -> DestroySessionUseCase:
    return DestroySessionUseCase(session_manager=session_manager)


DestroySessionUseCaseDep = Annotated[
    DestroySessionUseCase, Depends(get_destroy_session_use_case)
]
