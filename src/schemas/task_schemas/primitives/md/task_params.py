from typing import Literal
from uuid import UUID

from src.schemas.base_schemas import BaseSchema
from src.schemas.task_schemas.primitives.md.algo_config import OneOfMdAlgoConfig
from src.schemas.task_schemas.types import PrimitiveName


class MdTaskDatasetsConfig[T](BaseSchema):
    left_table: T
    right_table: T


class MdTaskParams[T = UUID](BaseSchema):
    primitive_name: Literal[PrimitiveName.MD]
    config: OneOfMdAlgoConfig
    datasets: MdTaskDatasetsConfig[T]
