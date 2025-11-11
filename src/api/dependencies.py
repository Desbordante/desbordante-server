from typing import Annotated

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.dataset_crud import DatasetCrud
from src.crud.user_crud import UserCrud
from src.db.session import get_session
from src.exceptions import ForbiddenException
from src.infrastructure.session.starsessions_adapter import StarsessionsAdapter
from src.schemas.base_schemas import PaginationParamsSchema
from src.schemas.session_schemas import UserSessionSchema
from src.usecases.account.send_confirmation_email import SendConfirmationEmailUseCase
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


async def get_get_user_by_id_use_case(user_crud: UserCrudDep) -> GetUserByIdUseCase:
    return GetUserByIdUseCase(user_crud=user_crud)


GetUserByIdUseCaseDep = Annotated[
    GetUserByIdUseCase, Depends(get_get_user_by_id_use_case)
]


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


async def get_admin_session(user_session: UserSessionDep) -> UserSessionSchema:
    """Require admin user from session."""
    if not user_session.is_admin:
        raise ForbiddenException("Admin access required")
    return user_session


AdminSessionDep = Annotated[UserSessionSchema, Depends(get_admin_session)]


PaginationParamsDep = Annotated[PaginationParamsSchema, Depends(PaginationParamsSchema)]
