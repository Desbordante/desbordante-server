"""Integration tests for ProfilingDepCrud.get_many (AR primitive)."""

import pytest

from src.crud.profiling_dep_crud.profiling_dep_crud import ProfilingDepCrud
from src.models.task_models import ProfilingDepModel
from src.schemas.base_schemas import OrderingDirection
from src.schemas.task_schemas.primitives.ar.task_result import (
    ArTaskResultOrderingField,
)
from tests.integration.crud.profiling_dep_crud.ar.helpers import make_query_params

pytestmark = pytest.mark.asyncio


async def test_get_many_filter_search(
    ar_profiling_dep_crud: ProfilingDepCrud,
    many_ar_deps: list[ProfilingDepModel],
) -> None:
    task_id = many_ar_deps[0].task_id

    pagination, query_params = make_query_params(search="alpha")
    result = await ar_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) == 1
    assert "alpha" in str(result.items[0].result)
    assert result.total_count == 1


async def test_get_many_filter_lhs_values(
    ar_profiling_dep_crud: ProfilingDepCrud,
    many_ar_deps: list[ProfilingDepModel],
) -> None:
    task_id = many_ar_deps[0].task_id

    pagination, query_params = make_query_params(lhs_values=["bread"])
    result = await ar_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) == 1
    assert result.items[0].result.lhs_values == ["bread"]  # type: ignore
    assert result.total_count == 1


async def test_get_many_filter_rhs_values(
    ar_profiling_dep_crud: ProfilingDepCrud,
    many_ar_deps: list[ProfilingDepModel],
) -> None:
    task_id = many_ar_deps[0].task_id

    pagination, query_params = make_query_params(rhs_values=["bar"])
    result = await ar_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) == 1
    assert result.items[0].result.rhs_values == ["bar"]  # type: ignore
    assert result.total_count == 1


async def test_get_many_filter_min_support(
    ar_profiling_dep_crud: ProfilingDepCrud,
    many_ar_deps: list[ProfilingDepModel],
) -> None:
    task_id = many_ar_deps[0].task_id

    pagination, query_params = make_query_params(min_support=0.5)
    result = await ar_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) == 2
    assert all(r.result.support >= 0.5 for r in result.items)  # type: ignore
    assert result.total_count == 2


async def test_get_many_filter_max_support(
    ar_profiling_dep_crud: ProfilingDepCrud,
    many_ar_deps: list[ProfilingDepModel],
) -> None:
    task_id = many_ar_deps[0].task_id

    pagination, query_params = make_query_params(max_support=0.3)
    result = await ar_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) == 2
    assert all(r.result.support <= 0.3 for r in result.items)  # type: ignore
    assert result.total_count == 2


async def test_get_many_filter_min_confidence(
    ar_profiling_dep_crud: ProfilingDepCrud,
    many_ar_deps: list[ProfilingDepModel],
) -> None:
    task_id = many_ar_deps[0].task_id

    pagination, query_params = make_query_params(min_confidence=0.8)
    result = await ar_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) == 3
    assert all(r.result.confidence >= 0.8 for r in result.items)  # type: ignore
    assert result.total_count == 3


async def test_get_many_filter_max_confidence(
    ar_profiling_dep_crud: ProfilingDepCrud,
    many_ar_deps: list[ProfilingDepModel],
) -> None:
    task_id = many_ar_deps[0].task_id

    pagination, query_params = make_query_params(max_confidence=0.3)
    result = await ar_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) == 1
    assert result.items[0].result.confidence == 0.2  # type: ignore
    assert result.total_count == 1


@pytest.mark.parametrize(
    ("order_by", "direction", "expected_support"),
    [
        (
            ArTaskResultOrderingField.SUPPORT,
            OrderingDirection.ASC,
            0.1,
        ),
        (
            ArTaskResultOrderingField.SUPPORT,
            OrderingDirection.DESC,
            0.7,
        ),
        (
            ArTaskResultOrderingField.CONFIDENCE,
            OrderingDirection.ASC,
            0.2,
        ),
        (
            ArTaskResultOrderingField.CONFIDENCE,
            OrderingDirection.DESC,
            0.95,
        ),
    ],
)
async def test_get_many_ordering(
    ar_profiling_dep_crud: ProfilingDepCrud,
    many_ar_deps: list[ProfilingDepModel],
    order_by: str,
    direction: OrderingDirection,
    expected_support: float,
) -> None:
    task_id = many_ar_deps[0].task_id

    pagination, query_params = make_query_params(
        order_by=order_by,
        direction=direction,
    )
    result = await ar_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) >= 1
    first = result.items[0].result  # type: ignore
    if order_by == ArTaskResultOrderingField.SUPPORT:
        assert first.support == expected_support
    else:
        assert first.confidence == expected_support
