import pytest
from uuid import uuid4
from pytest_mock import MockerFixture
from internal.domain.task.value_objects import TaskStatus
from internal.dto.repository.task import TaskUpdateSchema, TaskFindSchema
from internal.dto.repository.task.task import TaskNotFoundException
from internal.uow import DataStorageContext
from internal.usecase.task.update_task_info import TaskRepo, UpdateTaskInfo
from internal.usecase.task.exception import (
    TaskNotFoundException as TaskNotFoundUseCaseException,
)


@pytest.fixture
def unit_of_work_mock(mocker: MockerFixture):
    mock = mocker.MagicMock()
    mock.__enter__.return_value = mocker.Mock(spec=DataStorageContext)
    mock.__exit__.return_value = mocker.Mock()

    def exit_side_effect(exc_type, exc_value, traceback) -> bool:
        if exc_type:
            raise exc_value
        return False

    mock.__exit__.side_effect = exit_side_effect
    return mock


@pytest.fixture
def task_repo_mock(mocker: MockerFixture):
    mock = mocker.Mock(spec=TaskRepo)
    mock.update = mocker.Mock()
    return mock


@pytest.fixture
def update_task_info_use_case(unit_of_work_mock, task_repo_mock) -> UpdateTaskInfo:
    return UpdateTaskInfo(
        unit_of_work=unit_of_work_mock,
        task_repo=task_repo_mock,
    )


def test_update_task_info_success(
    update_task_info_use_case,
    unit_of_work_mock,
    task_repo_mock,
) -> None:
    # Prepare data
    task_id = uuid4()
    task_status = TaskStatus.RUNNING

    find_schema = TaskFindSchema(id=task_id)
    update_schema = TaskUpdateSchema(status=task_status)  # type: ignore

    # Act
    update_task_info_use_case(
        task_id=task_id, task_status=task_status, fields_to_update_if_none=None
    )

    # Check that all repository methods were called correctly
    task_repo_mock.update.assert_called_once_with(
        find_schema, update_schema, None, unit_of_work_mock.__enter__.return_value
    )

    # Check that UnitOfWork was entered and exited correctly
    unit_of_work_mock.__enter__.assert_called_once()
    unit_of_work_mock.__exit__.assert_called_once()


@pytest.mark.parametrize(
    "repo_exception, use_case_exception",
    [
        (TaskNotFoundException, TaskNotFoundUseCaseException),
    ],
)
def test_update_task_info_unsuccess(
    update_task_info_use_case,
    unit_of_work_mock,
    task_repo_mock,
    repo_exception,
    use_case_exception,
) -> None:
    # Prepare data
    task_id = uuid4()

    # Mocks
    task_repo_mock.update.side_effect = repo_exception

    # Act and except error
    with pytest.raises(use_case_exception):
        update_task_info_use_case(task_id=task_id)

    task_repo_mock.update.assert_called_once_with(
        TaskFindSchema(id=task_id),
        TaskUpdateSchema(),  # type: ignore
        None,
        unit_of_work_mock.__enter__.return_value,
    )
