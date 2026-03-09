from typing import Literal
from uuid import UUID

from src.schemas.base_schemas import BaseSchema
from src.schemas.task_schemas.primitives.afd.algo_config import OneOfAfdAlgoConfig
from src.schemas.task_schemas.primitives.base_schemas import BaseTaskParams
from src.schemas.task_schemas.types import PrimitiveName


class AfdTaskDatasetsConfig[T](BaseSchema):
    table: T


class AfdTaskParams[T = UUID](
    BaseTaskParams[
        Literal[PrimitiveName.AFD],
        OneOfAfdAlgoConfig,
        AfdTaskDatasetsConfig[T],
    ]
): ...
