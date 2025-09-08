from typing import Literal
from uuid import UUID

from src.schemas.base_schemas import BaseSchema
from src.schemas.task_schemas.primitives.afd.algo_config import OneOfAfdAlgoConfig
from src.schemas.task_schemas.types import PrimitiveName


class AfdTaskDatasetsConfig[T](BaseSchema):
    table: T


class AfdTaskParams[T = UUID](BaseSchema):
    primitive_name: Literal[PrimitiveName.AFD]
    config: OneOfAfdAlgoConfig
    datasets: AfdTaskDatasetsConfig[T]
