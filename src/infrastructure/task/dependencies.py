from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.dataset_crud import DatasetCrud
from src.crud.task_crud import TaskCrud
from src.infrastructure.storage.client import get_storage


async def get_dataset_crud(session: AsyncSession) -> DatasetCrud:
    return DatasetCrud(session=session)


async def get_task_crud(session: AsyncSession) -> TaskCrud:
    return TaskCrud(session=session)


async def get_update_task_info_use_case(session: AsyncSession):
    task_crud = await get_task_crud(session=session)

    return UpdateTaskInfoUseCase(
        task_crud=task_crud,
    )


async def get_profile_task_use_case(session: AsyncSession):
    dataset_crud = await get_dataset_crud(session=session)
    storage = get_storage()

    return ProfileTaskUseCase(
        dataset_crud=dataset_crud,
        storage=storage,
    )
