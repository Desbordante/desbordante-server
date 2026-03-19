from typing import Literal
from uuid import UUID

from src.schemas.base_schemas import BaseSchema
from src.schemas.task_schemas.primitives.base_schemas import BaseTaskParams
from src.schemas.task_schemas.primitives.nar.algo_config import (
    OneOfNarAlgoConfig,
)
from src.schemas.task_schemas.types import PrimitiveName


class NarTaskDatasetsConfig[T](BaseSchema):
    table: T


class NarTaskParams[T = UUID](
    BaseTaskParams[
        Literal[PrimitiveName.NAR],
        OneOfNarAlgoConfig,
        NarTaskDatasetsConfig[T],
    ]
): ...
