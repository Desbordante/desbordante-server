from typing import Literal

from pydantic import BaseModel

from src.domain.task.value_objects.afd.algo_config import OneOfAfdConfig
from src.domain.task.value_objects.afd.algo_name import AfdAlgoName  # noqa: F401
from src.domain.task.value_objects.afd.algo_result import (  # noqa: F401
    AfdAlgoResult,
    FdModel,
)
from src.domain.task.value_objects.afd.exception import (  # noqa: F401
    IncorrectAFDAlgorithmName,
)
from src.domain.task.value_objects.primitive_name import PrimitiveName


class BaseAfdTaskModel(BaseModel):
    primitive_name: Literal[PrimitiveName.afd]


class AfdTaskConfig(BaseAfdTaskModel):
    config: OneOfAfdConfig


class AfdTaskResult(BaseAfdTaskModel):
    result: AfdAlgoResult
