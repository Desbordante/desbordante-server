from typing import Literal
from uuid import UUID

from src.schemas.base_schemas import BaseSchema
from src.schemas.task_schemas.ac.algo_config import OneOfAcAlgoConfig
from src.schemas.task_schemas.types import PrimitiveName


class AcTaskDatasetsConfig[T](BaseSchema):
    table: T


class AcTaskParams[T = UUID](BaseSchema):
    primitive_name: Literal[PrimitiveName.AC]
    config: OneOfAcAlgoConfig
    datasets: AcTaskDatasetsConfig[T]
