from typing import Literal
from uuid import UUID

from src.schemas.base_schemas import BaseSchema
from src.schemas.task_schemas.ar.algo_config import (
    OneOfArAlgoConfig,
)
from src.schemas.task_schemas.types import PrimitiveName


class ArTaskDatasetsConfig[T](BaseSchema):
    table: T


class ArTaskParams[T = UUID](BaseSchema):
    primitive_name: Literal[PrimitiveName.AR]
    config: OneOfArAlgoConfig
    datasets: ArTaskDatasetsConfig[T]
