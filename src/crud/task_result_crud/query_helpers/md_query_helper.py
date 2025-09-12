from sqlalchemy import (
    cast,
    column,
    func,
    or_,
)
from sqlalchemy.dialects.postgresql import JSONPATH

from src.crud.task_result_crud.query_helpers.base_query_helper import BaseQueryHelper
from src.models.task_result_models import TaskResultModel
from src.schemas.task_schemas.primitives.md.task_result import (
    MdTaskResultFiltersSchema,
    MdTaskResultOrderingField,
)


class MdQueryHelper(
    BaseQueryHelper[MdTaskResultOrderingField, MdTaskResultFiltersSchema]
):
    def get_ordering_field(self, order_by: MdTaskResultOrderingField):
        match order_by:
            case MdTaskResultOrderingField.NumberOfLhs:
                return func.jsonb_array_length(
                    TaskResultModel.result[MdTaskResultOrderingField.Lhs]
                )
            case MdTaskResultOrderingField.NumberOfRhs:
                return func.jsonb_array_length(
                    TaskResultModel.result[MdTaskResultOrderingField.Rhs]
                )
            case MdTaskResultOrderingField.Lhs:
                return TaskResultModel.result[order_by].astext
            case MdTaskResultOrderingField.Rhs:
                return TaskResultModel.result[order_by].astext

        super().get_ordering_field(order_by)

    def make_filters(self, filters: MdTaskResultFiltersSchema):
        return [
            # search
            or_(
                TaskResultModel.result[MdTaskResultOrderingField.Lhs].astext.icontains(
                    filters.search
                ),
                TaskResultModel.result[MdTaskResultOrderingField.Rhs].astext.icontains(
                    filters.search
                ),
            )
            if filters.search
            else None,
            or_(
                func.jsonb_array_length(column("result").op("->")("lhs")) > 0,
                func.jsonb_array_length(column("result").op("->")("rhs")) > 0,
            )
            if filters.metrics
            else None,
        ]

    def get_filtered_result_column(self, filters: MdTaskResultFiltersSchema):
        conditions = [
            "@.boundary != 0" if not filters.show_zeroes else None,
            (
                f"({' || '.join([f'@.metrics == "{metric}"' for metric in filters.metrics])})"
            )
            if filters.metrics
            else None,
        ]
        conditions = [c for c in conditions if c is not None]

        if not conditions:
            return super().get_filtered_result_column(filters)

        condition = cast(
            f"$[*] ? ({' && '.join(conditions)})",
            JSONPATH,
        )

        return func.jsonb_build_object(
            "lhs",
            func.jsonb_path_query_array(
                TaskResultModel.result["lhs"],
                condition,
            ),
            "rhs",
            func.jsonb_path_query_array(
                TaskResultModel.result["rhs"],
                condition,
            ),
        )
