"""Fixtures for FD verification profiling dep CRUD tests."""

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
from src.schemas.task_schemas.primitives.fd_verification.algo_config import (
    FdVerifierConfig,
)
from src.schemas.task_schemas.primitives.fd_verification.algo_name import (
    FdVerificationAlgoName,
)
from src.schemas.task_schemas.primitives.fd_verification.task_params import (
    FdVerificationTaskDatasetsConfig,
    FdVerificationTaskParams,
)
from src.schemas.task_schemas.types import PrimitiveName
from tests.integration.crud.profiling_dep_crud.fd_verification.helpers import (
    make_fd_verification_result,
)


def _make_fd_verification_task_entity(
    *,
    datasets: list[DatasetModel],
    owner_id: int | None = None,
    is_public: bool = False,
) -> ProfilingTaskModel:
    params = FdVerificationTaskParams(
        primitive_name=PrimitiveName.FD_VERIFICATION,
        config=FdVerifierConfig(algo_name=FdVerificationAlgoName.FD_VERIFIER),
        datasets=FdVerificationTaskDatasetsConfig(table=datasets[0].id),
    )
    return ProfilingTaskModel(
        params=params,
        datasets=datasets,
        owner_id=owner_id,
        is_public=is_public,
    )


@pytest_asyncio.fixture
async def fd_verification_task(
    task_crud: TaskCrud,
    dataset: DatasetModel,
    user: UserModel,
) -> ProfilingTaskModel:
    entity = _make_fd_verification_task_entity(
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
async def fd_verification_profiling_dep_crud(
    session: AsyncSession,
) -> ProfilingDepCrud:
    return ProfilingDepCrud(
        session=session, primitive_name=PrimitiveName.FD_VERIFICATION
    )


@pytest_asyncio.fixture
async def many_fd_verification_deps(
    session: AsyncSession,
    task_crud: TaskCrud,
    dataset: DatasetModel,
    user: UserModel,
) -> list[ProfilingDepModel]:
    entity = _make_fd_verification_task_entity(
        datasets=[dataset], owner_id=user.id, is_public=False
    )
    task = await task_crud.create(entity=entity)
    await task_crud._session.execute(
        update(ProfilingTaskModel)
        .where(ProfilingTaskModel.id == task.id)
        .values(status=TaskStatus.SUCCESS)
    )
    await task_crud._session.commit()

    # FD verification: number_of_distinct_rhs_values, most_frequent_rhs_value_proportion, rows
    deps = [
        ProfilingDepModel(
            task_id=task.id,
            result=make_fd_verification_result(
                number_of_distinct_rhs_values=5,
                most_frequent_rhs_value_proportion=0.2,
                rows=[
                    {"row_index": 0, "values": ["a", "b"]},
                    {"row_index": 1, "values": ["c", "d"]},
                ],
            ),
        ),
        ProfilingDepModel(
            task_id=task.id,
            result=make_fd_verification_result(
                number_of_distinct_rhs_values=3,
                most_frequent_rhs_value_proportion=0.5,
                rows=[
                    {"row_index": 0, "values": ["alpha", "beta"]},
                    {"row_index": 1, "values": ["gamma", "delta"]},
                ],
            ),
        ),
        ProfilingDepModel(
            task_id=task.id,
            result=make_fd_verification_result(
                number_of_distinct_rhs_values=10,
                most_frequent_rhs_value_proportion=0.1,
                rows=[{"row_index": 0, "values": ["x", "y"]}],
            ),
        ),
        ProfilingDepModel(
            task_id=task.id,
            result=make_fd_verification_result(
                number_of_distinct_rhs_values=2,
                most_frequent_rhs_value_proportion=0.9,
                rows=[
                    {"row_index": 0, "values": ["p", "q"]},
                    {"row_index": 1, "values": ["r", "s"]},
                    {"row_index": 2, "values": ["t", "u"]},
                ],
            ),
        ),
        ProfilingDepModel(
            task_id=task.id,
            result=make_fd_verification_result(
                number_of_distinct_rhs_values=7,
                most_frequent_rhs_value_proportion=0.3,
                rows=[
                    {"row_index": 0, "values": ["foo", "bar"]},
                    {"row_index": 1, "values": ["baz", "qux"]},
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
