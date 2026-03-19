"""Helper functions for FD verification profiling dep CRUD tests."""

from src.schemas.base_schemas import (
    OrderingDirection,
    PaginationParamsSchema,
)
from src.schemas.base_schemas import OrderingParamsSchema
from src.schemas.task_schemas.base_schemas import TaskResultQueryParamsSchema
from src.schemas.task_schemas.primitives.fd_verification.task_result import (
    FdVerificationTaskResultFiltersSchema,
)


def make_fd_verification_result(
    *,
    number_of_distinct_rhs_values: int,
    most_frequent_rhs_value_proportion: float,
    rows: list[dict],
) -> dict:
    """Build a valid FD verification result dict for ProfilingDepModel.result."""
    return {
        "number_of_distinct_rhs_values": number_of_distinct_rhs_values,
        "most_frequent_rhs_value_proportion": most_frequent_rhs_value_proportion,
        "rows": rows,
    }


def make_query_params(
    *,
    limit: int = 10,
    offset: int = 0,
    search: str | None = None,
    min_num: int | None = None,
    max_num: int | None = None,
    min_prop: float | None = None,
    max_prop: float | None = None,
    order_by: str | None = None,
    direction: OrderingDirection = OrderingDirection.ASC,
) -> tuple[PaginationParamsSchema, TaskResultQueryParamsSchema]:
    pagination = PaginationParamsSchema(limit=limit, offset=offset)
    filters = FdVerificationTaskResultFiltersSchema.model_construct(
        search=search or "",
        min_num=min_num,
        max_num=max_num,
        min_prop=min_prop,
        max_prop=max_prop,
    )
    ordering = OrderingParamsSchema(
        order_by=order_by,
        direction=direction,
    )
    query_params = TaskResultQueryParamsSchema[FdVerificationTaskResultFiltersSchema](
        filters=filters,
        ordering=ordering,  # type: ignore
    )
    return pagination, query_params  # type: ignore
