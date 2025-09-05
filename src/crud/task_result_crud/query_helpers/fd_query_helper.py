import sqlalchemy
from sqlalchemy import func, or_

from src.crud.task_result_crud.query_helpers.base_query_helper import BaseQueryHelper
from src.models.task_result_models import TaskResultModel
from src.schemas.task_schemas.fd.task_result import (
    FdTaskResultFiltersSchema,
    FdTaskResultOrderingField,
)


class FdQueryHelper(
    BaseQueryHelper[FdTaskResultOrderingField, FdTaskResultFiltersSchema]
):
    def get_ordering_field(self, order_by: FdTaskResultOrderingField):
        match order_by:
            case FdTaskResultOrderingField.LhsIndices:
                return TaskResultModel.result[order_by].astext
            case FdTaskResultOrderingField.LhsNames:
                return TaskResultModel.result[order_by].astext
            case FdTaskResultOrderingField.RhsIndex:
                return func.cast(
                    TaskResultModel.result[order_by].astext, sqlalchemy.Integer
                )
            case FdTaskResultOrderingField.RhsName:
                return TaskResultModel.result[order_by].astext

        super().get_ordering_field(order_by)

    def make_filters(self, filters: FdTaskResultFiltersSchema):
        return [
            or_(
                TaskResultModel.result[
                    FdTaskResultOrderingField.LhsNames
                ].astext.icontains(filters.search),
                TaskResultModel.result[
                    FdTaskResultOrderingField.RhsName
                ].astext.icontains(filters.search),
            )
            if filters.search
            else None,
            # lhs indices
            TaskResultModel.result[FdTaskResultOrderingField.LhsIndices].op("@>")(
                filters.lhs_indices
            )
            if filters.lhs_indices
            else None,
            # lhs names
            TaskResultModel.result[FdTaskResultOrderingField.LhsNames].op("@>")(
                filters.lhs_names
            )
            if filters.lhs_names
            else None,
            # rhs index
            TaskResultModel.result[FdTaskResultOrderingField.RhsIndex].astext
            == str(filters.rhs_index)
            if filters.rhs_index is not None
            else None,
            # rhs name
            TaskResultModel.result[FdTaskResultOrderingField.RhsName].astext
            == filters.rhs_name
            if filters.rhs_name
            else None,
        ]
