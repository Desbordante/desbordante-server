"""Helper functions for MD profiling dep CRUD tests."""

from src.schemas.base_schemas import (
    OrderingDirection,
    PaginationParamsSchema,
)
from src.schemas.base_schemas import OrderingParamsSchema
from src.schemas.task_schemas.base_schemas import TaskResultQueryParamsSchema
from src.schemas.task_schemas.primitives.md.task_result import (
    MdTaskResultFiltersSchema,
)
from src.schemas.task_schemas.primitives.md.types import ColumnMatchMetric


def make_md_result(
    *,
    lhs_items: list[dict],
    rhs_item: dict,
) -> dict:
    """Build a valid MD result dict for ProfilingDepModel.result."""
    return {
        "lhs_items": lhs_items,
        "rhs_item": rhs_item,
    }


def make_query_params(
    *,
    limit: int = 10,
    offset: int = 0,
    search: str | None = None,
    lhs_items_metrics: list[ColumnMatchMetric] | None = None,
    rhs_item_metrics: list[ColumnMatchMetric] | None = None,
    show_zeroes: bool | None = None,
    order_by: str | None = None,
    direction: OrderingDirection = OrderingDirection.ASC,
) -> tuple[PaginationParamsSchema, TaskResultQueryParamsSchema]:
    pagination = PaginationParamsSchema(limit=limit, offset=offset)
    filters = MdTaskResultFiltersSchema.model_construct(
        search=search or "",
        lhs_items_metrics=lhs_items_metrics,
        rhs_item_metrics=rhs_item_metrics,
        show_zeroes=show_zeroes,
    )
    ordering = OrderingParamsSchema(
        order_by=order_by,
        direction=direction,
    )
    query_params = TaskResultQueryParamsSchema[MdTaskResultFiltersSchema](
        filters=filters,
        ordering=ordering,  # type: ignore
    )
    return pagination, query_params  # type: ignore
