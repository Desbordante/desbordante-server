"""Helper functions for NAR profiling dep CRUD tests."""

from src.schemas.base_schemas import (
    OrderingDirection,
    PaginationParamsSchema,
)
from src.schemas.base_schemas import OrderingParamsSchema
from src.schemas.task_schemas.base_schemas import TaskResultQueryParamsSchema
from src.schemas.task_schemas.primitives.nar.task_result import (
    NarTaskResultFiltersSchema,
)


def make_nar_result(
    *,
    lhs_items: list[dict],
    rhs_items: list[dict],
    confidence: float,
    support: float,
    fitness: float,
) -> dict:
    """Build a valid NAR result dict for ProfilingDepModel.result."""
    return {
        "lhs_items": lhs_items,
        "rhs_items": rhs_items,
        "confidence": confidence,
        "support": support,
        "fitness": fitness,
    }


def make_query_params(
    *,
    limit: int = 10,
    offset: int = 0,
    search: str | None = None,
    min_confidence: float | None = None,
    max_confidence: float | None = None,
    min_support: float | None = None,
    max_support: float | None = None,
    min_fitness: float | None = None,
    max_fitness: float | None = None,
    lhs_items_names: list[str] | None = None,
    rhs_items_names: list[str] | None = None,
    lhs_items_indices: list[int] | None = None,
    rhs_items_indices: list[int] | None = None,
    order_by: str | None = None,
    direction: OrderingDirection = OrderingDirection.ASC,
) -> tuple[PaginationParamsSchema, TaskResultQueryParamsSchema]:
    pagination = PaginationParamsSchema(limit=limit, offset=offset)
    filters = NarTaskResultFiltersSchema.model_construct(
        search=search or "",
        min_confidence=min_confidence,
        max_confidence=max_confidence,
        min_support=min_support,
        max_support=max_support,
        min_fitness=min_fitness,
        max_fitness=max_fitness,
        lhs_items_names=lhs_items_names,
        rhs_items_names=rhs_items_names,
        lhs_items_indices=lhs_items_indices,
        rhs_items_indices=rhs_items_indices,
    )
    ordering = OrderingParamsSchema(
        order_by=order_by,
        direction=direction,
    )
    query_params = TaskResultQueryParamsSchema[NarTaskResultFiltersSchema](
        filters=filters,
        ordering=ordering,  # type: ignore
    )
    return pagination, query_params  # type: ignore
