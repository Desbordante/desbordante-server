from typing import Literal

from pydantic import BaseModel

from internal.domain.task.value_objects.primitive_name import PrimitiveName
from internal.domain.task.value_objects.fd.algo_config import OneOfFdAlgoConfig
from internal.domain.task.value_objects.fd.algo_result import FdAlgoResult, FdModel
from internal.domain.task.value_objects.fd.algo_name import FdAlgoName


class BaseFdTaskModel(BaseModel):
    primitive_name: Literal[PrimitiveName.fd]


class FdTaskConfig(BaseFdTaskModel):
    config: OneOfFdAlgoConfig


class FdTaskResult(BaseFdTaskModel):
    result: FdAlgoResult
