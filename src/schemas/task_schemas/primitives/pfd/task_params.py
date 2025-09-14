from typing import Literal
from uuid import UUID

from src.schemas.base_schemas import BaseSchema
from src.schemas.task_schemas.primitives.base_schemas import BaseTaskParams
from src.schemas.task_schemas.primitives.pfd.algo_config import (
    OneOfPfdAlgoConfig,
)
from src.schemas.task_schemas.types import PrimitiveName


class PfdTaskDatasetsConfig[T](BaseSchema):
    table: T


class PfdTaskParams[T = UUID](
    BaseTaskParams[
        Literal[PrimitiveName.PFD],
        OneOfPfdAlgoConfig,
        PfdTaskDatasetsConfig[T],
    ]
): ...
