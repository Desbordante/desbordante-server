from datetime import datetime, timedelta, timezone
from typing import Literal

import pytest

from src.crud.dataset_crud import DatasetCrud
from src.models.dataset_models import DatasetModel
from src.models.user_models import UserModel
from src.schemas.base_schemas import (
    OrderingDirection,
    PaginationParamsSchema,
)
from src.schemas.base_schemas import OrderingParamsSchema
from src.schemas.dataset_schemas import (
    DatasetFiltersSchema,
    DatasetQueryParamsSchema,
    DatasetType,
)

from tests.integration.crud.dataset_crud.helpers import make_dataset_entity

pytestmark = pytest.mark.asyncio

OrderByField = Literal["name", "size", "created_at"]


def make_query_params(
    *,
    limit: int = 10,
    offset: int = 0,
    search: str | None = None,
    type: DatasetType | None = None,
    is_public: bool | None = None,
    min_size: int | None = None,
    max_size: int | None = None,
    created_after: datetime | None = None,
    created_before: datetime | None = None,
    order_by: OrderByField | None = None,
    direction: OrderingDirection = OrderingDirection.ASC,
) -> tuple[PaginationParamsSchema, DatasetQueryParamsSchema]:
    pagination = PaginationParamsSchema(limit=limit, offset=offset)
    filters = DatasetFiltersSchema(
        search=search or "",
        type=type,
        is_public=is_public,
        min_size=min_size,
        max_size=max_size,
        created_after=created_after,
        created_before=created_before,
    )
    ordering = OrderingParamsSchema[OrderByField](
        order_by=order_by,
        direction=direction,
    )
    query_params = DatasetQueryParamsSchema(filters=filters, ordering=ordering)
    return pagination, query_params


async def test_get_many_pagination(
    dataset_crud: DatasetCrud,
    many_datasets: list[DatasetModel],
    user: UserModel,
) -> None:
    pagination, query_params = make_query_params(limit=2, offset=0)
    result = await dataset_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        owner_id=user.id,
    )

    assert len(result.items) == 2
    assert result.total_count == 5
    assert result.limit == 2
    assert result.offset == 0

    pagination, query_params = make_query_params(limit=2, offset=2)
    result = await dataset_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        owner_id=user.id,
    )

    assert len(result.items) == 2
    assert result.total_count == 5

    pagination, query_params = make_query_params(limit=10, offset=0)
    result = await dataset_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        owner_id=user.id,
    )

    assert len(result.items) == 5
    assert result.total_count == 5


async def test_get_many_filter_search(
    dataset_crud: DatasetCrud,
    many_datasets: list[DatasetModel],
    user: UserModel,
) -> None:
    pagination, query_params = make_query_params(search="alpha")
    result = await dataset_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        owner_id=user.id,
    )

    assert len(result.items) == 1
    assert result.items[0].name == "alpha.csv"
    assert result.total_count == 1


async def test_get_many_filter_type(
    dataset_crud: DatasetCrud,
    many_datasets: list[DatasetModel],
    user: UserModel,
) -> None:
    pagination, query_params = make_query_params(type=DatasetType.TABULAR)
    result = await dataset_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        owner_id=user.id,
    )

    assert len(result.items) == 4
    assert all(d.type == DatasetType.TABULAR for d in result.items)
    assert result.total_count == 4

    pagination, query_params = make_query_params(type=DatasetType.TRANSACTIONAL)
    result = await dataset_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        owner_id=user.id,
    )

    assert len(result.items) == 1
    assert result.items[0].type == DatasetType.TRANSACTIONAL
    assert result.total_count == 1


async def test_get_many_filter_is_public(
    dataset_crud: DatasetCrud,
    many_datasets: list[DatasetModel],
    user: UserModel,
) -> None:
    pagination, query_params = make_query_params(is_public=True)
    result = await dataset_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        owner_id=user.id,
    )

    assert len(result.items) == 2
    assert all(d.is_public is True for d in result.items)
    assert result.total_count == 2

    pagination, query_params = make_query_params(is_public=False)
    result = await dataset_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        owner_id=user.id,
    )

    assert len(result.items) == 3
    assert all(d.is_public is False for d in result.items)
    assert result.total_count == 3


