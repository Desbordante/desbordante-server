from typing import Literal
from uuid import UUID

from src.schemas.base_schemas import BaseSchema
from src.schemas.task_schemas.primitives.ar.algo_config import (
    OneOfArAlgoConfig,
)
from src.schemas.task_schemas.primitives.base_schemas import BaseTaskParams
from src.schemas.task_schemas.types import PrimitiveName


class ArTaskDatasetsConfig[T](BaseSchema):
    table: T


class ArTaskParams[T = UUID](
    BaseTaskParams[
        Literal[PrimitiveName.AR],
        OneOfArAlgoConfig,
        ArTaskDatasetsConfig[T],
    ]
): ...
