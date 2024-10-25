from typing import Literal, Annotated
from pydantic import Field
from internal.domain.common import OptionalModel
from internal.domain.task.value_objects.ind.algo_name import IndAlgoName
from internal.domain.task.value_objects.ind.algo_descriptions import descriptions


class BaseIndConfig(OptionalModel):
    __non_optional_fields__ = {
        "algo_name",
    }


class FaidaConfig(BaseIndConfig):
    algo_name: Literal[IndAlgoName.Faida]

    max_arity: Annotated[int, Field(gt=0, description=descriptions["max_arity"])]
    sample_size: Annotated[int, Field(gt=0, description=descriptions["sample_size"])]
    ignore_constant_cols: Annotated[
        bool, Field(description=descriptions["ignore_constant_cols"])
    ]
    hll_accuracy: Annotated[
        float, Field(gt=0, description=descriptions["hll_accuracy"])
    ]
    ignore_null_cols: Annotated[
        bool, Field(description=descriptions["ignore_null_cols"])
    ]
    threads: Annotated[int, Field(ge=0, description=descriptions["threads"])]


class MindConfig(BaseIndConfig):
    algo_name: Literal[IndAlgoName.Mind]

    max_arity: Annotated[int, Field(gt=0, description=descriptions["max_arity"])]
    error: Annotated[float, Field(ge=0, le=1.0, description=descriptions["error"])]


class SpiderConfig(BaseIndConfig):
    algo_name: Literal[IndAlgoName.Spider]

    error: Annotated[float, Field(ge=0, le=1.0, description=descriptions["error"])]
    is_null_equal_null: Annotated[
        bool, Field(description=descriptions["is_null_equal_null"])
    ]
    threads: Annotated[int, Field(ge=0, description=descriptions["threads"])]
    mem_limit: Annotated[int, Field(gt=0, description=descriptions["mem_limit"])]


OneOfIndAlgoConfig = Annotated[
    FaidaConfig | MindConfig | SpiderConfig,
    Field(discriminator="algo_name"),
]
