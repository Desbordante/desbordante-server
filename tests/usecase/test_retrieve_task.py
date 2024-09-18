from uuid import uuid4

import pytest
from pytest_mock import MockerFixture

from internal.domain.task.value_objects import PrimitiveName, TaskStatus, FdTaskResult
from internal.domain.task.value_objects.fd import FdAlgoName, FdAlgoResult, FdTaskConfig
from internal.dto.repository.task import (
    TaskResponseSchema,
    TaskFindSchema,
)
from internal.uow import UnitOfWork, DataStorageContext
from internal.usecase.task.exception import TaskNotFoundException
from internal.usecase.task.retrieve_task import (
    RetrieveTask,
    TaskRepo,
    RetrieveTaskUseCaseResult,
)


@pytest.fixture
def unit_of_work_mock(mocker: MockerFixture) -> UnitOfWork:
    mock = mocker.MagicMock()
    mock.__enter__.return_value = mocker.Mock(
        return_value=mocker.Mock(), spec=DataStorageContext
    )
    mock.__exit__.return_value = mocker.Mock(return_value=None)
    return mock


@pytest.fixture
def task_repo_mock(mocker: MockerFixture) -> TaskRepo:
    mock = mocker.Mock(spec=TaskRepo)
    return mock


@pytest.fixture
def retrieve_task_use_case(
    unit_of_work_mock: UnitOfWork, task_repo_mock: TaskRepo
) -> RetrieveTask:
    return RetrieveTask(unit_of_work=unit_of_work_mock, task_repo=task_repo_mock)


def test_retrieve_task_use_case_success(
    unit_of_work_mock: UnitOfWork,
    task_repo_mock: TaskRepo,
    retrieve_task_use_case: RetrieveTask,
):
    # Prepare data
    task_id = uuid4()
    dataset_id = uuid4()

    task_config = FdTaskConfig(
        primitive_name=PrimitiveName.fd, config={"algo_name": FdAlgoName.Aid}
    )
    task_result = FdTaskResult(
        primitive_name=PrimitiveName.fd, result=FdAlgoResult(fds=[])
    )

    task_repo_mock.find.return_value = TaskResponseSchema(
        id=task_id,
        status=TaskStatus.COMPLETED,
        config=task_config,
        result=task_result,
        dataset_id=dataset_id,
        created_at=None,
        updated_at=None,
    )

    # Act
    result = retrieve_task_use_case(task_id=task_id)

    # Check result
    assert result == RetrieveTaskUseCaseResult(
        task_id=task_id,
        status=TaskStatus.COMPLETED,
        config=task_config,
        result=task_result,
        dataset_id=dataset_id,
        raised_exception_name=None,
        failure_reason=None,
        traceback=None,
        created_at=None,
        updated_at=None,
    )

    # Check that repositories' find method work correctly
    task_repo_mock.find.assert_called_once_with(
        TaskFindSchema(id=task_id), unit_of_work_mock.__enter__.return_value
    )

    # Check that UnitOfWork was entered and exited correctly
    unit_of_work_mock.__enter__.assert_called_once()
    unit_of_work_mock.__exit__.assert_called_once()


def test_retrieve_task_use_case_not_found(
    unit_of_work_mock: UnitOfWork,
    retrieve_task_use_case: RetrieveTask,
    task_repo_mock: TaskRepo,
):
    task_id = uuid4()

    task_repo_mock.find.return_value = None

    with pytest.raises(TaskNotFoundException):
        retrieve_task_use_case(task_id=task_id)

    # Check that repositories' find method work correctly
    task_repo_mock.find.assert_called_once_with(
        TaskFindSchema(id=task_id), unit_of_work_mock.__enter__.return_value
    )

    # Check that UnitOfWork was entered and exited correctly
    unit_of_work_mock.__enter__.assert_called_once()
    unit_of_work_mock.__exit__.assert_called_once()
