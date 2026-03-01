from uuid import uuid4

import pytest
from pytest_mock import MockerFixture
from unittest.mock import AsyncMock

from src.domain.task.value_objects import TaskStatus
from src.exceptions import ResourceNotFoundException
from src.models.task_models import TaskModel
from src.usecases.task.update_task_info import UpdateTaskInfoUseCase


@pytest.fixture
def task_crud_mock(mocker: MockerFixture):
    mock = mocker.Mock()
    mock.get_by = AsyncMock()
    mock.update = AsyncMock()
    return mock


@pytest.fixture
def update_task_info_use_case(task_crud_mock) -> UpdateTaskInfoUseCase:
    return UpdateTaskInfoUseCase(task_crud=task_crud_mock)


pytestmark = pytest.mark.asyncio


async def test_update_task_info_success(
    mocker: MockerFixture,
    update_task_info_use_case: UpdateTaskInfoUseCase,
    task_crud_mock,
) -> None:
    task_id = uuid4()
    task_status = TaskStatus.PROCESSING

    task = mocker.Mock(spec=TaskModel)
    task.id = task_id
    task_crud_mock.get_by.return_value = task
    task_crud_mock.update.return_value = task

    result = await update_task_info_use_case(
        task_id=task_id,
        status=task_status,
    )

    task_crud_mock.get_by.assert_awaited_once_with(id=task_id)
    task_crud_mock.update.assert_awaited_once_with(entity=task, status=task_status)
    assert result == task


async def test_update_task_info_task_not_found(
    update_task_info_use_case: UpdateTaskInfoUseCase,
    task_crud_mock,
) -> None:
    task_id = uuid4()

    task_crud_mock.get_by.side_effect = ResourceNotFoundException("Task not found")

    with pytest.raises(ResourceNotFoundException):
        await update_task_info_use_case(task_id=task_id)

    task_crud_mock.get_by.assert_awaited_once_with(id=task_id)
    task_crud_mock.update.assert_not_called()
