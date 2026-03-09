from typing import Literal
from uuid import UUID

from src.schemas.base_schemas import BaseSchema
from src.schemas.task_schemas.primitives.base_schemas import BaseTaskParams
from src.schemas.task_schemas.primitives.fd_verification.algo_config import (
    OneOfFdVerificationAlgoConfig,
)
from src.schemas.task_schemas.types import PrimitiveName


class FdVerificationTaskDatasetsConfig[T](BaseSchema):
    table: T


class FdVerificationTaskParams[T = UUID](
    BaseTaskParams[
        Literal[PrimitiveName.FD_VERIFICATION],
        OneOfFdVerificationAlgoConfig,
        FdVerificationTaskDatasetsConfig[T],
    ]
): ...
