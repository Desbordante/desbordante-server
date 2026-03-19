"""Integration tests for ProfilingDepCrud.get_many (PFD primitive)."""

import pytest

from src.crud.profiling_dep_crud.profiling_dep_crud import ProfilingDepCrud
from src.models.task_models import ProfilingDepModel
from src.schemas.base_schemas import OrderingDirection
from src.schemas.task_schemas.primitives.pfd.task_result import (
    PfdTaskResultOrderingField,
)
from tests.integration.crud.profiling_dep_crud.pfd.helpers import make_query_params

pytestmark = pytest.mark.asyncio


async def test_get_many_filter_search(
    pfd_profiling_dep_crud: ProfilingDepCrud,
    many_pfd_deps: list[ProfilingDepModel],
) -> None:
    task_id = many_pfd_deps[0].task_id

    pagination, query_params = make_query_params(search="alpha")
    result = await pfd_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) == 1
    assert "alpha" in str(result.items[0].result)
    assert result.total_count == 1

    pagination, query_params = make_query_params(search="name")
    result = await pfd_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) >= 1
    assert result.total_count >= 1


async def test_get_many_filter_rhs_column_names(
    pfd_profiling_dep_crud: ProfilingDepCrud,
    many_pfd_deps: list[ProfilingDepModel],
) -> None:
    task_id = many_pfd_deps[0].task_id

    pagination, query_params = make_query_params(rhs_column_names=["age"])
    result = await pfd_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) == 1
    assert result.items[0].result.rhs_column.name == "age"  # type: ignore
    assert result.total_count == 1

    pagination, query_params = make_query_params(rhs_column_names=["delta"])
    result = await pfd_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) == 1
    assert result.items[0].result.rhs_column.name == "delta"  # type: ignore
    assert result.total_count == 1


async def test_get_many_filter_rhs_column_indices(
    pfd_profiling_dep_crud: ProfilingDepCrud,
    many_pfd_deps: list[ProfilingDepModel],
) -> None:
    task_id = many_pfd_deps[0].task_id

    pagination, query_params = make_query_params(rhs_column_indices=[3])
    result = await pfd_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) == 2
    assert all(r.result.rhs_column.index == 3 for r in result.items)  # type: ignore
    assert result.total_count == 2


async def test_get_many_filter_lhs_columns_names(
    pfd_profiling_dep_crud: ProfilingDepCrud,
    many_pfd_deps: list[ProfilingDepModel],
) -> None:
    task_id = many_pfd_deps[0].task_id

    pagination, query_params = make_query_params(
        lhs_columns_names=["name", "email"],
    )
    result = await pfd_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) >= 1
    lhs_names = [c.name for c in result.items[0].result.lhs_columns]  # type: ignore
    assert set(lhs_names).issubset({"name", "email"})
    assert result.total_count >= 1


async def test_get_many_filter_lhs_columns_indices(
    pfd_profiling_dep_crud: ProfilingDepCrud,
    many_pfd_deps: list[ProfilingDepModel],
) -> None:
    task_id = many_pfd_deps[0].task_id

    pagination, query_params = make_query_params(lhs_columns_indices=[0])
    result = await pfd_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) >= 1
    lhs_indices = [c.index for c in result.items[0].result.lhs_columns]  # type: ignore
    assert set(lhs_indices).issubset({0})
    assert result.total_count >= 1


@pytest.mark.parametrize(
    ("order_by", "direction", "expected_rhs_name"),
    [
        (
            PfdTaskResultOrderingField.RHS_COLUMN_NAME,
            OrderingDirection.ASC,
            "age",
        ),
        (
            PfdTaskResultOrderingField.RHS_COLUMN_NAME,
            OrderingDirection.DESC,
            "name",
        ),
        (
            PfdTaskResultOrderingField.NUMBER_OF_LHS_COLUMNS,
            OrderingDirection.DESC,
            "age",
        ),
    ],
)
async def test_get_many_ordering(
    pfd_profiling_dep_crud: ProfilingDepCrud,
    many_pfd_deps: list[ProfilingDepModel],
    order_by: str,
    direction: OrderingDirection,
    expected_rhs_name: str,
) -> None:
    task_id = many_pfd_deps[0].task_id

    pagination, query_params = make_query_params(
        order_by=order_by,
        direction=direction,
    )
    result = await pfd_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) >= 1
    assert result.items[0].result.rhs_column.name == expected_rhs_name  # type: ignore
