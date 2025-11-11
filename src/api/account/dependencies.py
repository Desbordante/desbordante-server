from typing import Annotated

from fastapi import Depends

from src.api.dependencies import (
    DatasetCrudDep,
    GetUserByIdUseCaseDep,
    UserSessionDep,
)
from src.models.user_models import UserModel
from src.usecases.account.get_stats import GetStatsUseCase


async def get_get_stats_use_case(
    dataset_crud: DatasetCrudDep,
    user_session: UserSessionDep,
) -> GetStatsUseCase:
    return GetStatsUseCase(dataset_crud=dataset_crud, user_session=user_session)


GetStatsUseCaseDep = Annotated[GetStatsUseCase, Depends(get_get_stats_use_case)]


async def get_current_user(
    user_session: UserSessionDep,
    get_user_by_id: GetUserByIdUseCaseDep,
) -> UserModel:
    """Get authenticated user model from session."""
    return await get_user_by_id(id=user_session.id)


CurrentUserDep = Annotated[UserModel, Depends(get_current_user)]
