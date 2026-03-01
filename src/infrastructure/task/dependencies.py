from src.crud.dataset_crud import DatasetCrud
from src.crud.task_crud import TaskCrud
from src.db.session import async_session_factory_without_pool
from src.infrastructure.storage.client import get_storage
from src.usecases.task.profile_task import ProfileTaskUseCase
from src.usecases.task.update_task_info import UpdateTaskInfoUseCase


async def get_dataset_crud() -> DatasetCrud:
    async with async_session_factory_without_pool() as session:
        return DatasetCrud(session=session)


async def get_task_crud() -> TaskCrud:
    async with async_session_factory_without_pool() as session:
        return TaskCrud(session=session)


async def get_update_task_info_use_case() -> UpdateTaskInfoUseCase:
    task_crud = await get_task_crud()

    return UpdateTaskInfoUseCase(
        task_crud=task_crud,
    )


async def get_profile_task_use_case() -> ProfileTaskUseCase:
    dataset_crud = await get_dataset_crud()
    storage = get_storage()

    return ProfileTaskUseCase(
        dataset_crud=dataset_crud,
        storage=storage,
    )
