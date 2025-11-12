from typing import Annotated

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.dataset_crud import DatasetCrud
from src.crud.user_crud import UserCrud
from src.db.session import get_session
from src.domain.session.manager import SessionManager
from src.exceptions import ForbiddenException, UnauthorizedException
from src.infrastructure.session.manager import session_manager
from src.schemas.base_schemas import PaginationParamsSchema
from src.schemas.session_schemas import UserSessionSchema
from src.usecases.session.get_user_session import GetUserSessionUseCase

oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token", auto_error=False)
TokenDep = Annotated[str, Depends(oauth2)]

SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def get_user_crud(session: SessionDep) -> UserCrud:
    return UserCrud(session=session)


UserCrudDep = Annotated[UserCrud, Depends(get_user_crud)]


async def get_dataset_crud(session: SessionDep) -> DatasetCrud:
    return DatasetCrud(session=session)


DatasetCrudDep = Annotated[DatasetCrud, Depends(get_dataset_crud)]


def get_session_manager() -> SessionManager:
    return session_manager


SessionManagerDep = Annotated[SessionManager, Depends(get_session_manager)]


async def get_user_session(
    request: Request,
    session_manager: SessionManagerDep,
) -> UserSessionSchema:
    """Get user session data."""
    get_user_session_use_case = GetUserSessionUseCase(session_manager=session_manager)
    return await get_user_session_use_case(request=request)


UserSessionDep = Annotated[UserSessionSchema, Depends(get_user_session)]


async def get_optional_user_session(
    request: Request,
    session_manager: SessionManagerDep,
) -> UserSessionSchema | None:
    """Get user session if exists, None otherwise (for optional auth)."""
    try:
        get_user_session_use_case = GetUserSessionUseCase(
            session_manager=session_manager
        )
        return await get_user_session_use_case(request=request)
    except UnauthorizedException:
        return None


OptionalUserSessionDep = Annotated[
    UserSessionSchema | None, Depends(get_optional_user_session)
]


async def get_admin_session(user_session: UserSessionDep) -> UserSessionSchema:
    """Require admin user from session."""
    if not user_session.is_admin:
        raise ForbiddenException("Admin access required")
    return user_session


AdminSessionDep = Annotated[UserSessionSchema, Depends(get_admin_session)]


PaginationParamsDep = Annotated[PaginationParamsSchema, Depends(PaginationParamsSchema)]
