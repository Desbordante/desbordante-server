from typing import Literal
from uuid import UUID

from src.schemas.base_schemas import BaseSchema
from src.schemas.task_schemas.afd.algo_config import OneOfAfdAlgoConfig
from src.schemas.task_schemas.types import PrimitiveName


class AFdTaskDatasetsConfig[T](BaseSchema):
    table: T


class AFdTaskParams[T = UUID](BaseSchema):
    primitive_name: Literal[PrimitiveName.AFD]
    config: OneOfAfdAlgoConfig
    datasets: AFdTaskDatasetsConfig[T]
