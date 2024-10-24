from typing import Literal

from pydantic import BaseModel

from internal.domain.task.value_objects.primitive_name import PrimitiveName
from internal.domain.task.value_objects.ac.algo_config import OneOfAcAlgoConfig
from internal.domain.task.value_objects.ac.algo_result import (  # noqa: F401
    AcAlgoResult,
    AcModel,
    AcExceptionModel,
)
from internal.domain.task.value_objects.ac.algo_name import AcAlgoName  # noqa: F401


class BaseAcTaskModel(BaseModel):
    primitive_name: Literal[PrimitiveName.ac]


class AcTaskConfig(BaseAcTaskModel):
    config: OneOfAcAlgoConfig


class AcTaskResult(BaseAcTaskModel):
    result: AcAlgoResult
