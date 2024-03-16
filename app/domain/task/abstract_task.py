from typing import Type
from abc import ABC, abstractmethod
from pydantic import BaseModel
from desbordante import Algorithm
import pandas


type AnyAlgo = Algorithm
type AnyConf = BaseModel
type AnyRes = BaseModel


class AbstractTask[Algo: AnyAlgo, Conf: AnyConf, Res: AnyRes](ABC):
    algo: Algo
    config_model_cls: Type[Conf]
    result_model_cls: Type[Res]

    def __init__(self, table: pandas.DataFrame) -> None:
        try:
            self.algo
            self.config_model_cls
            self.result_model_cls
        except AttributeError:
            raise NotImplementedError(
                "algo, config_model_cls and result_model_cls attributes, must be implemented"
            )

        self.table = table
        self.algo.load_data(table=table)

    def execute(self, config: Conf | None = None) -> Res:
        options = config.model_dump(exclude_unset=True) if config else {}
        self.algo.execute(**options)
        return self.collect_result()

    @abstractmethod
    def collect_result(self) -> Res: ...
