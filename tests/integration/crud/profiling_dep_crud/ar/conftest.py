"""Fixtures for AR profiling dep CRUD tests."""

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
from src.schemas.task_schemas.primitives.ar.algo_config import AprioriConfig
from src.schemas.task_schemas.primitives.ar.algo_name import ArAlgoName
from src.schemas.task_schemas.primitives.ar.task_params import (
    ArTaskDatasetsConfig,
    ArTaskParams,
)
from src.schemas.task_schemas.types import PrimitiveName
from tests.integration.crud.profiling_dep_crud.ar.helpers import make_ar_result


def _make_ar_task_entity(
    *,
    datasets: list[DatasetModel],
    owner_id: int | None = None,
    is_public: bool = False,
) -> ProfilingTaskModel:
    params = ArTaskParams(
        primitive_name=PrimitiveName.AR,
        config=AprioriConfig(algo_name=ArAlgoName.APRIORI),
        datasets=ArTaskDatasetsConfig(table=datasets[0].id),
    )
    return ProfilingTaskModel(
        params=params,
        datasets=datasets,
        owner_id=owner_id,
        is_public=is_public,
    )


@pytest_asyncio.fixture
async def ar_task(
    task_crud: TaskCrud,
    dataset: DatasetModel,
    user: UserModel,
) -> ProfilingTaskModel:
    entity = _make_ar_task_entity(
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
async def ar_profiling_dep_crud(session: AsyncSession) -> ProfilingDepCrud:
    return ProfilingDepCrud(session=session, primitive_name=PrimitiveName.AR)


@pytest_asyncio.fixture
async def many_ar_deps(
    session: AsyncSession,
    task_crud: TaskCrud,
    dataset: DatasetModel,
    user: UserModel,
) -> list[ProfilingDepModel]:
    entity = _make_ar_task_entity(datasets=[dataset], owner_id=user.id, is_public=False)
    task = await task_crud.create(entity=entity)
    await task_crud._session.execute(
        update(ProfilingTaskModel)
        .where(ProfilingTaskModel.id == task.id)
        .values(status=TaskStatus.SUCCESS)
    )
    await task_crud._session.commit()

    # AR results: lhs_values, rhs_values, support, confidence
    deps = [
        ProfilingDepModel(
            task_id=task.id,
            result=make_ar_result(
                lhs_values=["bread"],
                rhs_values=["milk"],
                support=0.3,
                confidence=0.8,
            ),
        ),
        ProfilingDepModel(
            task_id=task.id,
            result=make_ar_result(
                lhs_values=["alpha", "beta"],
                rhs_values=["gamma"],
                support=0.5,
                confidence=0.9,
            ),
        ),
        ProfilingDepModel(
            task_id=task.id,
            result=make_ar_result(
                lhs_values=["x"],
                rhs_values=["y", "z"],
                support=0.1,
                confidence=0.2,
            ),
        ),
        ProfilingDepModel(
            task_id=task.id,
            result=make_ar_result(
                lhs_values=["foo"],
                rhs_values=["bar"],
                support=0.7,
                confidence=0.95,
            ),
        ),
        ProfilingDepModel(
            task_id=task.id,
            result=make_ar_result(
                lhs_values=["a", "b"],
                rhs_values=["c"],
                support=0.4,
                confidence=0.6,
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
