"""Fixtures for NAR profiling dep CRUD tests."""

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
from src.schemas.task_schemas.primitives.nar.algo_config import DesConfig
from src.schemas.task_schemas.primitives.nar.algo_name import NarAlgoName
from src.schemas.task_schemas.primitives.nar.task_params import (
    NarTaskDatasetsConfig,
    NarTaskParams,
)
from src.schemas.task_schemas.types import PrimitiveName
from tests.integration.crud.profiling_dep_crud.nar.helpers import make_nar_result


def _make_nar_task_entity(
    *,
    datasets: list[DatasetModel],
    owner_id: int | None = None,
    is_public: bool = False,
) -> ProfilingTaskModel:
    params = NarTaskParams(
        primitive_name=PrimitiveName.NAR,
        config=DesConfig(algo_name=NarAlgoName.DES),
        datasets=NarTaskDatasetsConfig(table=datasets[0].id),
    )
    return ProfilingTaskModel(
        params=params,
        datasets=datasets,
        owner_id=owner_id,
        is_public=is_public,
    )


@pytest_asyncio.fixture
async def nar_task(
    task_crud: TaskCrud,
    dataset: DatasetModel,
    user: UserModel,
) -> ProfilingTaskModel:
    entity = _make_nar_task_entity(
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
async def nar_profiling_dep_crud(session: AsyncSession) -> ProfilingDepCrud:
    return ProfilingDepCrud(session=session, primitive_name=PrimitiveName.NAR)


@pytest_asyncio.fixture
async def many_nar_deps(
    session: AsyncSession,
    task_crud: TaskCrud,
    dataset: DatasetModel,
    user: UserModel,
) -> list[ProfilingDepModel]:
    entity = _make_nar_task_entity(
        datasets=[dataset], owner_id=user.id, is_public=False
    )
    task = await task_crud.create(entity=entity)
    await task_crud._session.execute(
        update(ProfilingTaskModel)
        .where(ProfilingTaskModel.id == task.id)
        .values(status=TaskStatus.SUCCESS)
    )
    await task_crud._session.commit()

    # NAR results: lhs_items, rhs_items (each: name, index, type, values/range), confidence, support, fitness
    deps = [
        ProfilingDepModel(
            task_id=task.id,
            result=make_nar_result(
                lhs_items=[
                    {"name": "alpha", "index": 0, "type": "string", "values": ["a"]},
                ],
                rhs_items=[
                    {"name": "beta", "index": 1, "type": "string", "values": ["b"]},
                ],
                confidence=0.9,
                support=0.5,
                fitness=0.85,
            ),
        ),
        ProfilingDepModel(
            task_id=task.id,
            result=make_nar_result(
                lhs_items=[
                    {"name": "gamma", "index": 0, "type": "string", "values": ["x"]},
                    {"name": "delta", "index": 1, "type": "integer", "range": [0, 10]},
                ],
                rhs_items=[
                    {
                        "name": "epsilon",
                        "index": 2,
                        "type": "float",
                        "range": [0.0, 1.0],
                    },
                ],
                confidence=0.7,
                support=0.3,
                fitness=0.6,
            ),
        ),
        ProfilingDepModel(
            task_id=task.id,
            result=make_nar_result(
                lhs_items=[
                    {"name": "foo", "index": 0, "type": "string", "values": ["bar"]},
                ],
                rhs_items=[
                    {"name": "baz", "index": 1, "type": "string", "values": ["qux"]},
                ],
                confidence=0.2,
                support=0.1,
                fitness=0.15,
            ),
        ),
        ProfilingDepModel(
            task_id=task.id,
            result=make_nar_result(
                lhs_items=[
                    {"name": "id", "index": 0, "type": "integer", "range": [1, 100]},
                ],
                rhs_items=[
                    {
                        "name": "score",
                        "index": 1,
                        "type": "float",
                        "range": [0.0, 10.0],
                    },
                ],
                confidence=0.95,
                support=0.8,
                fitness=0.9,
            ),
        ),
        ProfilingDepModel(
            task_id=task.id,
            result=make_nar_result(
                lhs_items=[
                    {
                        "name": "alpha",
                        "index": 0,
                        "type": "string",
                        "values": ["x", "y"],
                    },
                    {"name": "omega", "index": 1, "type": "string", "values": ["z"]},
                ],
                rhs_items=[
                    {"name": "result", "index": 2, "type": "string", "values": ["ok"]},
                ],
                confidence=0.5,
                support=0.4,
                fitness=0.45,
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
