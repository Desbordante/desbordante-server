from typing import Literal
from uuid import UUID

from src.schemas.base_schemas import BaseSchema
from src.schemas.task_schemas.pfd.algo_config import (
    OneOfPfdAlgoConfig,
)
from src.schemas.task_schemas.types import PrimitiveName


class PfdTaskDatasetsConfig[T](BaseSchema):
    table: T


class PfdTaskParams[T = UUID](BaseSchema):
    primitive_name: Literal[PrimitiveName.PFD]
    config: OneOfPfdAlgoConfig
    datasets: PfdTaskDatasetsConfig[T]
