from typing import Annotated

from fastapi import Depends, Request

from src.api.constants import REFRESH_TOKEN_KEY
from src.api.dependencies import UserCrudDep, ValidateTokenUseCaseDep
from src.schemas.auth_schemas import RefreshTokenPayloadSchema
from src.usecases.auth.authenticate_user import AuthenticateUserUseCase
from src.usecases.auth.create_tokens import CreateTokensUseCase
from src.usecases.auth.register_user import RegisterUserUseCase
from src.usecases.auth.reset_password import ResetPasswordUseCase
from src.usecases.auth.send_reset_email import SendResetEmailUseCase
from src.usecases.user.get_user_by_id import GetUserByIdUseCase


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


async def get_refresh_token_payload(
    request: Request,
    validate_token: ValidateTokenUseCaseDep,
) -> RefreshTokenPayloadSchema:
    token = request.cookies.get(REFRESH_TOKEN_KEY)

    return validate_token(schema=RefreshTokenPayloadSchema, token=token)


RefreshTokenPayloadDep = Annotated[
    RefreshTokenPayloadSchema, Depends(get_refresh_token_payload)
]


async def get_send_reset_email_use_case(
    user_crud: UserCrudDep,
) -> SendResetEmailUseCase:
    return SendResetEmailUseCase(user_crud=user_crud)


SendResetEmailUseCaseDep = Annotated[
    SendResetEmailUseCase, Depends(get_send_reset_email_use_case)
]


async def get_reset_password_use_case(user_crud: UserCrudDep) -> ResetPasswordUseCase:
    return ResetPasswordUseCase(user_crud=user_crud)


ResetPasswordUseCaseDep = Annotated[
    ResetPasswordUseCase, Depends(get_reset_password_use_case)
]
