"""Fixtures for FD profiling dep CRUD tests."""

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
from src.schemas.task_schemas.types import PrimitiveName
from tests.integration.crud.task_crud.helpers import make_task_entity
from tests.integration.crud.profiling_dep_crud.fd.helpers import make_fd_result


@pytest_asyncio.fixture
async def fd_task(
    task_crud: TaskCrud,
    dataset: DatasetModel,
    user: UserModel,
) -> ProfilingTaskModel:
    entity = make_task_entity(
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
async def fd_profiling_dep_crud(session: AsyncSession) -> ProfilingDepCrud:
    return ProfilingDepCrud(session=session, primitive_name=PrimitiveName.FD)


@pytest_asyncio.fixture
async def many_fd_deps(
    session: AsyncSession,
    task_crud: TaskCrud,
    dataset: DatasetModel,
    user: UserModel,
) -> list[ProfilingDepModel]:
    entity = make_task_entity(datasets=[dataset], owner_id=user.id, is_public=False)
    task = await task_crud.create(entity=entity)
    await task_crud._session.execute(
        update(ProfilingTaskModel)
        .where(ProfilingTaskModel.id == task.id)
        .values(status=TaskStatus.SUCCESS)
    )
    await task_crud._session.commit()

    # FD results: lhs_columns=[{name, index}], rhs_column={name, index}
    deps = [
        ProfilingDepModel(
            task_id=task.id,
            result=make_fd_result(
                lhs_columns=[{"name": "id", "index": 0}],
                rhs_column={"name": "name", "index": 1},
            ),
        ),
        ProfilingDepModel(
            task_id=task.id,
            result=make_fd_result(
                lhs_columns=[{"name": "id", "index": 0}],
                rhs_column={"name": "email", "index": 2},
            ),
        ),
        ProfilingDepModel(
            task_id=task.id,
            result=make_fd_result(
                lhs_columns=[
                    {"name": "name", "index": 1},
                    {"name": "email", "index": 2},
                ],
                rhs_column={"name": "age", "index": 3},
            ),
        ),
        ProfilingDepModel(
            task_id=task.id,
            result=make_fd_result(
                lhs_columns=[{"name": "alpha", "index": 0}],
                rhs_column={"name": "beta", "index": 1},
            ),
        ),
        ProfilingDepModel(
            task_id=task.id,
            result=make_fd_result(
                lhs_columns=[{"name": "gamma", "index": 2}],
                rhs_column={"name": "delta", "index": 3},
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
