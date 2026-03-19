"""Fixtures for MFD verification profiling dep CRUD tests."""

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
from src.schemas.task_schemas.primitives.mfd_verification.algo_config import (
    MetricVerifierConfig,
)
from src.schemas.task_schemas.primitives.mfd_verification.algo_name import (
    MfdVerificationAlgoName,
)
from src.schemas.task_schemas.primitives.mfd_verification.task_params import (
    MfdVerificationTaskDatasetsConfig,
    MfdVerificationTaskParams,
)
from src.schemas.task_schemas.types import PrimitiveName
from tests.integration.crud.profiling_dep_crud.mfd_verification.helpers import (
    make_mfd_verification_result,
)


def _make_mfd_verification_task_entity(
    *,
    datasets: list[DatasetModel],
    owner_id: int | None = None,
    is_public: bool = False,
) -> ProfilingTaskModel:
    params = MfdVerificationTaskParams(
        primitive_name=PrimitiveName.MFD_VERIFICATION,
        config=MetricVerifierConfig(
            algo_name=MfdVerificationAlgoName.METRIC_VERIFIER,
        ),
        datasets=MfdVerificationTaskDatasetsConfig(table=datasets[0].id),
    )
    return ProfilingTaskModel(
        params=params,
        datasets=datasets,
        owner_id=owner_id,
        is_public=is_public,
    )


@pytest_asyncio.fixture
async def mfd_verification_task(
    task_crud: TaskCrud,
    dataset: DatasetModel,
    user: UserModel,
) -> ProfilingTaskModel:
    entity = _make_mfd_verification_task_entity(
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
async def mfd_verification_profiling_dep_crud(
    session: AsyncSession,
) -> ProfilingDepCrud:
    return ProfilingDepCrud(
        session=session, primitive_name=PrimitiveName.MFD_VERIFICATION
    )


@pytest_asyncio.fixture
async def many_mfd_verification_deps(
    session: AsyncSession,
    task_crud: TaskCrud,
    dataset: DatasetModel,
    user: UserModel,
) -> list[ProfilingDepModel]:
    entity = _make_mfd_verification_task_entity(
        datasets=[dataset], owner_id=user.id, is_public=False
    )
    task = await task_crud.create(entity=entity)
    await task_crud._session.execute(
        update(ProfilingTaskModel)
        .where(ProfilingTaskModel.id == task.id)
        .values(status=TaskStatus.SUCCESS)
    )
    await task_crud._session.commit()

    # MFD verification: cluster_index, lhs_values, max_distance, highlights
    deps = [
        ProfilingDepModel(
            task_id=task.id,
            result=make_mfd_verification_result(
                cluster_index=0,
                lhs_values=["alpha", "beta"],
                max_distance=1.5,
                highlights=[
                    {
                        "data_index": 0,
                        "furthest_data_index": 2,
                        "max_distance": 0.5,
                        "rhs_values": ["x", "y"],
                        "within_limit": True,
                    },
                ],
            ),
        ),
        ProfilingDepModel(
            task_id=task.id,
            result=make_mfd_verification_result(
                cluster_index=1,
                lhs_values=["gamma", "delta"],
                max_distance=2.0,
                highlights=[
                    {
                        "data_index": 1,
                        "furthest_data_index": 3,
                        "max_distance": 1.0,
                        "rhs_values": ["a", "b"],
                        "within_limit": False,
                    },
                ],
            ),
        ),
        ProfilingDepModel(
            task_id=task.id,
            result=make_mfd_verification_result(
                cluster_index=2,
                lhs_values=["epsilon", "zeta"],
                max_distance=0.8,
                highlights=[
                    {
                        "data_index": 2,
                        "furthest_data_index": 0,
                        "max_distance": 0.3,
                        "rhs_values": ["foo", "bar"],
                        "within_limit": True,
                    },
                ],
            ),
        ),
        ProfilingDepModel(
            task_id=task.id,
            result=make_mfd_verification_result(
                cluster_index=0,
                lhs_values=["alpha", "omega"],
                max_distance=3.0,
                highlights=[
                    {
                        "data_index": 3,
                        "furthest_data_index": 1,
                        "max_distance": 2.0,
                        "rhs_values": ["baz", "qux"],
                        "within_limit": False,
                    },
                ],
            ),
        ),
        ProfilingDepModel(
            task_id=task.id,
            result=make_mfd_verification_result(
                cluster_index=3,
                lhs_values=["iota", "kappa"],
                max_distance=0.5,
                highlights=[
                    {
                        "data_index": 0,
                        "furthest_data_index": 1,
                        "max_distance": 0.2,
                        "rhs_values": ["test", "data"],
                        "within_limit": True,
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
