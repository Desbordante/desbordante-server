from typing import Literal

from pydantic import BaseModel

from internal.domain.task.value_objects.primitive_name import PrimitiveName
from internal.domain.task.value_objects.ind.algo_config import OneOfIndAlgoConfig
from internal.domain.task.value_objects.ind.algo_result import (  # noqa: F401
    IndAlgoResult,
    IndModel,
)
from internal.domain.task.value_objects.ind.algo_name import IndAlgoName  # noqa: F401


class BaseIndTaskModel(BaseModel):
    primitive_name: Literal[PrimitiveName.ind]


class IndTaskConfig(BaseIndTaskModel):
    config: OneOfIndAlgoConfig


class IndTaskResult(BaseIndTaskModel):
    result: IndAlgoResult
