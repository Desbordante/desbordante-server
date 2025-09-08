from typing import Literal
from uuid import UUID

from src.schemas.base_schemas import BaseSchema
from src.schemas.task_schemas.primitives.nar.algo_config import (
    OneOfNarAlgoConfig,
)
from src.schemas.task_schemas.types import PrimitiveName


class NarTaskDatasetsConfig[T](BaseSchema):
    table: T


class NarTaskParams[T = UUID](BaseSchema):
    primitive_name: Literal[PrimitiveName.NAR]
    config: OneOfNarAlgoConfig
    datasets: NarTaskDatasetsConfig[T]
