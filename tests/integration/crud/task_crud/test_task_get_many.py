from datetime import datetime, timedelta, timezone
from typing import Literal

import pytest

from src.crud.task_crud import TaskCrud
from src.models.task_models import ProfilingTaskModel
from src.models.user_models import UserModel
from src.schemas.base_schemas import (
    OrderingDirection,
    PaginationParamsSchema,
    TaskStatus,
)
from src.schemas.base_schemas import OrderingParamsSchema
from src.schemas.task_schemas.base_schemas import (
    TaskFiltersSchema,
    TaskQueryParamsSchema,
)

pytestmark = pytest.mark.asyncio

OrderByField = Literal["status", "created_at"]


def make_query_params(
    *,
    limit: int = 10,
    offset: int = 0,
    search: str | None = None,
    status: TaskStatus | None = None,
    created_after: datetime | None = None,
    created_before: datetime | None = None,
    order_by: OrderByField | None = None,
    direction: OrderingDirection = OrderingDirection.ASC,
) -> tuple[PaginationParamsSchema, TaskQueryParamsSchema]:
    pagination = PaginationParamsSchema(limit=limit, offset=offset)
    filters = TaskFiltersSchema(
        search=search or "",
        status=status,
        created_after=created_after,
        created_before=created_before,
    )
    ordering = OrderingParamsSchema[OrderByField](
        order_by=order_by,
        direction=direction,
    )
    query_params = TaskQueryParamsSchema(filters=filters, ordering=ordering)
    return pagination, query_params


async def test_get_many_pagination(
    task_crud: TaskCrud,
    many_tasks: list[ProfilingTaskModel],
    user: UserModel,
) -> None:
    pagination, query_params = make_query_params(limit=2, offset=0)
    result = await task_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        owner_id=user.id,
    )

    assert len(result.items) == 2
    assert result.total_count == 5
    assert result.limit == 2
    assert result.offset == 0

    pagination, query_params = make_query_params(limit=2, offset=2)
    result = await task_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        owner_id=user.id,
    )

    assert len(result.items) == 2
    assert result.total_count == 5

    pagination, query_params = make_query_params(limit=10, offset=0)
    result = await task_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        owner_id=user.id,
    )

    assert len(result.items) == 5
    assert result.total_count == 5


async def test_get_many_filter_search(
    task_crud: TaskCrud,
    many_tasks: list[ProfilingTaskModel],
    user: UserModel,
) -> None:
    pagination, query_params = make_query_params(search="alpha")
    result = await task_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        owner_id=user.id,
    )

    assert len(result.items) == 1
    assert result.items[0].datasets[0].name == "alpha.csv"
    assert result.total_count == 1


async def test_get_many_filter_status(
    task_crud: TaskCrud,
    many_tasks: list[ProfilingTaskModel],
    user: UserModel,
) -> None:
    pagination, query_params = make_query_params(status=TaskStatus.PENDING)
    result = await task_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        owner_id=user.id,
    )

    assert len(result.items) == 3
    assert all(t.status == TaskStatus.PENDING for t in result.items)
    assert result.total_count == 3

    pagination, query_params = make_query_params(status=TaskStatus.SUCCESS)
    result = await task_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        owner_id=user.id,
    )

    assert len(result.items) == 2
    assert all(t.status == TaskStatus.SUCCESS for t in result.items)
    assert result.total_count == 2


async def test_get_many_filter_created(
    task_crud: TaskCrud,
    many_tasks: list[ProfilingTaskModel],
    user: UserModel,
) -> None:
    base = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

    pagination, query_params = make_query_params(
        created_after=base + timedelta(seconds=2),
    )
    result = await task_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        owner_id=user.id,
    )

    assert len(result.items) == 3
    assert all(t.created_at >= base + timedelta(seconds=2) for t in result.items)
    assert result.total_count == 3

    pagination, query_params = make_query_params(
        created_before=base + timedelta(seconds=2),
    )
    result = await task_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        owner_id=user.id,
    )

    assert len(result.items) == 3
    assert all(t.created_at <= base + timedelta(seconds=2) for t in result.items)
    assert result.total_count == 3

    pagination, query_params = make_query_params(
        created_after=base + timedelta(seconds=1),
        created_before=base + timedelta(seconds=3),
    )
    result = await task_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        owner_id=user.id,
    )

    assert len(result.items) == 3
    assert all(
        base + timedelta(seconds=1) <= t.created_at <= base + timedelta(seconds=3)
        for t in result.items
    )
    assert result.total_count == 3


async def test_get_many_filter_owner_id(
    task_crud: TaskCrud,
    many_tasks: list[ProfilingTaskModel],
    user: UserModel,
    second_user: UserModel,
) -> None:
    pagination, query_params = make_query_params()
    result = await task_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        owner_id=user.id,
    )

    assert len(result.items) == 5
    assert all(t.owner_id == user.id for t in result.items)
    assert result.total_count == 5

    result = await task_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        owner_id=second_user.id,
    )

    assert len(result.items) == 1
    assert result.items[0].owner_id == second_user.id
    assert result.total_count == 1


@pytest.mark.parametrize(
    ("order_by", "direction", "expected_first_dataset"),
    [
        ("status", OrderingDirection.ASC, "alpha.csv"),
        ("status", OrderingDirection.DESC, "gamma.csv"),
        ("created_at", OrderingDirection.ASC, "alpha.csv"),
        ("created_at", OrderingDirection.DESC, "epsilon.csv"),
    ],
)
async def test_get_many_ordering(
    task_crud: TaskCrud,
    many_tasks: list[ProfilingTaskModel],
    user: UserModel,
    order_by: OrderByField,
    direction: OrderingDirection,
    expected_first_dataset: str,
) -> None:
    pagination, query_params = make_query_params(
        order_by=order_by,
        direction=direction,
    )
    result = await task_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        owner_id=user.id,
    )

    assert len(result.items) >= 1
    assert result.items[0].datasets[0].name == expected_first_dataset


async def test_get_many_empty_result(
    task_crud: TaskCrud,
    many_tasks: list[ProfilingTaskModel],
    user: UserModel,
) -> None:
    pagination, query_params = make_query_params(search="nonexistent")
    result = await task_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        owner_id=user.id,
    )

    assert len(result.items) == 0
    assert result.total_count == 0
