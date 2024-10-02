from typing import Literal

from pydantic import BaseModel

from internal.domain.task.value_objects.afd.algo_config import OneOfAfdConfig
from internal.domain.task.value_objects.afd.algo_result import (  # noqa: F401
    AfdAlgoResult,
    FdModel,
)
from internal.domain.task.value_objects.afd.algo_name import AfdAlgoName  # noqa: F401
from internal.domain.task.value_objects.primitive_name import PrimitiveName
from internal.domain.task.value_objects.afd.exception import (  # noqa: F401
    IncorrectAFDAlgorithmName,
)


class BaseAfdTaskModel(BaseModel):
    primitive_name: Literal[PrimitiveName.afd]


class AfdTaskConfig(BaseAfdTaskModel):
    config: OneOfAfdConfig


class AfdTaskResult(BaseAfdTaskModel):
    result: AfdAlgoResult
