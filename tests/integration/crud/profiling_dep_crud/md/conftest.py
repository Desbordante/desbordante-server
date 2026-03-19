"""Fixtures for MD profiling dep CRUD tests."""

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
from src.schemas.task_schemas.primitives.md.algo_config import (
    EqualityConfig,
    HyMDConfig,
)
from src.schemas.task_schemas.primitives.md.algo_name import MdAlgoName
from src.schemas.task_schemas.primitives.md.task_params import (
    MdTaskDatasetsConfig,
    MdTaskParams,
)
from src.schemas.task_schemas.primitives.md.types import ColumnMatchMetric
from src.schemas.task_schemas.types import PrimitiveName
from tests.integration.crud.profiling_dep_crud.md.helpers import make_md_result


def _make_md_task_entity(
    *,
    datasets: list[DatasetModel],
    owner_id: int | None = None,
    is_public: bool = False,
) -> ProfilingTaskModel:
    params = MdTaskParams(
        primitive_name=PrimitiveName.MD,
        config=HyMDConfig(
            algo_name=MdAlgoName.HY_MD,
            column_matches=[
                EqualityConfig(
                    left_column=0, right_column=1, metric=ColumnMatchMetric.EQUALITY
                ),
            ],
        ),
        datasets=MdTaskDatasetsConfig(
            left_table=datasets[0].id,
            right_table=datasets[0].id,
        ),
    )
    return ProfilingTaskModel(
        params=params,
        datasets=datasets,
        owner_id=owner_id,
        is_public=is_public,
    )


@pytest_asyncio.fixture
async def md_task(
    task_crud: TaskCrud,
    dataset: DatasetModel,
    user: UserModel,
) -> ProfilingTaskModel:
    entity = _make_md_task_entity(
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
async def md_profiling_dep_crud(session: AsyncSession) -> ProfilingDepCrud:
    return ProfilingDepCrud(session=session, primitive_name=PrimitiveName.MD)


@pytest_asyncio.fixture
async def many_md_deps(
    session: AsyncSession,
    task_crud: TaskCrud,
    dataset: DatasetModel,
    user: UserModel,
) -> list[ProfilingDepModel]:
    entity = _make_md_task_entity(datasets=[dataset], owner_id=user.id, is_public=False)
    task = await task_crud.create(entity=entity)
    await task_crud._session.execute(
        update(ProfilingTaskModel)
        .where(ProfilingTaskModel.id == task.id)
        .values(status=TaskStatus.SUCCESS)
    )
    await task_crud._session.commit()

    # MD results: lhs_items, rhs_item - each has metric, left_column, right_column, boundary, max_invalid_boundary
    deps = [
        ProfilingDepModel(
            task_id=task.id,
            result=make_md_result(
                lhs_items=[
                    {
                        "metric": "equality",
                        "left_column": {"name": "id", "index": 0},
                        "right_column": {"name": "id", "index": 0},
                        "boundary": 0.0,
                        "max_invalid_boundary": None,
                    },
                ],
                rhs_item={
                    "metric": "equality",
                    "left_column": {"name": "age", "index": 3},
                    "right_column": {"name": "age", "index": 3},
                    "boundary": 0.0,
                    "max_invalid_boundary": None,
                },
            ),
        ),
        ProfilingDepModel(
            task_id=task.id,
            result=make_md_result(
                lhs_items=[
                    {
                        "metric": "levenshtein",
                        "left_column": {"name": "id", "index": 0},
                        "right_column": {"name": "id", "index": 0},
                        "boundary": 0.5,
                        "max_invalid_boundary": 0.1,
                    },
                ],
                rhs_item={
                    "metric": "levenshtein",
                    "left_column": {"name": "score", "index": 4},
                    "right_column": {"name": "score", "index": 4},
                    "boundary": 0.0,
                    "max_invalid_boundary": None,
                },
            ),
        ),
        ProfilingDepModel(
            task_id=task.id,
            result=make_md_result(
                lhs_items=[
                    {
                        "metric": "jaccard",
                        "left_column": {"name": "alpha", "index": 0},
                        "right_column": {"name": "alpha", "index": 0},
                        "boundary": 0.0,
                        "max_invalid_boundary": None,
                    },
                    {
                        "metric": "equality",
                        "left_column": {"name": "beta", "index": 1},
                        "right_column": {"name": "beta", "index": 1},
                        "boundary": 0.0,
                        "max_invalid_boundary": None,
                    },
                ],
                rhs_item={
                    "metric": "equality",
                    "left_column": {"name": "gamma", "index": 2},
                    "right_column": {"name": "gamma", "index": 2},
                    "boundary": 0.0,
                    "max_invalid_boundary": None,
                },
            ),
        ),
        ProfilingDepModel(
            task_id=task.id,
            result=make_md_result(
                lhs_items=[
                    {
                        "metric": "monge_elkan",
                        "left_column": {"name": "gamma", "index": 2},
                        "right_column": {"name": "gamma", "index": 2},
                        "boundary": 0.8,
                        "max_invalid_boundary": 0.2,
                    },
                ],
                rhs_item={
                    "metric": "monge_elkan",
                    "left_column": {"name": "delta", "index": 3},
                    "right_column": {"name": "delta", "index": 3},
                    "boundary": 0.0,
                    "max_invalid_boundary": None,
                },
            ),
        ),
        ProfilingDepModel(
            task_id=task.id,
            result=make_md_result(
                lhs_items=[
                    {
                        "metric": "levenshtein",
                        "left_column": {"name": "name", "index": 1},
                        "right_column": {"name": "name", "index": 1},
                        "boundary": 0.0,
                        "max_invalid_boundary": None,
                    },
                ],
                rhs_item={
                    "metric": "equality",
                    "left_column": {"name": "email", "index": 2},
                    "right_column": {"name": "email", "index": 2},
                    "boundary": 0.0,
                    "max_invalid_boundary": None,
                },
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
