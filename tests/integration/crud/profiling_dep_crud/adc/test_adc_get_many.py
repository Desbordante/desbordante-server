"""Integration tests for ProfilingDepCrud.get_many (ADC primitive)."""

import pytest

from src.crud.profiling_dep_crud.profiling_dep_crud import ProfilingDepCrud
from src.models.task_models import ProfilingDepModel
from src.schemas.base_schemas import OrderingDirection
from src.schemas.task_schemas.primitives.adc.task_result import (
    AdcTaskResultOrderingField,
)
from tests.integration.crud.profiling_dep_crud.adc.helpers import make_query_params

pytestmark = pytest.mark.asyncio


async def test_get_many_filter_search(
    adc_profiling_dep_crud: ProfilingDepCrud,
    many_adc_deps: list[ProfilingDepModel],
) -> None:
    task_id = many_adc_deps[0].task_id

    pagination, query_params = make_query_params(search="alpha")
    result = await adc_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) == 1
    assert "alpha" in str(result.items[0].result)
    assert result.total_count == 1


async def test_get_many_filter_rhs_item_names(
    adc_profiling_dep_crud: ProfilingDepCrud,
    many_adc_deps: list[ProfilingDepModel],
) -> None:
    task_id = many_adc_deps[0].task_id

    pagination, query_params = make_query_params(rhs_item_names=["age"])
    result = await adc_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) == 1
    assert result.items[0].result.conjuncts[0].rhs_item.name == "age"  # type: ignore
    assert result.total_count == 1

    pagination, query_params = make_query_params(rhs_item_names=["delta"])
    result = await adc_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) == 1
    assert result.total_count == 1


async def test_get_many_filter_rhs_item_indices(
    adc_profiling_dep_crud: ProfilingDepCrud,
    many_adc_deps: list[ProfilingDepModel],
) -> None:
    task_id = many_adc_deps[0].task_id

    pagination, query_params = make_query_params(rhs_item_indices=[3])
    result = await adc_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) == 2
    assert all(
        r.result.conjuncts[0].rhs_item.index == 3
        for r in result.items  # type: ignore
    )
    assert result.total_count == 2


async def test_get_many_filter_lhs_item_names(
    adc_profiling_dep_crud: ProfilingDepCrud,
    many_adc_deps: list[ProfilingDepModel],
) -> None:
    task_id = many_adc_deps[0].task_id

    pagination, query_params = make_query_params(lhs_item_names=["name"])
    result = await adc_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) == 1
    assert result.items[0].result.conjuncts[0].lhs_item.name == "name"  # type: ignore
    assert result.total_count == 1


async def test_get_many_filter_lhs_item_indices(
    adc_profiling_dep_crud: ProfilingDepCrud,
    many_adc_deps: list[ProfilingDepModel],
) -> None:
    task_id = many_adc_deps[0].task_id

    pagination, query_params = make_query_params(lhs_item_indices=[0])
    result = await adc_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) == 2
    assert all(
        r.result.conjuncts[0].lhs_item.index == 0
        for r in result.items  # type: ignore
    )
    assert result.total_count == 2


@pytest.mark.parametrize(
    ("order_by", "direction", "expected_rhs_name"),
    [
        (
            AdcTaskResultOrderingField.RHS_ITEM_NAMES,
            OrderingDirection.ASC,
            "age",
        ),
        (
            AdcTaskResultOrderingField.RHS_ITEM_NAMES,
            OrderingDirection.DESC,
            {"beta", "score"},
        ),
        (
            AdcTaskResultOrderingField.NUMBER_OF_CONJUNCTS,
            OrderingDirection.ASC,
            {"age", "score", "delta", "email"},
        ),
        (
            AdcTaskResultOrderingField.NUMBER_OF_CONJUNCTS,
            OrderingDirection.DESC,
            "beta",
        ),
    ],
)
async def test_get_many_ordering(
    adc_profiling_dep_crud: ProfilingDepCrud,
    many_adc_deps: list[ProfilingDepModel],
    order_by: str,
    direction: OrderingDirection,
    expected_rhs_name: str | set[str],
) -> None:
    task_id = many_adc_deps[0].task_id

    pagination, query_params = make_query_params(
        order_by=order_by,
        direction=direction,
    )
    result = await adc_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) >= 1
    actual = result.items[0].result.conjuncts[0].rhs_item.name  # type: ignore
    if isinstance(expected_rhs_name, set):
        assert actual in expected_rhs_name
    else:
        assert actual == expected_rhs_name
