from uuid import uuid4

import pytest

from src.crud.task_crud import TaskCrud
from src.exceptions import ResourceNotFoundException
from src.models.task_models import ProfilingTaskModel
from src.models.user_models import UserModel
from tests.integration.crud.task_crud.helpers import make_task_entity

pytestmark = pytest.mark.asyncio


async def test_create(
    task_crud: TaskCrud,
    user: UserModel,
    dataset,
) -> None:
    entity = make_task_entity(
        datasets=[dataset],
        owner_id=user.id,
        is_public=True,
    )

    created = await task_crud.create(entity=entity)

    assert created.id is not None
    assert created.owner_id == user.id
    assert created.is_public is True
    assert len(created.datasets) == 1
    assert created.datasets[0].id == dataset.id


@pytest.mark.parametrize(
    "filter_keys",
    [
        ["id"],
        ["id", "owner_id"],
    ],
)
async def test_get_by(
    task_crud: TaskCrud,
    task: ProfilingTaskModel,
    filter_keys: list[str],
) -> None:
    kwargs = {key: getattr(task, key) for key in filter_keys}
    found = await task_crud.get_by(**kwargs)

    assert found.id == task.id
    assert found.owner_id == task.owner_id


async def test_get_by_raises_when_not_found(
    task_crud: TaskCrud,
) -> None:
    with pytest.raises(ResourceNotFoundException):
        await task_crud.get_by(id=uuid4())
