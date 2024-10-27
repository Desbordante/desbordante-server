from typing import Literal

from pydantic import BaseModel

from internal.domain.task.value_objects.primitive_name import PrimitiveName
from internal.domain.task.value_objects.dd.algo_config import OneOfDdAlgoConfig
from internal.domain.task.value_objects.dd.algo_result import (  # noqa: F401
    DdAlgoResult,
    DdModel,
)
from internal.domain.task.value_objects.dd.algo_name import DdAlgoName  # noqa: F401


class BaseDdTaskModel(BaseModel):
    primitive_name: Literal[PrimitiveName.dd]


class DdTaskConfig(BaseDdTaskModel):
    config: OneOfDdAlgoConfig


class DdTaskResult(BaseDdTaskModel):
    result: DdAlgoResult
