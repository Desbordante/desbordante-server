from typing import Literal
from uuid import UUID

from src.schemas.base_schemas import BaseSchema
from src.schemas.task_schemas.primitives.adc.algo_config import OneOfAdcAlgoConfig
from src.schemas.task_schemas.primitives.base_schemas import BaseTaskParams
from src.schemas.task_schemas.types import PrimitiveName


class AdcTaskDatasetsConfig[T](BaseSchema):
    table: T


class AdcTaskParams[T = UUID](
    BaseTaskParams[
        Literal[PrimitiveName.ADC],
        OneOfAdcAlgoConfig,
        AdcTaskDatasetsConfig[T],
    ]
): ...
