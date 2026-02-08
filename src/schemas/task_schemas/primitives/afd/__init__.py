from typing import Literal

from src.schemas.base_schemas import BaseSchema
from src.schemas.task_schemas.primitives.afd.config import OneOfAfdConfig
from src.schemas.task_schemas.primitives.afd.result import AfdAlgoResult
from src.schemas.task_schemas.types import PrimitiveName


class BaseAfdTaskModel(BaseSchema):
    primitive_name: Literal[PrimitiveName.afd]


class AfdTaskConfig(BaseAfdTaskModel):
    config: OneOfAfdConfig


class AfdTaskResult(BaseAfdTaskModel):
    result: AfdAlgoResult
