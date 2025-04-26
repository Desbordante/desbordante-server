from typing import Annotated

from fastapi import Depends, Request

from api.constants import REFRESH_TOKEN_KEY
from src.api.dependencies import UserCrudDep
from src.schemas.auth_schemas import RefreshTokenPayloadSchema
from src.usecases.auth.authenticate_user import AuthenticateUserUseCase
from src.usecases.auth.create_tokens import CreateTokensUseCase
from src.usecases.auth.register_user import RegisterUserUseCase
from src.usecases.user.get_user_by_id import GetUserByIdUseCase
from usecases.auth.validate_token import ValidateTokenUseCase


async def get_register_user_use_case(user_crud: UserCrudDep) -> RegisterUserUseCase:
    return RegisterUserUseCase(user_crud=user_crud)


RegisterUserUseCaseDep = Annotated[
    RegisterUserUseCase, Depends(get_register_user_use_case)
]


async def get_create_tokens_use_case() -> CreateTokensUseCase:
    return CreateTokensUseCase()


CreateTokensUseCaseDep = Annotated[
    CreateTokensUseCase, Depends(get_create_tokens_use_case)
]


async def get_authenticate_user_use_case(
    user_crud: UserCrudDep,
) -> AuthenticateUserUseCase:
    return AuthenticateUserUseCase(user_crud=user_crud)


AuthenticateUserUseCaseDep = Annotated[
    AuthenticateUserUseCase, Depends(get_authenticate_user_use_case)
]


async def get_get_user_by_id_use_case(user_crud: UserCrudDep) -> GetUserByIdUseCase:
    return GetUserByIdUseCase(user_crud=user_crud)


GetUserByIdUseCaseDep = Annotated[
    GetUserByIdUseCase, Depends(get_get_user_by_id_use_case)
]


async def get_validate_token_use_case() -> ValidateTokenUseCase:
    return ValidateTokenUseCase()


ValidateTokenUseCaseDep = Annotated[
    ValidateTokenUseCase, Depends(get_validate_token_use_case)
]


async def get_refresh_token_payload(
    request: Request,
    validate_token: ValidateTokenUseCaseDep,
) -> RefreshTokenPayloadSchema:
    token = request.cookies.get(REFRESH_TOKEN_KEY)

    return validate_token(schema=RefreshTokenPayloadSchema, token=token)


RefreshTokenPayloadDep = Annotated[
    RefreshTokenPayloadSchema, Depends(get_refresh_token_payload)
]
