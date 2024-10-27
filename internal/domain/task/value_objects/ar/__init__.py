from typing import Literal

from pydantic import BaseModel

from internal.domain.task.value_objects.primitive_name import PrimitiveName
from internal.domain.task.value_objects.ar.algo_config import OneOfArAlgoConfig
from internal.domain.task.value_objects.ar.algo_result import (  # noqa: F401
    ArAlgoResult,
    ArModel,
)
from internal.domain.task.value_objects.ar.algo_name import ArAlgoName  # noqa: F401


class BaseArTaskModel(BaseModel):
    primitive_name: Literal[PrimitiveName.ar]


class ArTaskConfig(BaseArTaskModel):
    config: OneOfArAlgoConfig


class ArTaskResult(BaseArTaskModel):
    result: ArAlgoResult
