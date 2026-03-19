"""Helper functions for MFD verification profiling dep CRUD tests."""

from src.schemas.base_schemas import (
    OrderingDirection,
    PaginationParamsSchema,
)
from src.schemas.base_schemas import OrderingParamsSchema
from src.schemas.task_schemas.base_schemas import TaskResultQueryParamsSchema
from src.schemas.task_schemas.primitives.mfd_verification.task_result import (
    MfdVerificationTaskResultFiltersSchema,
)


def make_mfd_verification_result(
    *,
    cluster_index: int,
    lhs_values: list[str],
    max_distance: float,
    highlights: list[dict],
) -> dict:
    """Build a valid MFD verification result dict for ProfilingDepModel.result."""
    return {
        "cluster_index": cluster_index,
        "lhs_values": lhs_values,
        "max_distance": max_distance,
        "highlights": highlights,
    }


def make_query_params(
    *,
    limit: int = 10,
    offset: int = 0,
    search: str | None = None,
    cluster_indices: list[int] | None = None,
    order_by: str | None = None,
    direction: OrderingDirection = OrderingDirection.ASC,
) -> tuple[PaginationParamsSchema, TaskResultQueryParamsSchema]:
    pagination = PaginationParamsSchema(limit=limit, offset=offset)
    filters = MfdVerificationTaskResultFiltersSchema.model_construct(
        search=search or "",
        cluster_indices=cluster_indices,
    )
    ordering = OrderingParamsSchema(
        order_by=order_by,
        direction=direction,
    )
    query_params = TaskResultQueryParamsSchema[MfdVerificationTaskResultFiltersSchema](
        filters=filters,
        ordering=ordering,  # type: ignore
    )
    return pagination, query_params  # type: ignore
