from typing import Literal

from pydantic import BaseModel

from internal.domain.task.value_objects.primitive_name import PrimitiveName
from internal.domain.task.value_objects.aind.algo_config import OneOfAindAlgoConfig
from internal.domain.task.value_objects.aind.algo_result import (  # noqa: F401
    AindAlgoResult,
    AindModel,
)
from internal.domain.task.value_objects.aind.algo_name import AindAlgoName  # noqa: F401


class BaseAindTaskModel(BaseModel):
    primitive_name: Literal[PrimitiveName.aind]


class AindTaskConfig(BaseAindTaskModel):
    config: OneOfAindAlgoConfig


class AindTaskResult(BaseAindTaskModel):
    result: AindAlgoResult
