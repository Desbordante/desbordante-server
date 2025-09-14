from typing import Literal
from uuid import UUID

from src.schemas.base_schemas import BaseSchema
from src.schemas.task_schemas.primitives.base_schemas import BaseTaskParams
from src.schemas.task_schemas.primitives.mfd_verification.algo_config import (
    OneOfMfdVerificationAlgoConfig,
)
from src.schemas.task_schemas.types import PrimitiveName


class MfdVerificationTaskDatasetsConfig[T](BaseSchema):
    table: T


class MfdVerificationTaskParams[T = UUID](
    BaseTaskParams[
        Literal[PrimitiveName.MFD_VERIFICATION],
        OneOfMfdVerificationAlgoConfig,
        MfdVerificationTaskDatasetsConfig[T],
    ]
): ...
