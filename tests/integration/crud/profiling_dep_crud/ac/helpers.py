"""Helper functions for AC profiling dep CRUD tests."""

from src.schemas.base_schemas import (
    OrderingDirection,
    PaginationParamsSchema,
)
from src.schemas.base_schemas import OrderingParamsSchema
from src.schemas.task_schemas.base_schemas import TaskResultQueryParamsSchema
from src.schemas.task_schemas.primitives.ac.task_result import (
    AcTaskResultFiltersSchema,
)


def make_ac_result(
    *,
    lhs_column: dict,
    rhs_column: dict,
    ranges: list[list[float]],
    exceptions: list[dict] | None = None,
) -> dict:
    """Build a valid AC result dict for ProfilingDepModel.result."""
    return {
        "lhs_column": lhs_column,
        "rhs_column": rhs_column,
        "ranges": ranges,
        "exceptions": exceptions or [],
    }


def make_query_params(
    *,
    limit: int = 10,
    offset: int = 0,
    search: str | None = None,
    lhs_column_indices: list[int] | None = None,
    lhs_column_names: list[str] | None = None,
    rhs_column_indices: list[int] | None = None,
    rhs_column_names: list[str] | None = None,
    order_by: str | None = None,
    direction: OrderingDirection = OrderingDirection.ASC,
) -> tuple[PaginationParamsSchema, TaskResultQueryParamsSchema]:
    pagination = PaginationParamsSchema(limit=limit, offset=offset)
    filters = AcTaskResultFiltersSchema.model_construct(
        search=search or "",
        lhs_column_indices=lhs_column_indices,
        lhs_column_names=lhs_column_names,
        rhs_column_indices=rhs_column_indices,
        rhs_column_names=rhs_column_names,
    )
    ordering = OrderingParamsSchema(
        order_by=order_by,
        direction=direction,
    )
    query_params = TaskResultQueryParamsSchema[AcTaskResultFiltersSchema](
        filters=filters,
        ordering=ordering,  # type: ignore
    )
    return pagination, query_params  # type: ignore
