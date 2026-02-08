from typing import Literal

from src.schemas.base_schemas import BaseSchema
from src.schemas.task_schemas.primitives.fd.config import OneOfFdAlgoConfig
from src.schemas.task_schemas.primitives.fd.result import FdAlgoResult
from src.schemas.task_schemas.types import PrimitiveName


class BaseFdTaskModel(BaseSchema):
    primitive_name: Literal[PrimitiveName.fd]


class FdTaskConfig(BaseFdTaskModel):
    config: OneOfFdAlgoConfig


class FdTaskResult(BaseFdTaskModel):
    result: FdAlgoResult
