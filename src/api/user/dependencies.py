from typing import Annotated

from fastapi import Depends

from src.api.dependencies import (
    AuthAccountCrudDep,
    DatasetCrudDep,
    DatasetPolicyDep,
    SessionManagerDep,
    StorageDep,
    TaskCrudDep,
    UserCrudDep,
    UserPolicyDep,
)
from src.infrastructure.dataset.preprocess_dataset_worker import PreprocessDatasetWorker
from src.infrastructure.storage.config import settings as storage_settings
from src.usecases.dataset.check_content_type import CheckContentTypeUseCase
from src.usecases.dataset.get_user_datasets import GetUserDatasetsUseCase
from src.usecases.dataset.upload_dataset import UploadDatasetUseCase
from src.usecases.task.get_user_tasks import GetUserTasksUseCase
from src.usecases.user.get_linked_accounts import GetLinkedAccountsUseCase
from src.usecases.user.get_user_by_id import GetUserByIdUseCase
from src.usecases.user.get_user_stats import GetUserStatsUseCase
from src.usecases.user.update_user_status import UpdateUserStatusUseCase


async def get_get_user_stats_use_case(
    dataset_crud: DatasetCrudDep,
) -> GetUserStatsUseCase:
    return GetUserStatsUseCase(dataset_crud=dataset_crud, settings=storage_settings)


GetUserStatsUseCaseDep = Annotated[
    GetUserStatsUseCase, Depends(get_get_user_stats_use_case)
]


async def get_get_user_by_id_use_case(user_crud: UserCrudDep) -> GetUserByIdUseCase:
    return GetUserByIdUseCase(user_crud=user_crud)


GetUserByIdUseCaseDep = Annotated[
    GetUserByIdUseCase, Depends(get_get_user_by_id_use_case)
]


async def get_update_user_status_use_case(
    user_crud: UserCrudDep,
    session_manager: SessionManagerDep,
    user_policy: UserPolicyDep,
) -> UpdateUserStatusUseCase:
    return UpdateUserStatusUseCase(
        user_crud=user_crud, session_manager=session_manager, user_policy=user_policy
    )


UpdateUserStatusUseCaseDep = Annotated[
    UpdateUserStatusUseCase, Depends(get_update_user_status_use_case)
]


async def get_get_linked_accounts_use_case(
    auth_account_crud: AuthAccountCrudDep,
) -> GetLinkedAccountsUseCase:
    return GetLinkedAccountsUseCase(
        auth_account_crud=auth_account_crud,
    )


GetLinkedAccountsUseCaseDep = Annotated[
    GetLinkedAccountsUseCase, Depends(get_get_linked_accounts_use_case)
]


async def get_preprocess_dataset_task_worker() -> PreprocessDatasetWorker:
    return PreprocessDatasetWorker()


PreprocessDatasetTaskWorkerDep = Annotated[
    PreprocessDatasetWorker, Depends(get_preprocess_dataset_task_worker)
]


async def get_upload_my_dataset_use_case(
    dataset_crud: DatasetCrudDep,
    storage: StorageDep,
    dataset_policy: DatasetPolicyDep,
    preprocess_dataset_task_worker: PreprocessDatasetTaskWorkerDep,
) -> UploadDatasetUseCase:
    return UploadDatasetUseCase(
        dataset_crud=dataset_crud,
        storage=storage,
        dataset_policy=dataset_policy,
        settings=storage_settings,
        preprocess_dataset_task=preprocess_dataset_task_worker,
    )


UploadMyDatasetUseCaseDep = Annotated[
    UploadDatasetUseCase, Depends(get_upload_my_dataset_use_case)
]


async def get_get_user_datasets_use_case(
    dataset_crud: DatasetCrudDep,
) -> GetUserDatasetsUseCase:
    return GetUserDatasetsUseCase(dataset_crud=dataset_crud)


GetUserDatasetsUseCaseDep = Annotated[
    GetUserDatasetsUseCase, Depends(get_get_user_datasets_use_case)
]


async def get_check_content_type_use_case() -> CheckContentTypeUseCase:
    return CheckContentTypeUseCase()


CheckContentTypeUseCaseDep = Annotated[
    CheckContentTypeUseCase, Depends(get_check_content_type_use_case)
]


async def get_get_user_tasks_use_case(
    task_crud: TaskCrudDep,
) -> GetUserTasksUseCase:
    return GetUserTasksUseCase(task_crud=task_crud)


GetUserTasksUseCaseDep = Annotated[
    GetUserTasksUseCase, Depends(get_get_user_tasks_use_case)
]