async def test_get_many_filter_size(
    dataset_crud: DatasetCrud,
    many_datasets: list[DatasetModel],
    user: UserModel,
) -> None:
    pagination, query_params = make_query_params(min_size=150)
    result = await dataset_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        owner_id=user.id,
    )

    assert len(result.items) == 4
    assert all(d.size >= 150 for d in result.items)
    assert result.total_count == 4

    pagination, query_params = make_query_params(max_size=200)
    result = await dataset_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        owner_id=user.id,
    )

    assert len(result.items) == 3
    assert all(d.size <= 200 for d in result.items)
    assert result.total_count == 3

    pagination, query_params = make_query_params(min_size=150, max_size=250)
    result = await dataset_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        owner_id=user.id,
    )

    assert len(result.items) == 3
    assert all(150 <= d.size <= 250 for d in result.items)
    assert result.total_count == 3


async def test_get_many_filter_created(
    dataset_crud: DatasetCrud,
    many_datasets: list[DatasetModel],
    user: UserModel,
) -> None:
    base = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

    pagination, query_params = make_query_params(
        created_after=base + timedelta(seconds=2),
    )
    result = await dataset_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        owner_id=user.id,
    )

    assert len(result.items) == 3
    assert all(d.created_at >= base + timedelta(seconds=2) for d in result.items)
    assert result.total_count == 3

    pagination, query_params = make_query_params(
        created_before=base + timedelta(seconds=2),
    )
    result = await dataset_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        owner_id=user.id,
    )

    assert len(result.items) == 3
    assert all(d.created_at <= base + timedelta(seconds=2) for d in result.items)
    assert result.total_count == 3

    pagination, query_params = make_query_params(
        created_after=base + timedelta(seconds=1),
        created_before=base + timedelta(seconds=3),
    )
    result = await dataset_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        owner_id=user.id,
    )

    assert len(result.items) == 3
    assert all(
        base + timedelta(seconds=1) <= d.created_at <= base + timedelta(seconds=3)
        for d in result.items
    )
    assert result.total_count == 3


async def test_get_many_filter_owner_id(
    dataset_crud: DatasetCrud,
    many_datasets: list[DatasetModel],
    user: UserModel,
    second_user: UserModel,
) -> None:
    pagination, query_params = make_query_params()
    result = await dataset_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        owner_id=user.id,
    )

    assert len(result.items) == 5
    assert all(d.owner_id == user.id for d in result.items)
    assert result.total_count == 5

    result = await dataset_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        owner_id=second_user.id,
    )

    assert len(result.items) == 1
    assert result.items[0].owner_id == second_user.id
    assert result.total_count == 1


@pytest.mark.parametrize(
    ("order_by", "direction", "expected_first"),
    [
        ("name", OrderingDirection.ASC, "alpha.csv"),
        ("name", OrderingDirection.DESC, "gamma.csv"),
        ("size", OrderingDirection.ASC, "alpha.csv"),
        ("size", OrderingDirection.DESC, "gamma.csv"),
        ("created_at", OrderingDirection.ASC, "alpha.csv"),
        ("created_at", OrderingDirection.DESC, "epsilon.csv"),
    ],
)
async def test_get_many_ordering(
    dataset_crud: DatasetCrud,
    many_datasets: list[DatasetModel],
    user: UserModel,
    order_by: OrderByField,
    direction: OrderingDirection,
    expected_first: str,
) -> None:
    pagination, query_params = make_query_params(
        order_by=order_by,
        direction=direction,
    )
    result = await dataset_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        owner_id=user.id,
    )

    assert len(result.items) >= 1
    assert result.items[0].name == expected_first


async def test_get_many_filter_status(
    dataset_crud: DatasetCrud,
    user: UserModel,
) -> None:
    from src.schemas.base_schemas import TaskStatus

    entity = make_dataset_entity(owner_id=user.id, name="pending.csv")
    created = await dataset_crud.create(entity=entity)

    pagination, query_params = make_query_params()
    query_params.filters.status = TaskStatus.PENDING
    result = await dataset_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        owner_id=user.id,
    )

    assert len(result.items) >= 1
    assert any(d.id == created.id for d in result.items)


async def test_get_many_empty_result(
    dataset_crud: DatasetCrud,
    many_datasets: list[DatasetModel],
    user: UserModel,
) -> None:
    pagination, query_params = make_query_params(search="nonexistent")
    result = await dataset_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        owner_id=user.id,
    )

    assert len(result.items) == 0
    assert result.total_count == 0
