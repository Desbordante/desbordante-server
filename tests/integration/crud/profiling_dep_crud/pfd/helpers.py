"""Helper functions for PFD profiling dep CRUD tests."""

from src.schemas.base_schemas import (
    OrderingDirection,
    OrderingParamsSchema,
    PaginationParamsSchema,
)
from src.schemas.task_schemas.base_schemas import TaskResultQueryParamsSchema
from src.schemas.task_schemas.primitives.pfd.task_result import (
    PfdTaskResultFiltersSchema,
)


def make_pfd_result(
    *,
    lhs_columns: list[dict],
    rhs_column: dict,
) -> dict:
    """Build a valid PFD result dict for ProfilingDepModel.result."""
    return {
        "lhs_columns": lhs_columns,
        "rhs_column": rhs_column,
    }


def make_query_params(
    *,
    limit: int = 10,
    offset: int = 0,
    search: str | None = None,
    lhs_columns_indices: list[int] | None = None,
    lhs_columns_names: list[str] | None = None,
    rhs_column_indices: list[int] | None = None,
    rhs_column_names: list[str] | None = None,
    order_by: str | None = None,
    direction: OrderingDirection = OrderingDirection.ASC,
) -> tuple[PaginationParamsSchema, TaskResultQueryParamsSchema]:
    pagination = PaginationParamsSchema(limit=limit, offset=offset)
    filters = PfdTaskResultFiltersSchema.model_construct(
        search=search or "",
        lhs_columns_indices=lhs_columns_indices,
        lhs_columns_names=lhs_columns_names,
        rhs_column_indices=rhs_column_indices,
        rhs_column_names=rhs_column_names,
    )
    ordering = OrderingParamsSchema(
        order_by=order_by,
        direction=direction,
    )
    query_params = TaskResultQueryParamsSchema[PfdTaskResultFiltersSchema](
        filters=filters,
        ordering=ordering,  # type: ignore
    )
    return pagination, query_params  # type: ignore
