"""Fixtures for DD profiling dep CRUD tests."""

from datetime import datetime, timedelta, timezone

import pytest_asyncio
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.profiling_dep_crud.profiling_dep_crud import ProfilingDepCrud
from src.crud.task_crud import TaskCrud
from src.models.dataset_models import DatasetModel
from src.models.task_models import ProfilingDepModel, ProfilingTaskModel
from src.models.user_models import UserModel
from src.schemas.base_schemas import TaskStatus
from src.schemas.task_schemas.primitives.dd.algo_config import SplitConfig
from src.schemas.task_schemas.primitives.dd.algo_name import DdAlgoName
from src.schemas.task_schemas.primitives.dd.task_params import (
    DdTaskDatasetsConfig,
    DdTaskParams,
)
from src.schemas.task_schemas.types import PrimitiveName
from tests.integration.crud.profiling_dep_crud.dd.helpers import make_dd_result


def _make_dd_task_entity(
    *,
    datasets: list[DatasetModel],
    owner_id: int | None = None,
    is_public: bool = False,
) -> ProfilingTaskModel:
    params = DdTaskParams(
        primitive_name=PrimitiveName.DD,
        config=SplitConfig(algo_name=DdAlgoName.SPLIT),
        datasets=DdTaskDatasetsConfig(
            table=datasets[0].id,
            dif_table=datasets[0].id,
        ),
    )
    return ProfilingTaskModel(
        params=params,
        datasets=datasets,
        owner_id=owner_id,
        is_public=is_public,
    )


@pytest_asyncio.fixture
async def dd_task(
    task_crud: TaskCrud,
    dataset: DatasetModel,
    user: UserModel,
) -> ProfilingTaskModel:
    entity = _make_dd_task_entity(
        datasets=[dataset],
        owner_id=user.id,
        is_public=False,
    )
    task = await task_crud.create(entity=entity)
    await task_crud._session.execute(
        update(ProfilingTaskModel)
        .where(ProfilingTaskModel.id == task.id)
        .values(status=TaskStatus.SUCCESS)
    )
    await task_crud._session.commit()
    task.status = TaskStatus.SUCCESS
    return task


@pytest_asyncio.fixture
async def dd_profiling_dep_crud(session: AsyncSession) -> ProfilingDepCrud:
    return ProfilingDepCrud(session=session, primitive_name=PrimitiveName.DD)


@pytest_asyncio.fixture
async def many_dd_deps(
    session: AsyncSession,
    task_crud: TaskCrud,
    dataset: DatasetModel,
    user: UserModel,
) -> list[ProfilingDepModel]:
    entity = _make_dd_task_entity(datasets=[dataset], owner_id=user.id, is_public=False)
    task = await task_crud.create(entity=entity)
    await task_crud._session.execute(
        update(ProfilingTaskModel)
        .where(ProfilingTaskModel.id == task.id)
        .values(status=TaskStatus.SUCCESS)
    )
    await task_crud._session.commit()

    # DD results: lhs_items: [{name, index, distance_interval}], rhs_item: {name, index, distance_interval}
    deps = [
        ProfilingDepModel(
            task_id=task.id,
            result=make_dd_result(
                lhs_items=[
                    {"name": "id", "index": 0, "distance_interval": [0, 1]},
                ],
                rhs_item={"name": "age", "index": 3, "distance_interval": [0, 2]},
            ),
        ),
        ProfilingDepModel(
            task_id=task.id,
            result=make_dd_result(
                lhs_items=[
                    {"name": "id", "index": 0, "distance_interval": [0, 1]},
                ],
                rhs_item={"name": "score", "index": 4, "distance_interval": [0, 1]},
            ),
        ),
        ProfilingDepModel(
            task_id=task.id,
            result=make_dd_result(
                lhs_items=[
                    {"name": "alpha", "index": 0, "distance_interval": [0, 2]},
                    {"name": "beta", "index": 1, "distance_interval": [1, 3]},
                ],
                rhs_item={"name": "gamma", "index": 2, "distance_interval": [0, 1]},
            ),
        ),
        ProfilingDepModel(
            task_id=task.id,
            result=make_dd_result(
                lhs_items=[
                    {"name": "gamma", "index": 2, "distance_interval": [0, 1]},
                ],
                rhs_item={"name": "delta", "index": 3, "distance_interval": [0, 2]},
            ),
        ),
        ProfilingDepModel(
            task_id=task.id,
            result=make_dd_result(
                lhs_items=[
                    {"name": "name", "index": 1, "distance_interval": [0, 1]},
                ],
                rhs_item={"name": "email", "index": 2, "distance_interval": [0, 1]},
            ),
        ),
    ]
    session.add_all(deps)
    await session.commit()

    base = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    for i, dep in enumerate(deps):
        await session.execute(
            update(ProfilingDepModel)
            .where(ProfilingDepModel.id == dep.id)
            .values(
                created_at=base + timedelta(seconds=i),
                updated_at=base + timedelta(seconds=i),
            )
        )
    await session.commit()

    for dep in deps:
        await session.refresh(dep)
    return deps
