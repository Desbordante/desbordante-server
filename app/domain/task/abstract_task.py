from typing import Generic, TypeVar, Type
from abc import ABC, abstractmethod
from abcattrs import abstractattrs, Abstract
from pydantic import BaseModel
from desbordante import Algorithm
import pandas

Conf = TypeVar("Conf", bound=BaseModel)
Res = TypeVar("Res", bound=BaseModel)
Algo = TypeVar("Algo", bound=Algorithm)


@abstractattrs
class AbstractTask(Generic[Algo, Conf, Res], ABC):
    algorithm: Abstract[Algo]
    config_model_cls: Abstract[Type[Conf]]
    result_model_cls: Abstract[Type[Res]]

    def __init__(self, table: pandas.DataFrame) -> None:
        super().__init__()
        self.table = table
        self.algorithm.load_data(table=table)

    def execute(self, config: Conf = None) -> Res:
        options = config.model_dump(exclude_unset=True) if config else {}
        self.algorithm.execute(**options)
        return self.collect_result()

    @abstractmethod
    def collect_result(self) -> Res:
        ...
