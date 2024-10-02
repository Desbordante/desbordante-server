from internal.infrastructure.data_storage.context import get_context_maker_without_pool
from internal.repository.flat import FileRepository
from internal.repository.relational.file import DatasetRepository
from internal.repository.relational.task import TaskRepository
from internal.uow import UnitOfWork
from internal.usecase.task.profile_task import ProfileTask
from internal.usecase.task.update_task_info import UpdateTaskInfo


def get_file_repo() -> FileRepository:
    return FileRepository()


def get_dataset_repo() -> DatasetRepository:
    return DatasetRepository()


def get_task_repo() -> TaskRepository:
    return TaskRepository()


def get_unit_of_work_without_pool() -> UnitOfWork:
    context_maker_without_pool = get_context_maker_without_pool()
    return UnitOfWork(context_maker_without_pool)


def get_update_task_info_use_case():
    unit_of_work = get_unit_of_work_without_pool()
    task_repo = get_task_repo()

    return UpdateTaskInfo(
        unit_of_work=unit_of_work,
        task_repo=task_repo,  # type: ignore
    )


def get_profile_task_use_case():
    unit_of_work = get_unit_of_work_without_pool()
    file_repo = get_file_repo()
    dataset_repo = get_dataset_repo()

    return ProfileTask(
        unit_of_work=unit_of_work,
        file_repo=file_repo,  # type: ignore
        dataset_repo=dataset_repo,  # type: ignore
    )
