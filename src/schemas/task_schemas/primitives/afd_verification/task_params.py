from typing import Literal
from uuid import UUID

from src.schemas.base_schemas import BaseSchema
from src.schemas.task_schemas.primitives.afd_verification.algo_config import (
    OneOfAfdVerificationAlgoConfig,
)
from src.schemas.task_schemas.types import PrimitiveName


class AfdVerificationTaskDatasetsConfig[T](BaseSchema):
    table: T


class AfdVerificationTaskParams[T = UUID](BaseSchema):
    primitive_name: Literal[PrimitiveName.AFD_VERIFICATION]
    config: OneOfAfdVerificationAlgoConfig
    datasets: AfdVerificationTaskDatasetsConfig[T]
