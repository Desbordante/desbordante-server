"""Integration tests for ProfilingDepCrud.get_many (MD primitive)."""

import pytest

from src.crud.profiling_dep_crud.profiling_dep_crud import ProfilingDepCrud
from src.models.task_models import ProfilingDepModel
from src.schemas.base_schemas import OrderingDirection
from src.schemas.task_schemas.primitives.md.task_result import (
    MdTaskResultOrderingField,
)
from src.schemas.task_schemas.primitives.md.types import ColumnMatchMetric
from tests.integration.crud.profiling_dep_crud.md.helpers import make_query_params

pytestmark = pytest.mark.asyncio


async def test_get_many_filter_search(
    md_profiling_dep_crud: ProfilingDepCrud,
    many_md_deps: list[ProfilingDepModel],
) -> None:
    task_id = many_md_deps[0].task_id

    pagination, query_params = make_query_params(search="gamma")
    result = await md_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) == 2
    assert "gamma" in str(result.items[0].result)
    assert result.total_count == 2


async def test_get_many_filter_rhs_item_metrics(
    md_profiling_dep_crud: ProfilingDepCrud,
    many_md_deps: list[ProfilingDepModel],
) -> None:
    task_id = many_md_deps[0].task_id

    pagination, query_params = make_query_params(
        rhs_item_metrics=[ColumnMatchMetric.EQUALITY]
    )
    result = await md_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) >= 1
    assert all(
        r.result.rhs_item.metric == ColumnMatchMetric.EQUALITY  # type: ignore
        for r in result.items
    )
    assert result.total_count >= 1


async def test_get_many_filter_rhs_item_metrics_levenshtein(
    md_profiling_dep_crud: ProfilingDepCrud,
    many_md_deps: list[ProfilingDepModel],
) -> None:
    task_id = many_md_deps[0].task_id

    pagination, query_params = make_query_params(
        rhs_item_metrics=[ColumnMatchMetric.LEVENSHTEIN]
    )
    result = await md_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) == 1
    assert result.items[0].result.rhs_item.metric == ColumnMatchMetric.LEVENSHTEIN  # type: ignore
    assert result.total_count == 1


@pytest.mark.parametrize(
    ("order_by", "direction", "expected_rhs_metric"),
    [
        (
            MdTaskResultOrderingField.RHS_ITEM_METRIC,
            OrderingDirection.ASC,
            ColumnMatchMetric.EQUALITY,
        ),
        (
            MdTaskResultOrderingField.RHS_ITEM_METRIC,
            OrderingDirection.DESC,
            ColumnMatchMetric.MONGE_ELKAN,
        ),
        (
            MdTaskResultOrderingField.NUMBER_OF_LHS_ITEMS,
            OrderingDirection.ASC,
            {ColumnMatchMetric.EQUALITY, ColumnMatchMetric.LEVENSHTEIN},
        ),
        (
            MdTaskResultOrderingField.NUMBER_OF_LHS_ITEMS,
            OrderingDirection.DESC,
            ColumnMatchMetric.EQUALITY,
        ),
    ],
)
async def test_get_many_ordering(
    md_profiling_dep_crud: ProfilingDepCrud,
    many_md_deps: list[ProfilingDepModel],
    order_by: str,
    direction: OrderingDirection,
    expected_rhs_metric: ColumnMatchMetric | set[ColumnMatchMetric],
) -> None:
    task_id = many_md_deps[0].task_id

    pagination, query_params = make_query_params(
        order_by=order_by,
        direction=direction,
    )
    result = await md_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) >= 1
    actual = result.items[0].result.rhs_item.metric  # type: ignore
    if isinstance(expected_rhs_metric, set):
        assert actual in expected_rhs_metric
    else:
        assert actual == expected_rhs_metric
