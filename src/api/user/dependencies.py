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
from src.usecases.dataset.get_my_datasets import GetMyDatasetsUseCase
from src.usecases.dataset.get_user_datasets import GetUserDatasetsUseCase
from src.usecases.dataset.upload_dataset import UploadDatasetUseCase
from src.usecases.user.get_stats import GetStatsUseCase
from src.usecases.user.get_user_by_id import GetUserByIdUseCase
from src.usecases.user.get_user_stats import GetUserStatsUseCase
from src.usecases.user.update_user_status import UpdateUserStatusUseCase


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


async def get_update_user_status_use_case(
    user_crud: UserCrudDep,
    session_manager: SessionManagerDep,
    admin_session: AdminSessionDep,
) -> UpdateUserStatusUseCase:
    return UpdateUserStatusUseCase(user_crud=user_crud, session_manager=session_manager)


UpdateUserStatusUseCaseDep = Annotated[
    UpdateUserStatusUseCase, Depends(get_update_user_status_use_case)
]


async def get_get_my_datasets_use_case(
    dataset_crud: DatasetCrudDep,
    user_session: UserSessionDep,
) -> GetMyDatasetsUseCase:
    return GetMyDatasetsUseCase(dataset_crud=dataset_crud, user=user_session)


GetMyDatasetsUseCaseDep = Annotated[
    GetMyDatasetsUseCase, Depends(get_get_my_datasets_use_case)
]


async def get_upload_my_dataset_use_case(
    dataset_crud: DatasetCrudDep,
    user_session: UserSessionDep,
) -> UploadDatasetUseCase:
    return UploadDatasetUseCase(dataset_crud=dataset_crud, user=user_session)


UploadMyDatasetUseCaseDep = Annotated[
    UploadDatasetUseCase, Depends(get_upload_my_dataset_use_case)
]


async def get_get_user_datasets_use_case(
    dataset_crud: DatasetCrudDep,
    admin_session: AdminSessionDep,
) -> GetUserDatasetsUseCase:
    return GetUserDatasetsUseCase(dataset_crud=dataset_crud)


GetUserDatasetsUseCaseDep = Annotated[
    GetUserDatasetsUseCase, Depends(get_get_user_datasets_use_case)
]
