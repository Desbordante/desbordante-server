from typing import Literal
from uuid import UUID

from src.schemas.base_schemas import BaseSchema
from src.schemas.task_schemas.primitives.adc.algo_config import OneOfAdcAlgoConfig
from src.schemas.task_schemas.types import PrimitiveName


class AdcTaskDatasetsConfig[T](BaseSchema):
    table: T


class AdcTaskParams[T = UUID](BaseSchema):
    primitive_name: Literal[PrimitiveName.ADC]
    config: OneOfAdcAlgoConfig
    datasets: AdcTaskDatasetsConfig[T]
