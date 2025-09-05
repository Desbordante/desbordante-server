import sqlalchemy
from sqlalchemy import func, or_

from src.crud.task_result_crud.query_helpers.base_query_helper import BaseQueryHelper
from src.models.task_result_models import TaskResultModel
from src.schemas.task_schemas.afd.task_result import (
    AfdTaskResultFiltersSchema,
    AfdTaskResultOrderingField,
)


class AfdQueryHelper(
    BaseQueryHelper[AfdTaskResultOrderingField, AfdTaskResultFiltersSchema]
):
    def get_ordering_field(self, order_by: AfdTaskResultOrderingField):
        match order_by:
            case AfdTaskResultOrderingField.LhsIndices:
                return TaskResultModel.result[order_by].astext
            case AfdTaskResultOrderingField.LhsNames:
                return TaskResultModel.result[order_by].astext
            case AfdTaskResultOrderingField.RhsIndex:
                return func.cast(
                    TaskResultModel.result[order_by].astext, sqlalchemy.Integer
                )
            case AfdTaskResultOrderingField.RhsName:
                return TaskResultModel.result[order_by].astext

        super().get_ordering_field(order_by)

    def make_filters(self, filters: AfdTaskResultFiltersSchema):
        return [
            or_(
                TaskResultModel.result[
                    AfdTaskResultOrderingField.LhsNames
                ].astext.icontains(filters.search),
                TaskResultModel.result[
                    AfdTaskResultOrderingField.RhsName
                ].astext.icontains(filters.search),
            )
            if filters.search
            else None,
            # lhs indices
            TaskResultModel.result[AfdTaskResultOrderingField.LhsIndices].op("@>")(
                filters.lhs_indices
            )
            if filters.lhs_indices
            else None,
            # lhs names
            TaskResultModel.result[AfdTaskResultOrderingField.LhsNames].op("@>")(
                filters.lhs_names
            )
            if filters.lhs_names
            else None,
            # rhs index
            TaskResultModel.result[AfdTaskResultOrderingField.RhsIndex].astext
            == str(filters.rhs_index)
            if filters.rhs_index is not None
            else None,
            # rhs name
            TaskResultModel.result[AfdTaskResultOrderingField.RhsName].astext
            == filters.rhs_name
            if filters.rhs_name
            else None,
        ]
