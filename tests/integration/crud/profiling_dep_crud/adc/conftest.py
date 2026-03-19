"""Fixtures for ADC profiling dep CRUD tests."""

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
from src.schemas.task_schemas.primitives.adc.algo_config import FastAdcConfig
from src.schemas.task_schemas.primitives.adc.algo_name import AdcAlgoName
from src.schemas.task_schemas.primitives.adc.task_params import (
    AdcTaskDatasetsConfig,
    AdcTaskParams,
)
from src.schemas.task_schemas.types import PrimitiveName
from tests.integration.crud.profiling_dep_crud.adc.helpers import make_adc_result


def _make_adc_task_entity(
    *,
    datasets: list[DatasetModel],
    owner_id: int | None = None,
    is_public: bool = False,
) -> ProfilingTaskModel:
    params = AdcTaskParams(
        primitive_name=PrimitiveName.ADC,
        config=FastAdcConfig(algo_name=AdcAlgoName.FAST_ADC),
        datasets=AdcTaskDatasetsConfig(table=datasets[0].id),
    )
    return ProfilingTaskModel(
        params=params,
        datasets=datasets,
        owner_id=owner_id,
        is_public=is_public,
    )


@pytest_asyncio.fixture
async def adc_task(
    task_crud: TaskCrud,
    dataset: DatasetModel,
    user: UserModel,
) -> ProfilingTaskModel:
    entity = _make_adc_task_entity(
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
async def adc_profiling_dep_crud(session: AsyncSession) -> ProfilingDepCrud:
    return ProfilingDepCrud(session=session, primitive_name=PrimitiveName.ADC)


@pytest_asyncio.fixture
async def many_adc_deps(
    session: AsyncSession,
    task_crud: TaskCrud,
    dataset: DatasetModel,
    user: UserModel,
) -> list[ProfilingDepModel]:
    entity = _make_adc_task_entity(
        datasets=[dataset], owner_id=user.id, is_public=False
    )
    task = await task_crud.create(entity=entity)
    await task_crud._session.execute(
        update(ProfilingTaskModel)
        .where(ProfilingTaskModel.id == task.id)
        .values(status=TaskStatus.SUCCESS)
    )
    await task_crud._session.commit()

    # ADC results: conjuncts = [{lhs_item: {name, index, prefix}, rhs_item: {...}, operator}]
    deps = [
        ProfilingDepModel(
            task_id=task.id,
            result=make_adc_result(
                conjuncts=[
                    {
                        "lhs_item": {"name": "id", "index": 0, "prefix": "col"},
                        "rhs_item": {"name": "age", "index": 3, "prefix": "col"},
                        "operator": ">=",
                    },
                ],
            ),
        ),
        ProfilingDepModel(
            task_id=task.id,
            result=make_adc_result(
                conjuncts=[
                    {
                        "lhs_item": {"name": "id", "index": 0, "prefix": "col"},
                        "rhs_item": {"name": "score", "index": 4, "prefix": "col"},
                        "operator": "<",
                    },
                ],
            ),
        ),
        ProfilingDepModel(
            task_id=task.id,
            result=make_adc_result(
                conjuncts=[
                    {
                        "lhs_item": {"name": "alpha", "index": 0, "prefix": "col"},
                        "rhs_item": {"name": "beta", "index": 1, "prefix": "col"},
                        "operator": "==",
                    },
                    {
                        "lhs_item": {"name": "gamma", "index": 2, "prefix": "col"},
                        "rhs_item": {"name": "delta", "index": 3, "prefix": "col"},
                        "operator": "!=",
                    },
                ],
            ),
        ),
        ProfilingDepModel(
            task_id=task.id,
            result=make_adc_result(
                conjuncts=[
                    {
                        "lhs_item": {"name": "gamma", "index": 2, "prefix": "col"},
                        "rhs_item": {"name": "delta", "index": 3, "prefix": "col"},
                        "operator": "<=",
                    },
                ],
            ),
        ),
        ProfilingDepModel(
            task_id=task.id,
            result=make_adc_result(
                conjuncts=[
                    {
                        "lhs_item": {"name": "name", "index": 1, "prefix": "col"},
                        "rhs_item": {"name": "email", "index": 2, "prefix": "col"},
                        "operator": ">",
                    },
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
