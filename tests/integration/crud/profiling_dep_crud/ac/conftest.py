"""Fixtures for AC profiling dep CRUD tests."""

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
from src.schemas.task_schemas.primitives.ac.algo_config import BHUNTConfig
from src.schemas.task_schemas.primitives.ac.algo_name import AcAlgoName
from src.schemas.task_schemas.primitives.ac.task_params import (
    AcTaskDatasetsConfig,
    AcTaskParams,
)
from src.schemas.task_schemas.types import PrimitiveName
from tests.integration.crud.profiling_dep_crud.ac.helpers import make_ac_result


def _make_ac_task_entity(
    *,
    datasets: list[DatasetModel],
    owner_id: int | None = None,
    is_public: bool = False,
) -> ProfilingTaskModel:
    params = AcTaskParams(
        primitive_name=PrimitiveName.AC,
        config=BHUNTConfig(algo_name=AcAlgoName.BHUNT),
        datasets=AcTaskDatasetsConfig(table=datasets[0].id),
    )
    return ProfilingTaskModel(
        params=params,
        datasets=datasets,
        owner_id=owner_id,
        is_public=is_public,
    )


@pytest_asyncio.fixture
async def ac_task(
    task_crud: TaskCrud,
    dataset: DatasetModel,
    user: UserModel,
) -> ProfilingTaskModel:
    entity = _make_ac_task_entity(
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
async def ac_profiling_dep_crud(session: AsyncSession) -> ProfilingDepCrud:
    return ProfilingDepCrud(session=session, primitive_name=PrimitiveName.AC)


@pytest_asyncio.fixture
async def many_ac_deps(
    session: AsyncSession,
    task_crud: TaskCrud,
    dataset: DatasetModel,
    user: UserModel,
) -> list[ProfilingDepModel]:
    entity = _make_ac_task_entity(datasets=[dataset], owner_id=user.id, is_public=False)
    task = await task_crud.create(entity=entity)
    await task_crud._session.execute(
        update(ProfilingTaskModel)
        .where(ProfilingTaskModel.id == task.id)
        .values(status=TaskStatus.SUCCESS)
    )
    await task_crud._session.commit()

    # AC results: lhs_column, rhs_column, ranges, exceptions
    deps = [
        ProfilingDepModel(
            task_id=task.id,
            result=make_ac_result(
                lhs_column={"name": "id", "index": 0},
                rhs_column={"name": "age", "index": 3},
                ranges=[[1.0, 10.0], [11.0, 20.0]],
                exceptions=[{"row_index": 0, "lhs_value": 1.0, "rhs_value": 25.0}],
            ),
        ),
        ProfilingDepModel(
            task_id=task.id,
            result=make_ac_result(
                lhs_column={"name": "id", "index": 0},
                rhs_column={"name": "score", "index": 4},
                ranges=[[0.0, 100.0]],
                exceptions=[],
            ),
        ),
        ProfilingDepModel(
            task_id=task.id,
            result=make_ac_result(
                lhs_column={"name": "alpha", "index": 0},
                rhs_column={"name": "beta", "index": 1},
                ranges=[[1.0, 5.0], [6.0, 10.0], [11.0, 15.0]],
                exceptions=[{"row_index": 2, "lhs_value": 3.0, "rhs_value": 99.0}],
            ),
        ),
        ProfilingDepModel(
            task_id=task.id,
            result=make_ac_result(
                lhs_column={"name": "gamma", "index": 2},
                rhs_column={"name": "delta", "index": 3},
                ranges=[[0.0, 1.0]],
                exceptions=[],
            ),
        ),
        ProfilingDepModel(
            task_id=task.id,
            result=make_ac_result(
                lhs_column={"name": "name", "index": 1},
                rhs_column={"name": "email", "index": 2},
                ranges=[[10.0, 20.0]],
                exceptions=[
                    {"row_index": 1, "lhs_value": 11.0, "rhs_value": 22.0},
                    {"row_index": 2, "lhs_value": 12.0, "rhs_value": 23.0},
                ],
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
