from abc import ABC
from typing import Any, Sequence

from sqlalchemy import ColumnElement, ColumnExpressionArgument

from src.models.task_result_models import TaskResultModel


class BaseQueryHelper[O = Any, F = Any](ABC):
    def get_ordering_field(self, order_by: O) -> ColumnElement[TaskResultModel]:
        raise ValueError(
            f"Invalid ordering field {order_by} for {self.__class__.__name__.replace('QueryHelper', '')}"
        )

    def make_filters(
        self, filters: F
    ) -> Sequence[ColumnExpressionArgument[bool] | None]:
        return []
