from typing import Annotated

from fastapi import Depends

from src.api.dependencies import (
    AdminSessionDep,
    DatasetCrudDep,
    SessionManagerDep,
    UserCrudDep,
    UserSessionDep,
)
from src.models.user_models import UserModel
from src.usecases.user.ban_user import BanUserUseCase
from src.usecases.user.get_stats import GetStatsUseCase
from src.usecases.user.get_user_by_id import GetUserByIdUseCase
from src.usecases.user.get_user_stats import GetUserStatsUseCase
from src.usecases.user.unban_user import UnbanUserUseCase


async def get_get_my_stats_use_case(
    dataset_crud: DatasetCrudDep,
    user_session: UserSessionDep,
) -> GetStatsUseCase:
    return GetStatsUseCase(dataset_crud=dataset_crud, user=user_session)


GetMyStatsUseCaseDep = Annotated[GetStatsUseCase, Depends(get_get_my_stats_use_case)]


async def get_get_user_stats_use_case(
    dataset_crud: DatasetCrudDep,
    admin_session: AdminSessionDep,
) -> GetUserStatsUseCase:
    return GetUserStatsUseCase(dataset_crud=dataset_crud)


GetUserStatsUseCaseDep = Annotated[
    GetUserStatsUseCase, Depends(get_get_user_stats_use_case)
]


async def get_get_user_by_id_use_case(user_crud: UserCrudDep) -> GetUserByIdUseCase:
    return GetUserByIdUseCase(user_crud=user_crud)


GetUserByIdUseCaseDep = Annotated[
    GetUserByIdUseCase, Depends(get_get_user_by_id_use_case)
]


async def get_current_user(
    user_session: UserSessionDep,
    get_user_by_id: GetUserByIdUseCaseDep,
) -> UserModel:
    return await get_user_by_id(id=user_session.id)


CurrentUserDep = Annotated[UserModel, Depends(get_current_user)]


async def get_ban_user_use_case(
    user_crud: UserCrudDep,
    session_manager: SessionManagerDep,
    admin_session: AdminSessionDep,
) -> BanUserUseCase:
    return BanUserUseCase(user_crud=user_crud, session_manager=session_manager)


BanUserUseCaseDep = Annotated[BanUserUseCase, Depends(get_ban_user_use_case)]


async def get_unban_user_use_case(
    user_crud: UserCrudDep,
    admin_session: AdminSessionDep,
) -> UnbanUserUseCase:
    return UnbanUserUseCase(user_crud=user_crud)


UnbanUserUseCaseDep = Annotated[UnbanUserUseCase, Depends(get_unban_user_use_case)]
