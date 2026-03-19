"""Integration tests for ProfilingDepCrud.get_many (NAR primitive)."""

import pytest

from src.crud.profiling_dep_crud.profiling_dep_crud import ProfilingDepCrud
from src.models.task_models import ProfilingDepModel
from src.schemas.base_schemas import OrderingDirection
from src.schemas.task_schemas.primitives.nar.task_result import (
    NarTaskResultOrderingField,
)
from tests.integration.crud.profiling_dep_crud.nar.helpers import make_query_params

pytestmark = pytest.mark.asyncio


async def test_get_many_filter_search(
    nar_profiling_dep_crud: ProfilingDepCrud,
    many_nar_deps: list[ProfilingDepModel],
) -> None:
    task_id = many_nar_deps[0].task_id

    pagination, query_params = make_query_params(search="alpha")
    result = await nar_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) == 2
    assert "alpha" in str(result.items[0].result)
    assert result.total_count == 2


async def test_get_many_filter_min_confidence(
    nar_profiling_dep_crud: ProfilingDepCrud,
    many_nar_deps: list[ProfilingDepModel],
) -> None:
    task_id = many_nar_deps[0].task_id

    pagination, query_params = make_query_params(min_confidence=0.8)
    result = await nar_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) == 2
    assert all(r.result.confidence >= 0.8 for r in result.items)  # type: ignore
    assert result.total_count == 2


async def test_get_many_filter_max_support(
    nar_profiling_dep_crud: ProfilingDepCrud,
    many_nar_deps: list[ProfilingDepModel],
) -> None:
    task_id = many_nar_deps[0].task_id

    pagination, query_params = make_query_params(max_support=0.2)
    result = await nar_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) == 1
    assert result.items[0].result.support == 0.1  # type: ignore
    assert result.total_count == 1


async def test_get_many_filter_lhs_items_names(
    nar_profiling_dep_crud: ProfilingDepCrud,
    many_nar_deps: list[ProfilingDepModel],
) -> None:
    task_id = many_nar_deps[0].task_id

    pagination, query_params = make_query_params(lhs_items_names=["gamma"])
    result = await nar_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) == 1
    assert result.items[0].result.lhs_items[0].name == "gamma"  # type: ignore
    assert result.total_count == 1


async def test_get_many_filter_rhs_items_names(
    nar_profiling_dep_crud: ProfilingDepCrud,
    many_nar_deps: list[ProfilingDepModel],
) -> None:
    task_id = many_nar_deps[0].task_id

    pagination, query_params = make_query_params(rhs_items_names=["baz"])
    result = await nar_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) == 1
    assert result.items[0].result.rhs_items[0].name == "baz"  # type: ignore
    assert result.total_count == 1


@pytest.mark.parametrize(
    ("order_by", "direction", "expected_value"),
    [
        (
            NarTaskResultOrderingField.CONFIDENCE,
            OrderingDirection.ASC,
            0.2,
        ),
        (
            NarTaskResultOrderingField.CONFIDENCE,
            OrderingDirection.DESC,
            0.95,
        ),
        (
            NarTaskResultOrderingField.SUPPORT,
            OrderingDirection.ASC,
            0.1,
        ),
        (
            NarTaskResultOrderingField.SUPPORT,
            OrderingDirection.DESC,
            0.8,
        ),
        (
            NarTaskResultOrderingField.NUMBER_OF_LHS_ITEMS,
            OrderingDirection.ASC,
            1,
        ),
        (
            NarTaskResultOrderingField.NUMBER_OF_LHS_ITEMS,
            OrderingDirection.DESC,
            2,
        ),
    ],
)
async def test_get_many_ordering(
    nar_profiling_dep_crud: ProfilingDepCrud,
    many_nar_deps: list[ProfilingDepModel],
    order_by: str,
    direction: OrderingDirection,
    expected_value: int | float,
) -> None:
    task_id = many_nar_deps[0].task_id

    pagination, query_params = make_query_params(
        order_by=order_by,
        direction=direction,
    )
    result = await nar_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) >= 1
    first = result.items[0].result  # type: ignore
    if order_by == NarTaskResultOrderingField.CONFIDENCE:
        assert first.confidence == expected_value
    elif order_by == NarTaskResultOrderingField.SUPPORT:
        assert first.support == expected_value
    else:
        assert len(first.lhs_items) == expected_value
