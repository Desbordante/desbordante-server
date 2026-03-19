"""Helper functions for ADC profiling dep CRUD tests."""

from src.schemas.base_schemas import (
    OrderingDirection,
    PaginationParamsSchema,
)
from src.schemas.base_schemas import OrderingParamsSchema
from src.schemas.task_schemas.base_schemas import TaskResultQueryParamsSchema
from src.schemas.task_schemas.primitives.adc.task_result import (
    AdcTaskResultFiltersSchema,
)


def make_adc_result(
    *,
    conjuncts: list[dict],
) -> dict:
    """Build a valid ADC result dict for ProfilingDepModel.result."""
    return {"conjuncts": conjuncts}


def make_query_params(
    *,
    limit: int = 10,
    offset: int = 0,
    search: str | None = None,
    lhs_item_indices: list[int] | None = None,
    lhs_item_names: list[str] | None = None,
    rhs_item_indices: list[int] | None = None,
    rhs_item_names: list[str] | None = None,
    order_by: str | None = None,
    direction: OrderingDirection = OrderingDirection.ASC,
) -> tuple[PaginationParamsSchema, TaskResultQueryParamsSchema]:
    pagination = PaginationParamsSchema(limit=limit, offset=offset)
    filters = AdcTaskResultFiltersSchema.model_construct(
        search=search or "",
        lhs_item_indices=lhs_item_indices,
        lhs_item_names=lhs_item_names,
        rhs_item_indices=rhs_item_indices,
        rhs_item_names=rhs_item_names,
    )
    ordering = OrderingParamsSchema(
        order_by=order_by,
        direction=direction,
    )
    query_params = TaskResultQueryParamsSchema[AdcTaskResultFiltersSchema](
        filters=filters,
        ordering=ordering,  # type: ignore
    )
    return pagination, query_params  # type: ignore
