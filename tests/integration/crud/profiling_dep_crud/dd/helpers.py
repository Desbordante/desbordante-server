"""Helper functions for DD profiling dep CRUD tests."""

from src.schemas.base_schemas import (
    OrderingDirection,
    PaginationParamsSchema,
)
from src.schemas.base_schemas import OrderingParamsSchema
from src.schemas.task_schemas.base_schemas import TaskResultQueryParamsSchema
from src.schemas.task_schemas.primitives.dd.task_result import (
    DdTaskResultFiltersSchema,
)


def make_dd_result(
    *,
    lhs_items: list[dict],
    rhs_item: dict,
) -> dict:
    """Build a valid DD result dict for ProfilingDepModel.result."""
    return {
        "lhs_items": lhs_items,
        "rhs_item": rhs_item,
    }


def make_query_params(
    *,
    limit: int = 10,
    offset: int = 0,
    search: str | None = None,
    lhs_items_indices: list[int] | None = None,
    lhs_items_names: list[str] | None = None,
    rhs_item_indices: list[int] | None = None,
    rhs_item_names: list[str] | None = None,
    order_by: str | None = None,
    direction: OrderingDirection = OrderingDirection.ASC,
) -> tuple[PaginationParamsSchema, TaskResultQueryParamsSchema]:
    pagination = PaginationParamsSchema(limit=limit, offset=offset)
    filters = DdTaskResultFiltersSchema.model_construct(
        search=search or "",
        lhs_items_indices=lhs_items_indices,
        lhs_items_names=lhs_items_names,
        rhs_item_indices=rhs_item_indices,
        rhs_item_names=rhs_item_names,
    )
    ordering = OrderingParamsSchema(
        order_by=order_by,
        direction=direction,
    )
    query_params = TaskResultQueryParamsSchema[DdTaskResultFiltersSchema](
        filters=filters,
        ordering=ordering,  # type: ignore
    )
    return pagination, query_params  # type: ignore
