"""Helper functions for AR profiling dep CRUD tests."""

from src.schemas.base_schemas import (
    OrderingDirection,
    PaginationParamsSchema,
)
from src.schemas.base_schemas import OrderingParamsSchema
from src.schemas.task_schemas.base_schemas import TaskResultQueryParamsSchema
from src.schemas.task_schemas.primitives.ar.task_result import (
    ArTaskResultFiltersSchema,
)


def make_ar_result(
    *,
    lhs_values: list[str],
    rhs_values: list[str],
    support: float,
    confidence: float,
) -> dict:
    """Build a valid AR result dict for ProfilingDepModel.result."""
    return {
        "lhs_values": lhs_values,
        "rhs_values": rhs_values,
        "support": support,
        "confidence": confidence,
    }


def make_query_params(
    *,
    limit: int = 10,
    offset: int = 0,
    search: str | None = None,
    lhs_values: list[str] | None = None,
    rhs_values: list[str] | None = None,
    min_support: float | None = None,
    max_support: float | None = None,
    min_confidence: float | None = None,
    max_confidence: float | None = None,
    order_by: str | None = None,
    direction: OrderingDirection = OrderingDirection.ASC,
) -> tuple[PaginationParamsSchema, TaskResultQueryParamsSchema]:
    pagination = PaginationParamsSchema(limit=limit, offset=offset)
    filters = ArTaskResultFiltersSchema.model_construct(
        search=search or "",
        lhs_values=lhs_values,
        rhs_values=rhs_values,
        min_support=min_support,
        max_support=max_support,
        min_confidence=min_confidence,
        max_confidence=max_confidence,
    )
    ordering = OrderingParamsSchema(
        order_by=order_by,
        direction=direction,
    )
    query_params = TaskResultQueryParamsSchema[ArTaskResultFiltersSchema](
        filters=filters,
        ordering=ordering,  # type: ignore
    )
    return pagination, query_params  # type: ignore
