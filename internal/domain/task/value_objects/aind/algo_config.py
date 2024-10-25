from typing import Literal, Annotated
from pydantic import Field
from internal.domain.common import OptionalModel
from internal.domain.task.value_objects.aind.algo_name import AindAlgoName
from internal.domain.task.value_objects.aind.algo_descriptions import descriptions


class BaseAindConfig(OptionalModel):
    __non_optional_fields__ = {
        "algo_name",
    }


class MindConfig(BaseAindConfig):
    algo_name: Literal[AindAlgoName.Mind]

    max_arity: Annotated[int, Field(gt=0, description=descriptions["max_arity"])]
    error: Annotated[float, Field(ge=0, le=1.0, description=descriptions["error"])]


class SpiderConfig(BaseAindConfig):
    algo_name: Literal[AindAlgoName.Spider]

    error: Annotated[float, Field(ge=0, le=1.0, description=descriptions["error"])]
    is_null_equal_null: Annotated[
        bool, Field(description=descriptions["is_null_equal_null"])
    ]
    threads: Annotated[int, Field(ge=0, description=descriptions["threads"])]
    mem_limit: Annotated[int, Field(gt=0, description=descriptions["mem_limit"])]


OneOfAindAlgoConfig = Annotated[
    MindConfig | SpiderConfig,
    Field(discriminator="algo_name"),
]
