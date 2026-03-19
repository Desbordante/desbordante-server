"""Integration tests for ProfilingDepCrud.get_many (DD primitive)."""

import pytest

from src.crud.profiling_dep_crud.profiling_dep_crud import ProfilingDepCrud
from src.models.task_models import ProfilingDepModel
from src.schemas.base_schemas import OrderingDirection
from src.schemas.task_schemas.primitives.dd.task_result import (
    DdTaskResultOrderingField,
)
from tests.integration.crud.profiling_dep_crud.dd.helpers import make_query_params

pytestmark = pytest.mark.asyncio


async def test_get_many_filter_search(
    dd_profiling_dep_crud: ProfilingDepCrud,
    many_dd_deps: list[ProfilingDepModel],
) -> None:
    task_id = many_dd_deps[0].task_id

    pagination, query_params = make_query_params(search="alpha")
    result = await dd_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) == 1
    assert "alpha" in str(result.items[0].result)
    assert result.total_count == 1


async def test_get_many_filter_rhs_item_names(
    dd_profiling_dep_crud: ProfilingDepCrud,
    many_dd_deps: list[ProfilingDepModel],
) -> None:
    task_id = many_dd_deps[0].task_id

    pagination, query_params = make_query_params(rhs_item_names=["age"])
    result = await dd_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) == 1
    assert result.items[0].result.rhs_item.name == "age"  # type: ignore
    assert result.total_count == 1


async def test_get_many_filter_rhs_item_indices(
    dd_profiling_dep_crud: ProfilingDepCrud,
    many_dd_deps: list[ProfilingDepModel],
) -> None:
    task_id = many_dd_deps[0].task_id

    pagination, query_params = make_query_params(rhs_item_indices=[3])
    result = await dd_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) == 2
    assert all(r.result.rhs_item.index == 3 for r in result.items)  # type: ignore
    assert result.total_count == 2


async def test_get_many_filter_lhs_items_names(
    dd_profiling_dep_crud: ProfilingDepCrud,
    many_dd_deps: list[ProfilingDepModel],
) -> None:
    task_id = many_dd_deps[0].task_id

    pagination, query_params = make_query_params(lhs_items_names=["name"])
    result = await dd_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) == 1
    assert result.items[0].result.lhs_items[0].name == "name"  # type: ignore
    assert result.total_count == 1


async def test_get_many_filter_lhs_items_indices(
    dd_profiling_dep_crud: ProfilingDepCrud,
    many_dd_deps: list[ProfilingDepModel],
) -> None:
    task_id = many_dd_deps[0].task_id

    pagination, query_params = make_query_params(lhs_items_indices=[0])
    result = await dd_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) >= 1
    assert all(
        any(item.index == 0 for item in r.result.lhs_items)  # type: ignore
        for r in result.items
    )
    assert result.total_count >= 1


@pytest.mark.parametrize(
    ("order_by", "direction", "expected_rhs_name"),
    [
        (
            DdTaskResultOrderingField.RHS_ITEM_NAMES,
            OrderingDirection.ASC,
            "age",
        ),
        (
            DdTaskResultOrderingField.RHS_ITEM_NAMES,
            OrderingDirection.DESC,
            "score",
        ),
        (
            DdTaskResultOrderingField.NUMBER_OF_LHS_ITEMS,
            OrderingDirection.ASC,
            {"age", "score", "delta", "email"},
        ),
        (
            DdTaskResultOrderingField.NUMBER_OF_LHS_ITEMS,
            OrderingDirection.DESC,
            "gamma",
        ),
    ],
)
async def test_get_many_ordering(
    dd_profiling_dep_crud: ProfilingDepCrud,
    many_dd_deps: list[ProfilingDepModel],
    order_by: str,
    direction: OrderingDirection,
    expected_rhs_name: str | set[str],
) -> None:
    task_id = many_dd_deps[0].task_id

    pagination, query_params = make_query_params(
        order_by=order_by,
        direction=direction,
    )
    result = await dd_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) >= 1
    actual = result.items[0].result.rhs_item.name  # type: ignore
    if isinstance(expected_rhs_name, set):
        assert actual in expected_rhs_name
    else:
        assert actual == expected_rhs_name
