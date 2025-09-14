from typing import Literal
from uuid import UUID

from src.schemas.base_schemas import BaseSchema
from src.schemas.task_schemas.primitives.ac.algo_config import OneOfAcAlgoConfig
from src.schemas.task_schemas.primitives.base_schemas import BaseTaskParams
from src.schemas.task_schemas.types import PrimitiveName


class AcTaskDatasetsConfig[T](BaseSchema):
    table: T


class AcTaskParams[T = UUID](
    BaseTaskParams[
        Literal[PrimitiveName.AC],
        OneOfAcAlgoConfig,
        AcTaskDatasetsConfig[T],
    ]
): ...
