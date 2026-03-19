from typing import Literal
from uuid import UUID

from src.schemas.base_schemas import BaseSchema
from src.schemas.task_schemas.primitives.base_schemas import BaseTaskParams
from src.schemas.task_schemas.primitives.dd.algo_config import OneOfDdAlgoConfig
from src.schemas.task_schemas.types import PrimitiveName


class DdTaskDatasetsConfig[T](BaseSchema):
    table: T
    dif_table: T


class DdTaskParams[T = UUID](
    BaseTaskParams[
        Literal[PrimitiveName.DD],
        OneOfDdAlgoConfig,
        DdTaskDatasetsConfig[T],
    ]
): ...
