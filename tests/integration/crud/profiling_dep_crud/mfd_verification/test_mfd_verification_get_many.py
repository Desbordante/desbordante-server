"""Integration tests for ProfilingDepCrud.get_many (MFD verification primitive)."""

import pytest

from src.crud.profiling_dep_crud.profiling_dep_crud import ProfilingDepCrud
from src.models.task_models import ProfilingDepModel
from src.schemas.base_schemas import OrderingDirection
from src.schemas.task_schemas.primitives.mfd_verification.task_result import (
    MfdVerificationTaskResultOrderingField,
)
from tests.integration.crud.profiling_dep_crud.mfd_verification.helpers import (
    make_query_params,
)

pytestmark = pytest.mark.asyncio


async def test_get_many_filter_search(
    mfd_verification_profiling_dep_crud: ProfilingDepCrud,
    many_mfd_verification_deps: list[ProfilingDepModel],
) -> None:
    task_id = many_mfd_verification_deps[0].task_id

    pagination, query_params = make_query_params(search="alpha")
    result = await mfd_verification_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) == 2
    assert "alpha" in str(result.items[0].result)
    assert result.total_count == 2


async def test_get_many_filter_cluster_indices(
    mfd_verification_profiling_dep_crud: ProfilingDepCrud,
    many_mfd_verification_deps: list[ProfilingDepModel],
) -> None:
    task_id = many_mfd_verification_deps[0].task_id

    pagination, query_params = make_query_params(cluster_indices=[0])
    result = await mfd_verification_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) == 2
    assert all(
        r.result.cluster_index == 0
        for r in result.items  # type: ignore
    )
    assert result.total_count == 2


async def test_get_many_filter_cluster_indices_multiple(
    mfd_verification_profiling_dep_crud: ProfilingDepCrud,
    many_mfd_verification_deps: list[ProfilingDepModel],
) -> None:
    task_id = many_mfd_verification_deps[0].task_id

    pagination, query_params = make_query_params(cluster_indices=[1, 3])
    result = await mfd_verification_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) == 2
    assert all(
        r.result.cluster_index in (1, 3)
        for r in result.items  # type: ignore
    )
    assert result.total_count == 2


@pytest.mark.parametrize(
    ("order_by", "direction", "expected_cluster_index"),
    [
        (
            MfdVerificationTaskResultOrderingField.CLUSTER_INDEX,
            OrderingDirection.ASC,
            0,
        ),
        (
            MfdVerificationTaskResultOrderingField.CLUSTER_INDEX,
            OrderingDirection.DESC,
            3,
        ),
        (
            MfdVerificationTaskResultOrderingField.MAX_DISTANCE,
            OrderingDirection.ASC,
            0.5,
        ),
        (
            MfdVerificationTaskResultOrderingField.MAX_DISTANCE,
            OrderingDirection.DESC,
            3.0,
        ),
        (
            MfdVerificationTaskResultOrderingField.LHS_VALUES,
            OrderingDirection.ASC,
            "alpha",
        ),
    ],
)
async def test_get_many_ordering(
    mfd_verification_profiling_dep_crud: ProfilingDepCrud,
    many_mfd_verification_deps: list[ProfilingDepModel],
    order_by: str,
    direction: OrderingDirection,
    expected_cluster_index: int | float | str,
) -> None:
    task_id = many_mfd_verification_deps[0].task_id

    pagination, query_params = make_query_params(
        order_by=order_by,
        direction=direction,
    )
    result = await mfd_verification_profiling_dep_crud.get_many(
        pagination=pagination,
        query_params=query_params,
        task_id=task_id,
    )

    assert len(result.items) >= 1
    first = result.items[0].result  # type: ignore
    if order_by == MfdVerificationTaskResultOrderingField.CLUSTER_INDEX:
        assert first.cluster_index == expected_cluster_index
    elif order_by == MfdVerificationTaskResultOrderingField.MAX_DISTANCE:
        assert first.max_distance == expected_cluster_index
    else:
        assert first.lhs_values[0] == expected_cluster_index
