from typing import Literal

from pydantic import BaseModel

from src.domain.task.value_objects.primitive_name import PrimitiveName
from src.domain.task.value_objects.fd.algo_config import OneOfFdAlgoConfig
from src.domain.task.value_objects.fd.algo_result import (  # noqa: F401
    FdAlgoResult,
    FdModel,
)
from src.domain.task.value_objects.fd.algo_name import FdAlgoName  # noqa: F401
from src.domain.task.value_objects.fd.exception import (  # noqa: F401
    IncorrectFDAlgorithmName,
)


class BaseFdTaskModel(BaseModel):
    primitive_name: Literal[PrimitiveName.fd]


class FdTaskConfig(BaseFdTaskModel):
    config: OneOfFdAlgoConfig


class FdTaskResult(BaseFdTaskModel):
    result: FdAlgoResult
