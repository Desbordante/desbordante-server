from typing import Literal
from uuid import UUID

from src.schemas.base_schemas import BaseSchema
from src.schemas.task_schemas.primitives.afd_verification.algo_config import (
    OneOfAfdVerificationAlgoConfig,
)
from src.schemas.task_schemas.primitives.base_schemas import BaseTaskParams
from src.schemas.task_schemas.types import PrimitiveName


class AfdVerificationTaskDatasetsConfig[T](BaseSchema):
    table: T


class AfdVerificationTaskParams[T = UUID](
    BaseTaskParams[
        Literal[PrimitiveName.AFD_VERIFICATION],
        OneOfAfdVerificationAlgoConfig,
        AfdVerificationTaskDatasetsConfig[T],
    ]
): ...
