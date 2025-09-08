from typing import Literal
from uuid import UUID

from src.schemas.base_schemas import BaseSchema
from src.schemas.task_schemas.primitives.fd.algo_config import OneOfFdAlgoConfig
from src.schemas.task_schemas.types import PrimitiveName


class FdTaskDatasetsConfig[T](BaseSchema):
    table: T


class FdTaskParams[T = UUID](BaseSchema):
    primitive_name: Literal[PrimitiveName.FD]
    config: OneOfFdAlgoConfig
    datasets: FdTaskDatasetsConfig[T]
