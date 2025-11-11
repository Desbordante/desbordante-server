from typing import Annotated

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.constants import ACCESS_TOKEN_KEY
from src.crud.dataset_crud import DatasetCrud
from src.crud.user_crud import UserCrud
from src.db.session import get_session
from src.exceptions import ForbiddenException
from src.infrastructure.session.starsessions_adapter import StarsessionsAdapter
from src.models.user_models import UserModel
from src.schemas.auth_schemas import AccessTokenPayloadSchema
from src.schemas.base_schemas import PaginationParamsSchema
from src.schemas.session_schemas import UserSessionSchema
from src.usecases.account.send_confirmation_email import SendConfirmationEmailUseCase
from src.usecases.auth.validate_token import ValidateTokenUseCase
from src.usecases.session.get_user_session import GetUserSessionUseCase
from src.usecases.user.get_user_by_id import GetUserByIdUseCase

oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token", auto_error=False)
TokenDep = Annotated[str, Depends(oauth2)]

SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def get_user_crud(session: SessionDep) -> UserCrud:
    return UserCrud(session=session)


UserCrudDep = Annotated[UserCrud, Depends(get_user_crud)]


async def get_dataset_crud(session: SessionDep) -> DatasetCrud:
    return DatasetCrud(session=session)


DatasetCrudDep = Annotated[DatasetCrud, Depends(get_dataset_crud)]


async def get_validate_token_use_case() -> ValidateTokenUseCase:
    return ValidateTokenUseCase()


ValidateTokenUseCaseDep = Annotated[
    ValidateTokenUseCase, Depends(get_validate_token_use_case)
]


async def get_access_token_payload(
    request: Request,
    header_token: TokenDep,
    validate_token: ValidateTokenUseCaseDep,
) -> AccessTokenPayloadSchema:
    token = header_token if header_token else request.cookies.get(ACCESS_TOKEN_KEY)

    return validate_token(schema=AccessTokenPayloadSchema, token=token)


AccessTokenPayloadDep = Annotated[
    AccessTokenPayloadSchema, Depends(get_access_token_payload)
]


async def get_optional_access_token_payload(
    request: Request,
    header_token: TokenDep,
    validate_token: ValidateTokenUseCaseDep,
) -> AccessTokenPayloadSchema | None:
    token = header_token if header_token else request.cookies.get(ACCESS_TOKEN_KEY)

    if not token:
        return None

    return validate_token(schema=AccessTokenPayloadSchema, token=token)


OptionalAccessTokenPayloadDep = Annotated[
    AccessTokenPayloadSchema | None, Depends(get_optional_access_token_payload)
]


async def get_get_user_by_id_use_case(user_crud: UserCrudDep) -> GetUserByIdUseCase:
    return GetUserByIdUseCase(user_crud=user_crud)


GetUserByIdUseCaseDep = Annotated[
    GetUserByIdUseCase, Depends(get_get_user_by_id_use_case)
]


async def get_authorized_user(
    access_token_payload: AccessTokenPayloadDep,
    get_user_by_id: GetUserByIdUseCaseDep,
) -> UserModel:
    return await get_user_by_id(id=access_token_payload.id)


AuthorizedUserDep = Annotated[UserModel, Depends(get_authorized_user)]


async def get_optionally_authorized_user(
    access_token_payload: OptionalAccessTokenPayloadDep,
    get_user_by_id: GetUserByIdUseCaseDep,
) -> UserModel | None:
    if access_token_payload:
        return await get_user_by_id(id=access_token_payload.id)
    return None


class VerificationDep:
    def __init__(self, should_be_verified: bool = True):
        self.should_be_verified = should_be_verified

    def __call__(self, user: AuthorizedUserDep) -> UserModel:
        # TODO: Implement is_verified when needed (removed from UserModel)
        return user


VerifiedUserDep = Annotated[UserModel, Depends(VerificationDep())]


async def get_send_confirmation_email_use_case() -> SendConfirmationEmailUseCase:
    return SendConfirmationEmailUseCase()


SendConfirmationEmailUseCaseDep = Annotated[
    SendConfirmationEmailUseCase, Depends(get_send_confirmation_email_use_case)
]


async def get_session_adapter(request: Request) -> StarsessionsAdapter:
    return StarsessionsAdapter(request=request)


SessionAdapterDep = Annotated[StarsessionsAdapter, Depends(get_session_adapter)]


async def get_user_session(session_adapter: SessionAdapterDep) -> UserSessionSchema:
    """Get user session data."""
    get_user_session = GetUserSessionUseCase(session_adapter=session_adapter)
    return await get_user_session()


UserSessionDep = Annotated[UserSessionSchema, Depends(get_user_session)]


async def get_current_user(
    user_session: UserSessionDep,
    get_user_by_id: GetUserByIdUseCaseDep,
) -> UserModel:
    """Get authenticated user model from session."""
    return await get_user_by_id(id=user_session.user_id)


CurrentUserDep = Annotated[UserModel, Depends(get_current_user)]


async def get_admin_session(user_session: UserSessionDep) -> UserSessionSchema:
    """Require admin user from session."""
    if not user_session.is_admin:
        raise ForbiddenException("Admin access required")
    return user_session


AdminSessionDep = Annotated[UserSessionSchema, Depends(get_admin_session)]


PaginationParamsDep = Annotated[PaginationParamsSchema, Depends(PaginationParamsSchema)]
