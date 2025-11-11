from typing import Annotated

from fastapi import Depends

from src.domain.auth.factory import OAuthClientFactory
from src.usecases.auth.oauth_authorize import OAuthAuthorizeUseCase
from src.usecases.auth.oauth_callback import OAuthCallbackUseCase


async def get_oauth_client_factory() -> OAuthClientFactory:
    return OAuthClientFactory()


OAuthClientFactoryDep = Annotated[OAuthClientFactory, Depends(get_oauth_client_factory)]


async def get_oauth_authorize_use_case(
    client_factory: OAuthClientFactoryDep,
) -> OAuthAuthorizeUseCase:
    return OAuthAuthorizeUseCase(client_factory=client_factory)


OAuthAuthorizeUseCaseDep = Annotated[
    OAuthAuthorizeUseCase, Depends(get_oauth_authorize_use_case)
]


async def get_oauth_callback_use_case(
    client_factory: OAuthClientFactoryDep,
) -> OAuthCallbackUseCase:
    return OAuthCallbackUseCase(client_factory=client_factory)


OAuthCallbackUseCaseDep = Annotated[
    OAuthCallbackUseCase, Depends(get_oauth_callback_use_case)
]
