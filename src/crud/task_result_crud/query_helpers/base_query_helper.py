from abc import ABC, abstractmethod

from sqlalchemy import ColumnElement

from src.models.task_result_models import TaskResultModel


class BaseQueryHelper[O](ABC):
    @abstractmethod
    def get_ordering_field(self, order_by: O) -> ColumnElement[TaskResultModel]:
        raise ValueError(
            f"Invalid ordering field {order_by} for {self.__class__.__name__.replace('QueryHelper', '')}"
        )
