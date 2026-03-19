"""Integration tests for ProfilingDepCrud.get_many (AC primitive)."""

import pytest

from src.crud.profiling_dep_crud.profiling_dep_crud import ProfilingDepCrud
from src.models.task_models import ProfilingDepModel
from src.schemas.base_schemas import OrderingDirection
from src.schemas.task_schemas.primitives.ac.task_result import AcTaskResultOrderingField
from tests.integration.crud.profiling_dep_crud.ac.helpers import make_query_params

pytestmark = pytest.mark.asyncio


async def test_get_many_filter_search(
    ac_profiling_dep_crud: ProfilingDepCrud,
    many_ac_deps: list[ProfilingDepModel],
) -> None:
    task_id = many_ac_deps[0].task_id

    pagination, query_params = make_query_params(search="alpha")
    result = await ac_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) == 1
    assert "alpha" in str(result.items[0].result)
    assert result.total_count == 1


async def test_get_many_filter_rhs_column_names(
    ac_profiling_dep_crud: ProfilingDepCrud,
    many_ac_deps: list[ProfilingDepModel],
) -> None:
    task_id = many_ac_deps[0].task_id

    pagination, query_params = make_query_params(rhs_column_names=["age"])
    result = await ac_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) == 1
    assert result.items[0].result.rhs_column.name == "age"  # type: ignore
    assert result.total_count == 1

    pagination, query_params = make_query_params(rhs_column_names=["delta"])
    result = await ac_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) == 1
    assert result.items[0].result.rhs_column.name == "delta"  # type: ignore
    assert result.total_count == 1


async def test_get_many_filter_rhs_column_indices(
    ac_profiling_dep_crud: ProfilingDepCrud,
    many_ac_deps: list[ProfilingDepModel],
) -> None:
    task_id = many_ac_deps[0].task_id

    pagination, query_params = make_query_params(rhs_column_indices=[3])
    result = await ac_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) == 2
    assert all(r.result.rhs_column.index == 3 for r in result.items)  # type: ignore
    assert result.total_count == 2


async def test_get_many_filter_lhs_column_names(
    ac_profiling_dep_crud: ProfilingDepCrud,
    many_ac_deps: list[ProfilingDepModel],
) -> None:
    task_id = many_ac_deps[0].task_id

    pagination, query_params = make_query_params(lhs_column_names=["name"])
    result = await ac_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) == 1
    assert result.items[0].result.lhs_column.name == "name"  # type: ignore
    assert result.total_count == 1


async def test_get_many_filter_lhs_column_indices(
    ac_profiling_dep_crud: ProfilingDepCrud,
    many_ac_deps: list[ProfilingDepModel],
) -> None:
    task_id = many_ac_deps[0].task_id

    pagination, query_params = make_query_params(lhs_column_indices=[0])
    result = await ac_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) == 3
    assert all(r.result.lhs_column.index == 0 for r in result.items)  # type: ignore
    assert result.total_count == 3


@pytest.mark.parametrize(
    ("order_by", "direction", "expected_rhs_name"),
    [
        (
            AcTaskResultOrderingField.RHS_COLUMN_NAME,
            OrderingDirection.ASC,
            "age",
        ),
        (
            AcTaskResultOrderingField.RHS_COLUMN_NAME,
            OrderingDirection.DESC,
            "score",
        ),
        (
            AcTaskResultOrderingField.NUMBER_OF_RANGES,
            OrderingDirection.ASC,
            {"delta", "score", "email"},
        ),
        (
            AcTaskResultOrderingField.NUMBER_OF_RANGES,
            OrderingDirection.DESC,
            "beta",
        ),
        (
            AcTaskResultOrderingField.NUMBER_OF_EXCEPTIONS,
            OrderingDirection.ASC,
            {"delta", "score"},
        ),
        (
            AcTaskResultOrderingField.NUMBER_OF_EXCEPTIONS,
            OrderingDirection.DESC,
            "email",
        ),
    ],
)
async def test_get_many_ordering(
    ac_profiling_dep_crud: ProfilingDepCrud,
    many_ac_deps: list[ProfilingDepModel],
    order_by: str,
    direction: OrderingDirection,
    expected_rhs_name: str | set[str],
) -> None:
    task_id = many_ac_deps[0].task_id

    pagination, query_params = make_query_params(
        order_by=order_by,
        direction=direction,
    )
    result = await ac_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) >= 1
    actual = result.items[0].result.rhs_column.name  # type: ignore
    if isinstance(expected_rhs_name, set):
        assert actual in expected_rhs_name
    else:
        assert actual == expected_rhs_name
