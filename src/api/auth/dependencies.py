from typing import Annotated

from fastapi import Depends

from src.api.dependencies import UserCrudDep
from src.domain.auth.factory import OAuthClientFactory
from src.usecases.auth.get_or_create_user_via_oauth import (
    GetOrCreateUserViaOAuthUseCase,
)
from src.usecases.auth.get_user_by_oauth import GetUserByOAuthUseCase
from src.usecases.auth.get_oauth_authorization_redirect import (
    GetOAuthAuthorizationRedirectUseCase,
)
from src.usecases.auth.get_oauth_user_info import GetOAuthUserInfoUseCase
from src.usecases.auth.register_user_via_oauth import RegisterUserViaOAuthUseCase


async def get_oauth_client_factory() -> OAuthClientFactory:
    return OAuthClientFactory()


OAuthClientFactoryDep = Annotated[OAuthClientFactory, Depends(get_oauth_client_factory)]


async def get_oauth_authorization_redirect_use_case(
    client_factory: OAuthClientFactoryDep,
) -> GetOAuthAuthorizationRedirectUseCase:
    return GetOAuthAuthorizationRedirectUseCase(client_factory=client_factory)


GetOAuthAuthorizationRedirectUseCaseDep = Annotated[
    GetOAuthAuthorizationRedirectUseCase,
    Depends(get_oauth_authorization_redirect_use_case),
]


async def get_oauth_user_info_use_case(
    client_factory: OAuthClientFactoryDep,
) -> GetOAuthUserInfoUseCase:
    return GetOAuthUserInfoUseCase(client_factory=client_factory)


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
