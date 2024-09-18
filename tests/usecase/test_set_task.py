from datetime import datetime, timezone
from uuid import uuid4

import pytest
from pytest_mock import MockerFixture

from internal.domain.task.value_objects import PrimitiveName, TaskStatus, FdTaskConfig
from internal.domain.task.value_objects.fd import FdAlgoName
from internal.dto.repository.file import (
    DatasetResponseSchema,
    DatasetFindSchema,
)
from internal.dto.repository.task import (
    TaskResponseSchema,
    TaskCreateSchema,
)
from internal.dto.worker.task import ProfilingTaskCreateSchema
from internal.uow import UnitOfWork, DataStorageContext
from internal.usecase.file.exception import DatasetNotFoundException
from internal.usecase.task.set_task import (
    SetTask,
    DatasetRepo,
    TaskRepo,
    ProfilingTaskWorker,
)


@pytest.fixture
def unit_of_work_mock(mocker: MockerFixture) -> UnitOfWork:
    mock = mocker.MagicMock()
    mock.__enter__.return_value = mocker.Mock(
        return_value=mocker.Mock(), spec=DataStorageContext
    )
    mock.__exit__.return_value = None

    def exit_side_effect(exc_type, exc_value, traceback) -> bool:
        if exc_type:
            raise exc_value
        return False

    mock.__exit__.side_effect = exit_side_effect
    return mock


@pytest.fixture
def dataset_repo_mock(mocker: MockerFixture) -> DatasetRepo:
    mock = mocker.Mock(spec=DatasetRepo)
    return mock


@pytest.fixture
def task_repo_mock(mocker: MockerFixture) -> TaskRepo:
    mock = mocker.Mock(spec=TaskRepo)
    return mock


@pytest.fixture
def profiling_task_worker(mocker: MockerFixture) -> ProfilingTaskWorker:
    mock = mocker.Mock(spec=ProfilingTaskWorker)
    return mock


@pytest.fixture
def set_task_use_case(
    unit_of_work_mock: UnitOfWork,
    dataset_repo_mock: DatasetRepo,
    task_repo_mock: TaskRepo,
    profiling_task_worker: ProfilingTaskWorker,
):
    return SetTask(
        unit_of_work=unit_of_work_mock,
        dataset_repo=dataset_repo_mock,
        task_repo=task_repo_mock,
        profiling_task_worker=profiling_task_worker,
    )


def test_set_task_use_case_success(
    set_task_use_case: SetTask,
    unit_of_work_mock: UnitOfWork,
    dataset_repo_mock: DatasetRepo,
    task_repo_mock: TaskRepo,
    profiling_task_worker: ProfilingTaskWorker,
) -> None:
    # Prepare data
    dataset_id = uuid4()
    task_id = uuid4()
    task_config = FdTaskConfig(
        primitive_name=PrimitiveName.fd, config={"algo_name": FdAlgoName.Aid}
    )

    # Mocks repo methods
    dataset_repo_mock.find.return_value = DatasetResponseSchema(
        id=dataset_id,
        file_id=uuid4(),
        separator="",
        header=[],
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    task_repo_mock.create.return_value = TaskResponseSchema(
        id=task_id,
        status=TaskStatus.CREATED,
        config=task_config,
        dataset_id=dataset_id,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    # Act
    result = set_task_use_case(dataset_id=dataset_id, config=task_config)

    # Check that result is correct task identifier
    assert result == task_id

    # Check that all methods inside the use case were called correctly
    dataset_repo_mock.find.assert_called_once_with(
        DatasetFindSchema(
            id=dataset_id,
        ),
        unit_of_work_mock.__enter__.return_value,
    )

    task_repo_mock.create.assert_called_once_with(
        TaskCreateSchema(
            status=TaskStatus.CREATED,
            config=task_config.model_dump(exclude_unset=True),
            dataset_id=dataset_id,
        ),
        unit_of_work_mock.__enter__.return_value,
    )

    profiling_task_worker.set.assert_called_once_with(
        ProfilingTaskCreateSchema(
            task_id=task_id,
            dataset_id=dataset_id,
            config=task_config,
        )
    )

    # Check that UnitOfWork was entered and exited correctly
    unit_of_work_mock.__enter__.assert_called_once()
    unit_of_work_mock.__exit__.assert_called_once()


def test_set_task_use_case_dataset_not_found(
    set_task_use_case: SetTask,
    unit_of_work_mock: UnitOfWork,
    dataset_repo_mock: DatasetRepo,
    task_repo_mock: TaskRepo,
    profiling_task_worker: ProfilingTaskWorker,
):
    # Prepare data
    dataset_id = uuid4()
    task_config = FdTaskConfig(
        primitive_name=PrimitiveName.fd, config={"algo_name": FdAlgoName.Aid}
    )

    # Mocks repo methods
    dataset_repo_mock.find.return_value = None

    # Act and except error
    with pytest.raises(DatasetNotFoundException):
        set_task_use_case(
            dataset_id=dataset_id,
            config=task_config,
        )

    # Check that all methods inside the use case were called correctly
    dataset_repo_mock.find.assert_called_once_with(
        DatasetFindSchema(
            id=dataset_id,
        ),
        unit_of_work_mock.__enter__.return_value,
    )

    assert not task_repo_mock.create.called
    assert not profiling_task_worker.set.called

    # Check that UnitOfWork was entered and exited correctly
    unit_of_work_mock.__enter__.assert_called_once()
    unit_of_work_mock.__exit__.assert_called_once()
