"""Integration tests for ProfilingDepCrud.get_many (FD verification primitive)."""

import pytest

from src.crud.profiling_dep_crud.profiling_dep_crud import ProfilingDepCrud
from src.models.task_models import ProfilingDepModel
from src.schemas.base_schemas import OrderingDirection
from src.schemas.task_schemas.primitives.fd_verification.task_result import (
    FdVerificationTaskResultOrderingField,
)
from tests.integration.crud.profiling_dep_crud.fd_verification.helpers import (
    make_query_params,
)

pytestmark = pytest.mark.asyncio


async def test_get_many_filter_search(
    fd_verification_profiling_dep_crud: ProfilingDepCrud,
    many_fd_verification_deps: list[ProfilingDepModel],
) -> None:
    task_id = many_fd_verification_deps[0].task_id

    pagination, query_params = make_query_params(search="alpha")
    result = await fd_verification_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) == 1
    assert "alpha" in str(result.items[0].result)
    assert result.total_count == 1


async def test_get_many_filter_min_num(
    fd_verification_profiling_dep_crud: ProfilingDepCrud,
    many_fd_verification_deps: list[ProfilingDepModel],
) -> None:
    task_id = many_fd_verification_deps[0].task_id

    pagination, query_params = make_query_params(min_num=5)
    result = await fd_verification_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) == 3
    assert all(
        r.result.number_of_distinct_rhs_values >= 5
        for r in result.items  # type: ignore
    )
    assert result.total_count == 3


async def test_get_many_filter_max_num(
    fd_verification_profiling_dep_crud: ProfilingDepCrud,
    many_fd_verification_deps: list[ProfilingDepModel],
) -> None:
    task_id = many_fd_verification_deps[0].task_id

    pagination, query_params = make_query_params(max_num=3)
    result = await fd_verification_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) == 2
    assert all(
        r.result.number_of_distinct_rhs_values <= 3
        for r in result.items  # type: ignore
    )
    assert result.total_count == 2


async def test_get_many_filter_min_prop(
    fd_verification_profiling_dep_crud: ProfilingDepCrud,
    many_fd_verification_deps: list[ProfilingDepModel],
) -> None:
    task_id = many_fd_verification_deps[0].task_id

    pagination, query_params = make_query_params(min_prop=0.5)
    result = await fd_verification_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) == 2
    assert all(
        r.result.most_frequent_rhs_value_proportion >= 0.5  # type: ignore
        for r in result.items
    )
    assert result.total_count == 2


async def test_get_many_filter_max_prop(
    fd_verification_profiling_dep_crud: ProfilingDepCrud,
    many_fd_verification_deps: list[ProfilingDepModel],
) -> None:
    task_id = many_fd_verification_deps[0].task_id

    pagination, query_params = make_query_params(max_prop=0.2)
    result = await fd_verification_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) == 2
    assert all(
        r.result.most_frequent_rhs_value_proportion <= 0.2  # type: ignore
        for r in result.items
    )
    assert result.total_count == 2


@pytest.mark.parametrize(
    ("order_by", "direction", "expected_num"),
    [
        (
            FdVerificationTaskResultOrderingField.NUMBER_OF_DISTINCT_RHS_VALUES,
            OrderingDirection.ASC,
            2,
        ),
        (
            FdVerificationTaskResultOrderingField.NUMBER_OF_DISTINCT_RHS_VALUES,
            OrderingDirection.DESC,
            10,
        ),
        (
            FdVerificationTaskResultOrderingField.MOST_FREQUENT_RHS_VALUE_PROPORTION,
            OrderingDirection.ASC,
            0.1,
        ),
        (
            FdVerificationTaskResultOrderingField.MOST_FREQUENT_RHS_VALUE_PROPORTION,
            OrderingDirection.DESC,
            0.9,
        ),
        (
            FdVerificationTaskResultOrderingField.NUMBER_OF_ROWS,
            OrderingDirection.ASC,
            1,
        ),
        (
            FdVerificationTaskResultOrderingField.NUMBER_OF_ROWS,
            OrderingDirection.DESC,
            3,
        ),
    ],
)
async def test_get_many_ordering(
    fd_verification_profiling_dep_crud: ProfilingDepCrud,
    many_fd_verification_deps: list[ProfilingDepModel],
    order_by: str,
    direction: OrderingDirection,
    expected_num: int | float,
) -> None:
    task_id = many_fd_verification_deps[0].task_id

    pagination, query_params = make_query_params(
        order_by=order_by,
        direction=direction,
    )
    result = await fd_verification_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) >= 1
    first = result.items[0].result  # type: ignore
    if order_by == FdVerificationTaskResultOrderingField.NUMBER_OF_DISTINCT_RHS_VALUES:
        assert first.number_of_distinct_rhs_values == expected_num
    elif (
        order_by
        == FdVerificationTaskResultOrderingField.MOST_FREQUENT_RHS_VALUE_PROPORTION
    ):
        assert first.most_frequent_rhs_value_proportion == expected_num
    else:
        assert len(first.rows) == expected_num
