from typing import Literal, Annotated
from pydantic import Field
from internal.domain.common import OptionalModel
from internal.domain.task.value_objects.ar.algo_name import ArAlgoName
from internal.domain.task.value_objects.ar.algo_descriptions import descriptions


class BaseArConfig(OptionalModel):
    __non_optional_fields__ = {
        "algo_name",
    }


class AprioriConfig(BaseArConfig):
    algo_name: Literal[ArAlgoName.Apriori]

    has_tid: Annotated[bool, Field(description=descriptions["has_tid"])]
    minconf: Annotated[float, Field(ge=0, le=1, description=descriptions["minconf"])]
    minsup: Annotated[float, Field(ge=0, le=1, description=descriptions["minsup"])]
    input_format: Annotated[
        str,
        Literal["singular", "tabular"],
        Field(description=descriptions["input_format"]),
    ]
    item_column_index: Annotated[
        int, Field(ge=0, description=descriptions["item_column_index"])
    ]
    tid_column_index: Annotated[
        int, Field(ge=0, description=descriptions["tid_column_index"])
    ]


OneOfArAlgoConfig = Annotated[
    AprioriConfig,
    Field(discriminator="algo_name"),
]
