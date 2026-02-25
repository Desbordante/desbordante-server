from typing import Annotated

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.dataset_crud import DatasetCrud
from src.crud.auth_account_crud import AuthAccountCrud
from src.crud.task_crud import TaskCrud
from src.crud.user_crud import UserCrud
from src.db.session import get_session
from src.domain.session.config import settings
from src.exceptions import ForbiddenException, UnauthorizedException
from src.infrastructure.session.manager import SessionManager
from src.schemas.base_schemas import PaginationParamsSchema
from src.schemas.session_schemas import SessionSchema
from src.usecases.session.get_user_session import GetUserSessionUseCase

oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token", auto_error=False)
TokenDep = Annotated[str, Depends(oauth2)]

SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def get_redis(request: Request) -> Redis:
    return request.app.state.redis


RedisDep = Annotated[Redis, Depends(get_redis)]


async def get_user_crud(session: SessionDep) -> UserCrud:
    return UserCrud(session=session)


UserCrudDep = Annotated[UserCrud, Depends(get_user_crud)]


async def get_dataset_crud(session: SessionDep) -> DatasetCrud:
    return DatasetCrud(session=session)


DatasetCrudDep = Annotated[DatasetCrud, Depends(get_dataset_crud)]


async def get_task_crud(session: SessionDep) -> TaskCrud:
    return TaskCrud(session=session)


TaskCrudDep = Annotated[TaskCrud, Depends(get_task_crud)]


async def get_auth_account_crud(session: SessionDep) -> AuthAccountCrud:
    return AuthAccountCrud(session=session)


AuthAccountCrudDep = Annotated[AuthAccountCrud, Depends(get_auth_account_crud)]


def get_session_manager(redis: RedisDep) -> SessionManager:
    return SessionManager(redis=redis)


SessionManagerDep = Annotated[SessionManager, Depends(get_session_manager)]


async def get_get_user_session_use_case(
    session_manager: SessionManagerDep,
) -> GetUserSessionUseCase:
    return GetUserSessionUseCase(session_manager=session_manager)


GetUserSessionUseCaseDep = Annotated[
    GetUserSessionUseCase, Depends(get_get_user_session_use_case)
]


def get_session_id(request: Request) -> str | None:
    return request.cookies.get(settings.SESSION_COOKIE_NAME)


SessionIdDep = Annotated[str | None, Depends(get_session_id)]


async def get_user_session(
    get_user_session_use_case: GetUserSessionUseCaseDep,
    session_id: SessionIdDep,
) -> SessionSchema:
    """Get user session data."""
    return await get_user_session_use_case(session_id=session_id)


UserSessionDep = Annotated[SessionSchema, Depends(get_user_session)]


async def get_optional_user_session(
    get_user_session_use_case: GetUserSessionUseCaseDep,
    session_id: SessionIdDep,
) -> SessionSchema | None:
    """Get user session if exists, None otherwise (for optional auth)."""
    try:
        return await get_user_session_use_case(session_id=session_id)
    except UnauthorizedException:
        return None


OptionalUserSessionDep = Annotated[
    SessionSchema | None, Depends(get_optional_user_session)
]


async def get_admin_session(user_session: UserSessionDep) -> SessionSchema:
    """Require admin user from session."""
    if not user_session.is_admin:
        raise ForbiddenException("Admin access required")
    return user_session


AdminSessionDep = Annotated[SessionSchema, Depends(get_admin_session)]


PaginationParamsDep = Annotated[PaginationParamsSchema, Depends(PaginationParamsSchema)]
