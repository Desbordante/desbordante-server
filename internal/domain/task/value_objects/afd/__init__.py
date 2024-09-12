from typing import Literal

from pydantic import BaseModel

from internal.domain.task.value_objects.afd.algo_config import OneOfAfdConfig
from internal.domain.task.value_objects.afd.algo_result import AfdAlgoResult, FdModel
from internal.domain.task.value_objects.afd.algo_name import AfdAlgoName
from internal.domain.task.value_objects.primitive_name import PrimitiveName


class BaseAfdTaskModel(BaseModel):
    primitive_name: Literal[PrimitiveName.afd]


class AfdTaskConfig(BaseAfdTaskModel):
    config: OneOfAfdConfig


class AfdTaskResult(BaseAfdTaskModel):
    result: AfdAlgoResult
