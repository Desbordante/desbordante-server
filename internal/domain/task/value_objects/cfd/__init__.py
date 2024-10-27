from typing import Literal

from pydantic import BaseModel

from internal.domain.task.value_objects.primitive_name import PrimitiveName
from internal.domain.task.value_objects.cfd.algo_config import OneOfCfdAlgoConfig
from internal.domain.task.value_objects.cfd.algo_result import (  # noqa: F401
    CfdAlgoResult,
    CfdModel,
)
from internal.domain.task.value_objects.cfd.algo_name import CfdAlgoName  # noqa: F401


class BaseCfdTaskModel(BaseModel):
    primitive_name: Literal[PrimitiveName.cfd]


class CfdTaskConfig(BaseCfdTaskModel):
    config: OneOfCfdAlgoConfig


class CfdTaskResult(BaseCfdTaskModel):
    result: CfdAlgoResult
