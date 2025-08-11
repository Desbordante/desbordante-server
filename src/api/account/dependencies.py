from typing import Annotated

from fastapi import Depends

from src.api.dependencies import (
    AuthorizedUserDep,
    DatasetCrudDep,
    UserCrudDep,
    VerificationDep,
)
from src.models.user_models import UserModel
from src.usecases.account.change_password import ChangePasswordUseCase
from src.usecases.account.confirm_email import ConfirmEmailUseCase
from src.usecases.account.get_stats import GetStatsUseCase
from src.usecases.account.update_info import UpdateInfoUseCase

NotVerifiedUserDep = Annotated[
    UserModel, Depends(VerificationDep(should_be_verified=False))
]


async def get_confirm_email_use_case(
    user_crud: UserCrudDep,
) -> ConfirmEmailUseCase:
    return ConfirmEmailUseCase(user_crud=user_crud)


ConfirmEmailUseCaseDep = Annotated[
    ConfirmEmailUseCase, Depends(get_confirm_email_use_case)
]


async def get_change_password_use_case(
    user_crud: UserCrudDep,
    user: AuthorizedUserDep,
) -> ChangePasswordUseCase:
    return ChangePasswordUseCase(user_crud=user_crud, user=user)


ChangePasswordUseCaseDep = Annotated[
    ChangePasswordUseCase, Depends(get_change_password_use_case)
]


async def get_update_info_use_case(
    user_crud: UserCrudDep,
    user: AuthorizedUserDep,
) -> UpdateInfoUseCase:
    return UpdateInfoUseCase(user_crud=user_crud, user=user)


UpdateInfoUseCaseDep = Annotated[UpdateInfoUseCase, Depends(get_update_info_use_case)]


async def get_get_stats_use_case(
    dataset_crud: DatasetCrudDep,
    user: AuthorizedUserDep,
) -> GetStatsUseCase:
    return GetStatsUseCase(dataset_crud=dataset_crud, user=user)


GetStatsUseCaseDep = Annotated[GetStatsUseCase, Depends(get_get_stats_use_case)]
