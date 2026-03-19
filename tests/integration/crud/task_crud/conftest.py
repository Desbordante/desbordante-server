"""Fixtures for task CRUD tests."""

from datetime import datetime, timedelta, timezone

import pytest_asyncio
from sqlalchemy import update

from src.crud.task_crud import TaskCrud
from src.models.dataset_models import DatasetModel
from src.models.task_models import ProfilingTaskModel
from src.models.user_models import UserModel
from src.schemas.base_schemas import TaskStatus
from tests.integration.crud.task_crud.helpers import make_task_entity


@pytest_asyncio.fixture
async def task(
    task_crud: TaskCrud,
    dataset: DatasetModel,
    user: UserModel,
) -> ProfilingTaskModel:
    entity = make_task_entity(
        datasets=[dataset],
        owner_id=user.id,
        is_public=False,
    )
    return await task_crud.create(entity=entity)


@pytest_asyncio.fixture
async def many_tasks(
    task_crud: TaskCrud,
    many_datasets: list[DatasetModel],
    user: UserModel,
    second_user: UserModel,
) -> list[ProfilingTaskModel]:
    alpha, beta, gamma, delta, epsilon, zeta = many_datasets
    entities = [
        make_task_entity(datasets=[alpha], owner_id=user.id, is_public=False),
        make_task_entity(datasets=[beta], owner_id=user.id, is_public=True),
        make_task_entity(datasets=[gamma], owner_id=user.id, is_public=False),
        make_task_entity(datasets=[delta], owner_id=user.id, is_public=True),
        make_task_entity(datasets=[epsilon], owner_id=user.id, is_public=False),
        make_task_entity(datasets=[zeta], owner_id=second_user.id, is_public=False),
    ]
    created = [await task_crud.create(entity=e) for e in entities]
    base = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    for i, task_model in enumerate(created):
        await task_crud._session.execute(
            update(ProfilingTaskModel)
            .where(ProfilingTaskModel.id == task_model.id)
            .values(
                created_at=base + timedelta(seconds=i),
                updated_at=base + timedelta(seconds=i),
                status=TaskStatus.SUCCESS if i in (2, 3) else TaskStatus.PENDING,
            )
        )
    await task_crud._session.commit()
    return created
